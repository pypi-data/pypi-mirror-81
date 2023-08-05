# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Majormode.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Majormode or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Majormode.
#
# MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY
# OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE SHALL NOT BE LIABLE FOR ANY
# LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
# OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

import collections
import hashlib
import io
import os
import re
import unidecode
import uuid

from majormode.perseus.constant.contact import ContactName
from majormode.perseus.constant.obj import ObjectStatus
from majormode.perseus.constant.regex import REGEX_PATTERN_EMAIL_ADDRESS
from majormode.perseus.model.contact import Contact
from majormode.perseus.model.enum import Enum
from majormode.perseus.model.locale import DEFAULT_LOCALE
from majormode.perseus.model.locale import Locale
from majormode.perseus.utils import cast
from majormode.perseus.utils import file_util
from majormode.perseus.utils import image_util
from majormode.perseus.utils.date_util import ISO8601DateTime
from PIL import Image

from majormode.perseus.service.account.contact_service import ContactService
from majormode.perseus.service.account.session_service import SessionService
from majormode.perseus.service.base_rdbms_service import BaseRdbmsService
from majormode.perseus.service.base_service import BaseService

import settings


# Default image file format to store the image with
# (cf. https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).
DEFAULT_IMAGE_FILE_FORMAT = 'JPEG'

# Default file extensions per image file format.  When not defined, the
# file extension is named after the image file format.
DEFAULT_IMAGE_FILE_FORMAT_EXTENSIONS = {
    'JPEG': 'jpg'
}

# Default quality to store the image with, on a scale from `1` (worst)
# to `95` (best).  Values above `95` should be avoided; `100` disables
# portions of the JPEG compression algorithm, and results in large files
# with hardly any gain in image quality.
DEFAULT_IMAGE_QUALITY = 75



class AccountService(BaseRdbmsService):
    """
    A user's account allows a user to authenticate to the platform and be
    granted authorization to access them; however, authentication does not
    imply authorization.  To log in to an account, a user is typically
    required to authenticate oneself with a password or other credentials
    for the purposes of accounting, security, logging, and resource
    management.  Once the user has logged on, the platform uses an
    identifier to refer to him, rather than his email address or his
    username, through a process known as identity correlation.
    """
    AccountType = Enum(
        'standard',
        'sns',
        'ghost',
        'botnet',
        'test',
        'administrator'
    )

    class AuthenticationFailureException(BaseService.IllegalAccessException):
        """
        Signal that the email address or password that has been provided for
        authenticating a user account is incorrect.
        """
        pass

    class UsernameAlreadyUsedException(BaseService.InvalidOperationException):
        """
        Signal that the username provided for signing-up a user account is
        already associated with an existing user account registered on the
        platform.
        """
        pass

    # Define the name of the Content Delivery Network (CDN) bucket that
    # groups user avatars all together.
    CDN_BUCKET_NAME_AVATAR = 'avatar'

    # Define the minimal allowed duration of time, expressed in seconds,
    # between two consecutive requests of a same user to reset his
    # forgotten password.
    MINIMAL_TIME_BETWEEN_PASSWORD_RESET_REQUEST = 60 * 5

    # Define the duration in seconds a password reset request lives before
    # it is deleted.
    PASSWORD_RESET_REQUEST_LIFESPAN = 25 * 60 * 60;

    # The password of a user account must:
    #
    # * be at least eight characters.
    # * contain at least one number (0-9).
    # * contain at least one uppercase letter (A-Z).
    # * contain at least one lowercase letter (a-z).
    # * not contain three consecutive identical characters.
    # * not have been used in the past year.
    # * not be the same as the user name of the user's email address.
    REGEX_PASSWORD = re.compile(r'^[a-zA-Z0-9@#$%\^&*+._<>=-]{6,18}$')

    def __index_account(
            self,
            account_id,
            full_name,
            connection=None):
        """
        Index the account of a user with the personal name by which this user
        is known.


        :param account_id: identification of the account of this child.

        :param full_name: personal name by which this user is known.

        :param connection: A `RdbmsConnection` instance to be used supporting
            the Python clause `with ...:`.
        """
        keywords = self.__string_to_keywords(full_name)

        if keywords:
            with self.acquire_rdbms_connection(auto_commit=True, connection=connection) as connection:
                connection.execute(
                    """
                    DELETE FROM 
                        account_index
                      WHERE 
                        account_id = %(account_id)s
                    """,
                    {
                        'account_id': account_id
                    })

                connection.execute(
                    """
                    INSERT INTO 
                        account_index(
                          account_id,
                          keyword)
                      VALUES 
                        %[values]s
                    """,
                    {
                        'values': [(account_id, keyword) for keyword in keywords]
                    })

    @staticmethod
    def __string_to_keywords(string, keyword_minimal_length=1):
        """
        Remove any punctuation character from the specified list of keywords,
        remove any double or more space character and represent Unicode
        characters in ASCII.


        :param keywords: a list of keywords strip out any punctuation characters.

        :param keyword_minimal_length: minimal number of characters of the
            keywords to be returned.


        :return: the set of keywords cleansed from any special Unicode
            accentuated character, punctuation character, and double space
            character.
        """
        if not string:
            return

        # Convert the string to ASCII lower characters.
        ascii_string = unidecode.unidecode(string).lower()

        # Replace any punctuation character with space.
        punctuationless_string = re.sub(r"""[.,\\/#!$%\^&*;:{}=\-_`~()<>"']""", ' ', ascii_string)

        # Remove any double space character.
        cleansed_string = re.sub(r'\s{2,}', ' ', punctuationless_string)

        # Decompose the string into distinct keywords.
        keywords = set(cleansed_string.split(' '))

        # Filter out sub-keywords of less than 2 characters.
        return [keyword for keyword in keywords if len(keyword) > keyword_minimal_length]

    @staticmethod
    def _cleanse_keywords(keywords):
        """
        Remove any punctuation character from the specified list of keywords,
        remove any double or more space character and represent Unicode
        characters in ASCII.


        :param keywords: a list of keywords strip out any punctuation characters.


        :return: the set of keywords cleansed from any special Unicode
            accentuated character, punctuation character, and double space
            character.
        """
        if not isinstance(keywords, (list, set, tuple)):
            keywords = [ keywords ]

        # Normalize the given keywords and split them into sub-keywords if
        # needed.  For instance:
        #
        #   [ u'Saint-Élie-de-Caxton', u'Québec' ]
        #
        # becomes:
        #
        #   [ [ u'saint', u'elie', u'de', u'caxton' ], [ u'Québec' ]]
        sub_keywords_list = [
            re.sub(                                         # 3. Remove any double space character
                r'\s{2,}',
                ' ',
                re.sub(                                     # 2. Remove any punctuation character
                    r"""[.,\\/#!$%\^&*;:{}=\-_`~()<>"']""",
                    ' ',
                    unidecode.unidecode(keyword).lower()))  # 1. Convert to ASCII characters
            .split(' ')                                     # 4. Split sub-keywords
            for keyword in keywords]

        # Merge all the sub-keywords in a single list.
        cleansed_keywords = set()
        map(lambda sub_keywords: cleansed_keywords.update(sub_keywords), sub_keywords_list)

        # Filter out sub-keywords of less than 2 characters.
        return [ keyword for keyword in cleansed_keywords if len(keyword) > 2 ]

    @classmethod
    def build_picture_url(cls, picture_id):
        """
        Return the Uniform Resource Locator of an account's picture.


        :param picture_id: Identification of the picture of an account.


        :return: A string representing the Uniform Resource Locator of the
            picture.
        """
        return picture_id and os.path.join(
            settings.CDN_URL_HOSTNAME,
            cls.CDN_BUCKET_NAME_AVATAR,
            str(picture_id))

    def change_password(self, app_id, account_id, old_password, new_password):
        """
        Change the password of the specified user's account with a new
        password that this user is providing.

        The new password must respect the rules of definition of a password.
        It cannot be identical to the old password.  It cannot contains part
        of the email address of the user.


        :param app_id: identification of the client application such as a Web,
           a desktop, or a mobile application, that accesses the service.

        :param account_id: identification of the account of the user who is
           changing his password.

        :param old_password: old password of the user's account.

        :param new_password: new password of this user's account.


        :raise IllegalAccessException: if the old password that is passed to
               the function is wrong.

        :raise InvalidArgumentException: if the new password doesn't conform
           to the rules of password definition, if the new  password is
           identical to the old password of the user.

        :raise UndefinedObjectException: if the specified identification
           doesn't refer to a user account registered against the platform.
        """
        new_password = new_password.strip()
        if not AccountService.REGEX_PASSWORD.match(new_password):
            raise self.InvalidArgumentException("The new password specified does not conform to the rules of the password definition")

        with self.acquire_rdbms_connection(auto_commit=True) as connection:
            cursor = connection.execute(
                """
                SELECT password
                  FROM account
                  WHERE account_id = %(account_id)s
                  FOR UPDATE
                """,
                {
                    'account_id': account_id
                })
            row = cursor.fetch_one()
            if row is None:
                raise self.UndefinedObjectException()
            account = row.get_object()

            old_password = old_password.strip()
            if hashlib.md5(old_password.encode()).hexdigest() != account.password:
                raise self.IllegalAccessException()

            if new_password == old_password:
                raise self.InvalidArgumentException("The new password cannot be identical to the previous password")

            cursor = connection.execute(
                """
                UPDATE account
                  SET password = %(new_password)s,
                      update_time = current_timestamp::timestamptz(3)
                  WHERE account_id = %(account_id)s
                  """,
                {
                    'account_id': account_id,
                    'new_password': hashlib.md5(new_password.encode()).hexdigest()
                })

    def get_account(
            self,
            account_id,
            check_status=False,
            connection=None,
            include_contacts=False):
        """
        Return extended information about a user account specified by its
        identification.

        @warning: this function is for internal usage only; it MUST not be
            surfaced to client applications.


        :param account_id: identification of the user account that is
            requested its information.

        :param check_status: indicate whether the function must check the
            current status of this user account and raise an exception if it
            is not of enabled.

        :param include_contacts: indicate whether to include the contacts
            information of this user account.

        :param connection: a `RdbmsConnection` instance to be used
            supporting the Python clause `with ...:`.


        :return: an instance containing the following members:

             * `account_id`: identification of the user account.

             * `account_type`: type of the user account as defined in the
               enumeration `AccountService.AccountType`.

             * `contacts` (optional): list of properties such as e-mail
                addresses, phone numbers, etc., in respect of the electronic
                business card specification (vCard).  The contact information
                is represented by a list of tuples of the following form::

                   (name:Contact.ContactName, value:string, is_primary:boolean, is_verified:boolean)

                where:

                * `name`: type of this contact information, which can be one
                  of these standard names in respect of the electronic
                  business card specification (vCard).

                * `value`: value of this contact information representing by
                  a string, such as `+84.01272170781`, the formatted value
                  for a telephone number property.

                * `is_primary`: indicate whether this contact information is
                  the primary.

                * `is_verified`: indicate whether this contact information
                  has been verified, whether it has been grabbed from a
                  trusted Social Networking Service (SNS), or whether through
                  a challenge/response process.

             * `creation_time`: time when this user account has been
               registered against the platform.  This attribute is returned
               only if the user on behalf of whom this function is called is
               the owner of this account or connected with this user.

             * `full_name`: full name of the user.

             * `locale`: a `Locale` instance that identifies the preferred
               language of the user, or English by default.

            * `object_status`: An item of the enumeration `ObjectStatus`
              representing thr current status of this user account.

             * `picture_id`: identification of the user account's picture,
               if any picture defined for this user account.

             * `picture_url`: Uniform Resource Locator (URL) that specifies
               the location of the user account's picture, if any defined.
               The client application can use this URL and append the query
               parameter `size` to specify a given pixel resolution of the
               user account's picture, such as `thumbnail`, `small`,
               `medium`, `large` (cf. `settings.IMAGE_PIXEL_RESOLUTIONS['avatar']`).

             * `timezone`: time zone of the default location of the user.
               It is the difference between the time at this location and UTC
               (Universal Time Coordinated).  UTC is also  known as GMT or
               Greenwich Mean Time or Zulu Time.

             * `update_time`: time when the information of this user account
               has been updated for the last time.

             * `username`: a name used to gain access to a the platform.


        :raise DeletedObjectException: if the user account has been deleted
            while the argument `check_status` has been set to `True`.

        :raise DisabledObjectException: if the user account has been disabled
            while the argument `check_status` has been set to `True`.

        :raise UndefinedObjectException: if the specified identification
            doesn't refer to a user account registered against the platform.
        """
        with self.acquire_rdbms_connection(
                auto_commit=False,
                connection=connection) as connection:
            cursor = connection.execute(
                """
                SELECT
                    account_id,
                    full_name,
                    username,
                    picture_id,
                    locale,
                    timezone,
                    account_type,
                    object_status,
                    creation_time,
                    update_time
                  FROM
                    account
                  WHERE
                    account_id = %(account_id)s
                """,
                {
                    'account_id': account_id
                })
            row = cursor.fetch_one()
            if row is None:
                raise self.UndefinedObjectException(
                    f"The account {account_id} is not registered to the platform",
                    payload={'account_id': account_id})

            account = row.get_object({
                'account_id': cast.string_to_uuid,
                'account_type': AccountService.AccountType,
                'creation_time': cast.string_to_timestamp,
                'locale': Locale.from_string,
                'object_status': ObjectStatus,
                'update_time': cast.string_to_timestamp
            })

            if check_status:
                if account.object_status == ObjectStatus.disabled:
                    raise self.DisabledObjectException()
                elif account.object_status == ObjectStatus.deleted:
                    raise self.DeletedObjectException()

            account.picture_url = self.build_picture_url(account.picture_id)

            # Include the contacts information of this user account.
            if include_contacts:
                account.contacts = ContactService().get_contacts(account_id, connection=connection)

            return account

    def get_account_by_contact(
            self,
            contact,
            check_status=False,
            connection=None,
            include_pending=False,
            is_verified=True):
        """
        Return extended information about the user account specified by a
        contact information, such as, for instance, an email address, a phone
        number.


        @note: The provided contact information MUST have been verified in
        order to return a user account.

        @warning: This function is for internal usage only; it MUST not be
            surfaced to client applications.


        :param contact: An object `Contact`.

        :param check_status: Indicate whether the function MUST check the
            current status of this user account and raise an exception if is
            not of enabled.

        :param connection: Am object `RdbmsConnection` to be used supporting
            the Python clause `with ...:`.

        :param include_pending: indicate whether to include pending account
            or only enabled account.

        :param is_verified: Indicate whether the function MUST only return a
            user account if the matching contact information has been
            verified.


        :return: An object containing the following members:

            * `account_id`: Identification of the user account.

            * `full_name`: Full name of the user.

            * `username`: Name of the account of the user, if any defined.

            * `picture_id`: Identification of the user account's picture, if any
              picture defined for this user account.

            * `picture_url`: Uniform Resource Locator (URL) that specifies the
              location of the user account's picture, if any defined.  The client
              application can use this URL and append the query parameter `size`
              to specify a given pixel resolution of the user account's picture,
              such as `thumbnail`, `small`, `medium`, `large` (cf.
              `settings.IMAGE_PIXEL_RESOLUTIONS['avatar']`).

            * `locale` (required): An object `Locale` that identifies the
              preferred language of the user, or English by default.

            * `timezone`: Time zone of the default location of the user.  It is
              the difference between the time at this location and UTC (Universal
              Time Coordinated).  UTC is also  known as GMT or Greenwich Mean Time
              or Zulu Time.

            * `account_type`: Type of the user account as defined in the
              enumeration `AccountType`.

            * `is_verified`: Indicate whether the matching contact information
              has been verified.

            * `object_status`: Current status of this user account.

            * `creation_time`: Time when this user account has been registered
              against the platform.  This attribute is returned only if the user
              on behalf of whom this function is called is the owner of this
              account or connected with this user.

            * `update_time`: Time when the information of this user account has
              been updated for the last time.


        :raise DeletedObjectException: If the user account has been deleted,
            while the argument `check_status` has been set to `True`.

        :raise DisabledObjectException: If the user account has been disabled,
            while the argument `check_status` has been set to `True`.

        :raise UndefinedObjectException: If the specified contact doesn't
            refer to a user account registered against the platform.
        """
        with self.acquire_rdbms_connection(auto_commit=False, connection=connection) as connection:
            cursor = connection.execute(
                """
                SELECT 
                    account_id,
                    full_name,
                    username,
                    picture_id,
                    locale,
                    timezone,
                    account_type,
                    is_verified,
                    account.object_status,
                    account.creation_time,
                    account.update_time
                  FROM 
                    account
                  INNER JOIN account_contact
                    USING (account_id)
                  WHERE 
                    name = %(name)s
                    AND lower(value) = lower(%(value)s)
                    AND (account.object_status = %(OBJECT_STATUS_ENABLED)s
                         OR (%(include_pending)s AND account.object_status = %(OBJECT_STATUS_PENDING)s))
                    AND (NOT %(is_verified)s OR is_verified)
                """,
                {
                    'OBJECT_STATUS_ENABLED': ObjectStatus.enabled,
                    'OBJECT_STATUS_PENDING': ObjectStatus.pending,
                    'include_pending': include_pending,
                    'is_verified': is_verified,
                    'name': contact.name,
                    'value': contact.value.strip()
                })
            row = cursor.fetch_one()

            if row is None:
                raise self.UndefinedObjectException('No account associated to the specified contact information')

            account = row.get_object({
                'account_id': cast.string_to_uuid,
                'account_type': AccountService.AccountType,
                'creation_time': cast.string_to_timestamp,
                'locale': Locale.from_string,
                'update_time': cast.string_to_timestamp
            })

            if check_status:
                if account.object_status == ObjectStatus.disabled:
                    raise self.DisabledObjectException()
                elif account.object_status == ObjectStatus.deleted:
                    raise self.DeletedObjectException()

            account.picture_url = self.build_picture_url(account.picture_id)

            return account

    def get_accounts(
            self,
            app_id,
            account_ids,
            account_id=None,
            start_time=None,
            is_verified=False,
            include_contacts=False,
            include_pending=False):
        """
        Return up to 100 users worth of extended information, specified by
        their identification.

        If a requested user is unknown, suspended, or deleted, then that user
        will not be returned in the results list.


        :param app_id: identification of the client application such as a Web,
               a desktop, or a mobile application, that accesses the service.

        :param account_ids: a list of account identifications or email
               addresses.

        :param account_id: identification of the user account that is
               requesting this information, if this information is available.

        :param start_time: indicate the earliest time to return a information
               of user account that might have been modified since.  If not
               specified, the function returns information about all the
               specified user accounts.

        :param include_contacts: indicate whether to include the contacts
            information of these user accounts.


        :return: a list of instances containing the following members:

                 * `account_id`: identification of the user account.

                 * `full_name`: full name of the user.

                 * `username`: name of the account of the user,
                   if any defined.

                 * `picture_id`: identification of the user account's
                   picture, if any picture defined for this user account.

                 * `picture_url`: Uniform Resource Locator (URL) that
                   specifies the location of the user account's picture, if
                   any defined.  The client application can use this URL and
                   append the query parameter `size` to specify a given
                   pixel resolution of the user account's picture, such as
                   `thumbnail`, `small`, `medium`, `large`.

                 * `locale`: a `Locale` instance that identifies the
                   preferred language of the user, or English by default.

                 * `timezone`: time zone of the default location of the user.
                   It is the difference between the time at this location and
                   UTC (Universal Time Coordinated).  UTC is also  known as
                   GMT or Greenwich Mean Time or Zulu Time.

                * `creation_time`: time when this user account has been
                   registered against the platform.  This attribute is
                   returned only if the user on behalf of whom this function
                   is called is the owner of this account, connected with this
                   user, or an administrator of the platform.

                * `update_time`: time when the information of this user
                  account has been updated for the last time.

        :raise DeletedObjectException: if the user account has been deleted.

        :raise DisabledObjectException: if the user account has been disabled.

        :raise UndefinedObjectException: if the specified identification
               doesn't refer to a user account registered against the
               platform.
        """
        account_ids = set(account_ids)

        is_super_user = account_id and \
            self.get_account(account_id, check_status=True).account_type in [
                AccountService.AccountType.administrator, AccountService.AccountType.botnet ]

        if len(account_ids) == 0:
            return []

        with self.acquire_rdbms_connection() as connection:
            # For any email address provided, determine the identification of the
            # corresponding account.
            email_addresses = [ email_address for email_address in account_ids
                    if isinstance(email_address, str) and REGEX_PATTERN_EMAIL_ADDRESS.match(email_address.strip().lower()) ]
            if len(email_addresses) > 0:
                account_ids = account_ids - set(email_addresses)
                cursor = connection.execute(
                    """
                    SELECT DISTINCT 
                        account_id
                      FROM 
                        account_contact
                        WHERE 
                            name = %(PROPERTY_NAME_EMAIL)s
                          AND lower(value) IN (%[email_addresses]s)
                          AND (NOT %(is_verified)s OR is_verified)
                    """,
                    {
                        'PROPERTY_NAME_EMAIL': self.Contact.ContactName.EMAIL,
                        'email_addresses': [ email_address.strip().lower() for email_address in email_addresses ],
                        'is_verified': is_verified
                    })

                account_ids.update([ row.get_value('account_id', cast.string_to_uuid)
                        for row in cursor.fetch_all() ])

            cursor = connection.execute(
                """
                SELECT 
                    account_id,
                    full_name,
                    username,
                    picture_id,
                    locale,
                    timezone,
                    is_account_connected_to(%(account_id)s, account_id) AS is_connected,
                    creation_time,
                    update_time
                  FROM 
                    account
                  WHERE 
                    account_id IN (%[account_ids]s)
                    AND (object_status = %(OBJECT_STATUS_ENABLED)s OR
                         (%(include_pending)s AND object_status = %(OBJECT_STATUS_PENDING)s))
                    AND (%(start_time)s IS NULL OR update_time >= %(start_time)s)
                """,
                {
                    'OBJECT_STATUS_ENABLED': ObjectStatus.enabled,
                    'OBJECT_STATUS_PENDING': ObjectStatus.pending,
                    'account_id': account_id,
                    'account_ids': list(account_ids)[:self.MAXIMUM_LIMIT],
                    'include_pending': include_pending,
                    'start_time': start_time
                })

            accounts = [
                row.get_object({
                    'account_id': cast.string_to_uuid,
                    'creation_time': cast.string_to_timestamp,
                    'locale': Locale.from_string,
                    'update_time': cast.string_to_timestamp })
                for row in cursor.fetch_all()
            ]

            for account in accounts:
                account.picture_url = self.build_picture_url(account.picture_id)

            # Include the contacts information of the user accounts.
            if include_contacts:
                accounts_dict = dict([(account.account_id, account) for account in accounts])

                cursor = connection.execute(
                    """
                    SELECT 
                        account_id,
                        name,
                        value,
                        is_primary,
                        is_verified
                      FROM
                        account_contact
                      WHERE
                        account_id IN (%[account_ids]s)
                        AND object_status = %(OBJECT_STATUS_ENABLED)s
                    """,
                    {
                        'OBJECT_STATUS_ENABLED': ObjectStatus.enabled,
                        'account_ids': accounts_dict.keys()
                    })

                accounts_contacts = collections.defaultdict(list)
                for account_contact in [
                    row.get_object({
                        'account_id': cast.string_to_uuid,
                        'name': AccountService.Contact.ContactName
                    })
                    for row in cursor.fetch_all()
                ]:
                    accounts_contacts[account_contact.account_id].append(account_contact)
                    del account_contact.account_id

                for account_id, account_contacts in accounts_contacts.items():
                    accounts_dict[account_id].contacts = account_contacts

            return accounts

    def get_accounts_by_contacts(
            self,
            contacts,
            verified_only=False,
            ignore_deleted=True):
        """
        Return a list of accounts that match the specified contact
        information.


        :param contacts: a list of tuple `(name, value)` where:

               * `name`: name of a property, which can be one of a set of
                 pre-defined strings such as:

                 * `EMAIL`: e-mail address.

                 * `PHONE`: phone number in E.164 numbering plan, an ITU-T
                   recommendation which defines the international public
                   telecommunication numbering plan used in the Public
                   Switched Telephone Network (PSTN).

              * `value`: value of the property representing by a string,
                such as `+84.01272170781`, the formatted value for the
                Telephone Number property.

        :param verified_only: indicate whether the function must only return
               accounts that match contact information which has been
               verified.

        :param ignore_deleted: indicate whether the function must ignore
               accounts that are deleted.


        :return: a list of instances containing the following members:

            * `account_id`: identification of the user account.

            * `full_name`: full name of the user.

            * `username`: name of the account of the user, if any defined.

            * `picture_id`: identification of the user account's picture, if any
              picture defined.

            * `picture_url`: Uniform Resource Locator (URL) that specifies the
              location of the user account's picture, if any defined.  The client
              application can use this URL and append the query parameter `size`
              to specify a given pixel resolution of the user account's picture,
              such as `thumbnail`, `small`, `medium`, `large` (cf.
              `settings.IMAGE_PIXEL_RESOLUTIONS['avatar']`).

            * `locale`: a `Locale` instance that identifies the preferred
              language of the user, or English by default.

            * `timezone`: time zone of the default location of the user.  It is
              the difference between the time at this location and UTC (Universal
              Time Coordinated).  UTC is also  known as GMT or Greenwich Mean Time
              or Zulu Time.

            * `account_type`: type of the user account as defined in the
              enumeration `AccountType`.

            * `object_status`: current status of this user account.

            * `creation_time`: time when this user account has been registered
              to the platform.

            * `update_time`: time when the information of this user account has
              been updated for the last time.
        """
        if not isinstance(contacts, (list, set)) or len(contacts) == 0:
            return []

        with self.acquire_rdbms_connection() as connection:
            cursor = connection.execute("""
                SELECT
                    account_id,
                    picture_id,
                    locale,
                    timezone,
                    account_type,
                    account.object_status,
                    creation_time,
                    update_time
                  FROM (
                    SELECT DISTINCT
                        account_id
                      FROM
                          account_contact,
                          (VALUES %[values]s) AS foo(name, value)
                        WHERE 
                          account_contact.name = foo.name
                          AND lower(account_contact.value) = lower(trim(both ' ' from foo.value))
                          AND (NOT %(verified_only)s OR is_verified)
                          AND object_status = %(OBJECT_STATUS_ENABLED)s) AS foo
                  INNER JOIN account
                    USING (account_id)""",
                { 'OBJECT_STATUS_ENABLED': ObjectStatus.enabled,
                  'values': contacts,
                  'verified_only': verified_only })
            accounts = [ row.get_object({
                    'account_id': cast.string_to_uuid,
                    'creation_time': cast.string_to_timestamp,
                    'picture_id': cast.string_to_uuid,
                    'update_time': cast.string_to_uuid })
                for row in cursor.fetch_all() ]

            if ignore_deleted:
                accounts = [ account for account in accounts
                        if account.object_status != ObjectStatus.deleted ]

            for account in accounts:
                account.picture_url = self.build_picture_url(account.picture_id)

            return accounts

    def get_password_reset_request(
            self,
            app_id,
            request_id,
            account_id=None,
            check_access=False,
            check_app=False,
            check_status=False):
        """
        Return extended information about the specified password reset that a
        user has requested for his account.


        :param app_id: identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        :param request_id: identification of the password request.

        :param account_id: identification of the user account on behalf of
            which this function is called.

        :param check_access: indicate whether the function must check if the
            user on behalf of whom the function is called is either the user
            who added this photo.

        :param check_app: indicate whether the function must check if the
            client application on behalf of which the function is called is
            the same than the client application that requested the password
            reset of the user's account.

        :param check_status: indicate whether the function must check the
            current status of this passwor reset request and raise an
            exception if this status is not of enabled.


        :return: an instance containing the following members:

            * `account_id` (required): identification of the user's account
              which the user has requested to reset his password.

            * `app_id` (required): identification of the client application that
              submitted on behalf of the user the request to reset the password
              of his account.

            * `attempt_count` (required): number of times the platform sent an
              email to the user with an embedded link to let this user reset his
              password.

            * `creation_time` (required): time when the user requested to reset
              the password of his account.

            * `request_count` (required): number of times the user requested to
              reset his password before he finally changed it.

            * `request_id` (required): identification of this password reset
              request.

            * `update_time` (required): the most recent time when the platform
              sent an email to the user with an embedded link to let this user
              reset his password.


        :raise `DeletedObjectException`: if the specified password reset
            request has been cancelled by the user or if this request has
            expired.

        :raise `DisabledObjectException`: if the specified password reset
            request has been already used by the user to reset the password
            of his account.

        :raise `IllegalAccessException`: if the client application or the
            user account, on behalf of this function is called, is not allowed
            to retrieve the information of this password reset request.

        :raise `UndefinedObjectException`: if the specified password reset
            request has not been registered on the platform.
        """
        with self.acquire_rdbms_connection(auto_commit=True) as connection:
            # Retrieve the extended information about this password reset request.
            cursor = connection.execute(
                """
                SELECT request_id,
                       account_id,
                       request_count,
                       attempt_count,
                       object_status,
                       creation_time,
                       update_time,
                       app_id
                  FROM account_password_reset
                  WHERE request_id = %(request_id)s
                """,
                {
                    'request_id': request_id
                })
            row = cursor.fetch_one()
            if row is None:
                raise self.UndefinedObjectException()

            request = row.get_object({
                'account_id': cast.string_to_uuid,
                'creation_time': cast.string_to_timestamp,
                'request_id': cast.string_to_uuid,
                'update_time': cast.string_to_timestamp
            })

            # Check whether this password reset request didn't expire, and if so,
            # update its current status.
            if (ISO8601DateTime.now() - request.creation_time).total_seconds() > AccountService.PASSWORD_RESET_REQUEST_LIFESPAN \
               and request.object_status == ObjectStatus.enabled:
                connection.execute(
                    """
                    UPDATE account_password_reset
                      SET object_status = %(OBJECT_STATUS_DISABLED)s,
                          update_time = current_timestamp
                      WHERE request_id = %(request_id)s
                    """,
                    {
                        'OBJECT_STATUS_DISABLED': ObjectStatus.disabled,
                        'request_id': request_id
                    })

                request.object_status = ObjectStatus.diasbled

            # Check whether this password reset request is still valid, and whether
            # the client application and the user account are allowed to access the
            # extended information of this password reset request.
            if check_status:
                if request.object_status == ObjectStatus.diasbled:
                    raise self.DisabledObjectException()
                elif request.object_status == ObjectStatus.deleted:
                    raise self.DeletedObjectException()

            if check_access and account_id and request.account_id != account_id:
                raise self.IllegalAccessException("This password reset request doesn't belong to the specified user")

            if check_app and request.app_id != app_id:
                raise self.IllegalAccessException("The client application is not allowed to retrieve the information of this password reset request")

            return request

    def get_sns_data_deletion(self, app_id, request_id):
        """
        Return information about a request sent to the platform to delete the
        data of auser that an application has collected from the given Social
        Networking Service about this user.


        :param app_id: identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        :param request_id: identification of the data deletion request as
            registered to the platform.


        :return: an instance containing the following attributes:

            * `creation_time` (required): time when the request to delete the data
              of a user has been initiated.

            * `object_status` (required): current status of this data deletion
              request.

            * `request_id` (required): the identification of the data deletion
              request as registered to the platform.

            * `sns_app_id` (required): identification of the application as
              registered to the 3rd party Social Networking Service.

            * `sns_name` (required): code name of the 3rd party Social Networking
              Service.

            * `sns_user_id` (required): identification of the user as registered
              to the 3rd party Social Networking Service.

            * `update_time` (required): time of the most recent update of the
              access token of this user.
        """
        with self.acquire_rdbms_connection(auto_commit=False) as connection:
            cursor = connection.execute(
                """
                SELECT request_id,
                       sns_name,
                       sns_app_id,
                       sns_user_id,
                       object_status,
                       creation_time,
                       update_time 
                  FROM account_sns_data_deletion_request
                  WHERE request_id = %(request_id)s
                """,
                {
                    'request_id': request_id
                })

            row = cursor.fetch_one()
            if row is None:
                raise self.UndefinedObjectException('Undefined SNS data deletion request')

            return row.get_object({
                'creation_time': cast.string_to_timestamp,
                'object_status': ObjectStatus,
                'request_id': cast.string_to_uuid,
                'update_time': cast.string_to_timestamp
            })

    def is_contact_verification_request(self, app_id, name, request_id):
        """
        Indicate whether the specified contact verification request exists.


        :param app_id: identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        :param name: an instance `Contact.ContactName` of the contact that is
            requested to be verified.

        :param request_id: identification of the contact verification request.


        :return: `True` if the specified identification corresponds to a
            contact verification request registered to the platform;
            `False` otherwise.
        """
        return ContactService().is_contact_verification_request(name, request_id)

    def is_username_available(self, app_id, username):
        """
        Indicate whether the specified username is available or not.


        :param app_id: identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        :param username: a username to check whether it is already registered
            by an existing user or not.  A username is unique across the
            platform.  A username is not case sensitive.

        :return: `True` if the username is not registered by any existing
                 account; `False` otherwise.
        """
        with self.acquire_rdbms_connection() as connection:
            cursor = connection.execute(
                """
                SELECT true
                  FROM account
                  WHERE lower(username) = lower(%(username)s)
                    AND object_status = %(OBJECT_STATUS_ENABLED)s
                """,
                {
                    'OBJECT_STATUS_ENABLED': ObjectStatus.enabled,
                    'username': username
                })

            return cursor.get_row_count() == 0

    def request_password_reset(
            self,
            app_id,
            contact,
            connection=None,
            context=None,
            locale=None):
        """
        Request the platform to initiate the process to help the user in
        resetting his password that he has forgotten.

        The function generates a *nonce* ("number used once"), which is a
        pseudo-random number issued to identify the request of the user.  This
        nonce will be sent to the user to his email address, more likely in a
        HTML link that will redirect the end user to a web page responsible
        for allowing the user to reset his password (cf. function
        `change_forgotten_password` that must be passed this *nonce*).

        Note: if the user sends consecutively two requests to reset his
        password within the minimal allowed duration of time (cf. the constant
        `MINIMAL_TIME_BETWEEN_PASSWORD_RESET_REQUEST`), the function ignores the
        new request and returns the identification of the previous request.


        :param app_id: Identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        :param contact: An object `Contact` representing a contact of the user
            who is requesting to reset his forgotten password.

        :param connection: A `RdbmsConnection` instance to be used supporting
            the Python clause `with ...:`.

        :param context: A JSON expression corresponding to the context in
            this contact information has been added and needs to be verified.

        :param locale: A `Locale` instance referencing the preferred language
            of the user that will be used to generate a message to be sent to
            this user.

        :raise DeletedObjectException: If the user account has been deleted.

        :raise DisabledObjectException: If the user account has been disabled.

        :raise InvalidOperationException: If a password reset has already been
           requested recently for this email address.

        :raise UndefinedObjectException: If the specified email address
           doesn't refer to any user account registered against the platform.
        """
        account = self.get_account_by_contact(
            contact,
            check_status=True,
            is_verified=False)

        with self.acquire_rdbms_connection(auto_commit=True, connection=connection) as connection:
            cursor = connection.execute(
                """
                SELECT 
                    request_id,
                    EXTRACT(EPOCH FROM current_timestamp - update_time) AS elapsed_time
                  FROM
                    account_password_reset
                  WHERE
                    account_id = %(account_id)s
                    AND contact_name = %(contact_name)s
                    AND contact_value = %(contact_value)s
                """,
                {
                    'account_id': account.account_id,
                    'contact_name': contact.name,
                    'contact_value': contact.value
                })

            row = cursor.fetch_one()
            request = row and row.get_object({
                'request_id': cast.string_to_uuid
            })

            # Generate a password reset request using this contact information if
            # none has been initiated so far.
            if request is None:
                connection.execute(
                    """
                    INSERT INTO
                        account_password_reset(
                            account_id,
                            app_id,
                            contact_name,
                            contact_value,
                            context,
                            locale)
                      VALUES
                        (%(account_id)s,
                         %(app_id)s,
                         %(contact_name)s,
                         %(contact_value)s,
                         %(context)s,
                         %(locale)s)
                    """,
                    {
                        'account_id': account.account_id,
                        'app_id': app_id,
                        'contact_name': contact.name,
                        'contact_value': contact.value,
                        'context': context,
                        'locale': locale or DEFAULT_LOCALE
                    })

            # If the user has recently requested to reset his password, raise an
            # exception to inform him he needs to wait a little bit more before
            # further attempts.
            elif request.elapsed_time <= AccountService.MINIMAL_TIME_BETWEEN_PASSWORD_RESET_REQUEST:
                raise self.InvalidOperationException("a password reset has already been requested recently")

            # Otherwise, reattempt sending the reset password instruction to the
            # specified contact.
            else:
                connection.execute(
                    """
                    UPDATE 
                        account_password_reset
                      SET
                        update_time = current_timestamp,
                        request_count = request_count + 1
                      WHERE
                        account_id = %(account_id)s
                        AND contact_name = %(contact_name)s
                        AND contact_value = %(contact_value)s
                    """,
                    {
                        'account_id': account.account_id,
                        'contact_name': contact.name,
                        'contact_value': contact.value
                    })

    def request_sns_data_deletion(self, app_id, sns_name, sns_app_id, sns_user_id):
        """
        Request the platform to delete the data of the specified user that an
        application has collected from the given Social Networking Service
        about this user.


        :param app_id: identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        :param sns_name: code name of the 3rd party Social Networking Service.

        :param sns_app_id: identification of the application as registered to
            the 3rd party Social Networking Service.

        :param sns_user_id: identification of the user as registered to the
            3rd party Social Networking Service.


        :return: an instance containing the following attributes:

            * `creation_time` (required): time when this request has been
              registered to the platform.

            * `request_id` (required): identification of the data deletion
              request as registered to the platform.
        """
        with self.acquire_rdbms_connection(auto_commit=True) as connection:
            cursor = connection.execute(
                """
                INSERT INTO 
                    account_sns_data_deletion_request(
                        sns_name,
                        sns_app_id,
                        sns_user_id)
                  VALUES 
                    (lower(%(sns_name)s),
                     %(sns_app_id)s,
                     %(sns_user_id)s)
                  ON CONFLICT (sns_user_id, sns_app_id, sns_name) DO
                    UPDATE
                      SET 
                        object_status = %(OBJECT_STATUS_ENABLED)s,
                        update_time = current_timestamp
                      WHERE
                        account_sns_data_deletion_request.sns_name = EXCLUDED.sns_name
                        AND account_sns_data_deletion_request.sns_app_id = EXCLUDED.sns_app_id
                        AND account_sns_data_deletion_request.sns_user_id = EXCLUDED.sns_user_id
                  RETURNING
                    request_id,
                    creation_time
                """,
                {
                    'OBJECT_STATUS_ENABLED': ObjectStatus.enabled,
                    'sns_app_id': sns_app_id,
                    'sns_name': sns_name,
                    'sns_user_id': sns_user_id
                })

            return cursor.fetch_one().get_object({
                'creation_time': cast.string_to_timestamp,
                'request_id': cast.string_to_uuid,
            })

    def reset_password(self, app_id, request_id, new_password):
        """
        Change the password of the account of a user who forgot his password
        and who requested the platform to reset, as this user cannot login
        into the platform anymore.


        :param app_id: identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        :param request_id: identification of the request of the user to reset
             his forgotten that the function `request_password_reset`
             generated.

        :param new_password: new password of this user's account.


        :raise `DeletedObjectException`: if the specified password reset
            request has been cancelled by the user or if this request has
            expired.

        :raise `DisabledObjectException`: if the specified password reset
            request has been already used by the user to reset the password
            of his account.

        :raise `IllegalAccessException`: if the client application or the
            user account, on behalf of this function is called, is not allowed
            to reset this password.

        :raise InvalidArgumentException: if the new password doesn't conform
            to the rules of password definition.

        :raise `UndefinedObjectException`: if the specified password reset
            request has not been registered on the platform.
        """
        new_password = new_password.strip()
        if not self.REGEX_PASSWORD.match(new_password):
            raise self.InvalidArgumentException('The new password specified does not conform to the rules of the password definition')

        request = self.get_password_reset_request(app_id, request_id, check_status=True)

        with self.acquire_rdbms_connection(auto_commit=True) as connection:
            connection.execute(
                """
                UPDATE account
                  SET password = %(new_password)s,
                      update_time = current_timestamp
                  WHERE account_id = %(account_id)s
                """,
                {
                    'account_id': request.account_id,
                    'new_password': hashlib.md5(new_password.encode()).hexdigest()
                })

            connection.execute(
                """
                UPDATE account_password_reset
                  SET object_status = %(OBJECT_STATUS_DISABLED)s,
                      update_time = current_timestamp
                  WHERE request_id = %(request_id)s
                """,
                {
                    'OBJECT_STATUS_DISABLED': ObjectStatus.disabled,
                    'request_id': request.request_id
                })

    def search_users(
            self,
            full_name,
            account_id=None,
            connection=None,
            limit=BaseRdbmsService.DEFAULT_LIMIT,
            offset=0):
        """
        Search for users providing input text that may correspond to partial
        name, or contact information, such as email address or phone number.


        :param full_name: partial or complete personal name by which the child
            is known.

        :param account_id: identification of the account of the user who is
            requesting this search.

        :param connection: a `RdbmsConnection` instance to be used
            supporting the Python clause `with ...:`.

        :param limit: constrain the number of children to return to the
            specified number.  If not specified, the default value is
            `BaseService.DEFAULT_RESULT_SET_SIZE`.  The maximum value is
            `BaseService.MAXIMUM_RESULT_SET_LIMIT`.

        :param offset: require to skip that many records before beginning to
            return records to the client.  Default value is `0`.  If both
            `offset` and `limit` are specified, then `offset` records
            are skipped before starting to count the limit records that are
            returned.


        :return: an instance containing the following members:

            * `account_id`: identification of the user account.

            * `full_name`: full name of the user.

            * `username`: name of the account of the user, if any defined.

            * `picture_id`: identification of the user account's picture, if any
              picture defined for this user account.

            * `picture_url`: Uniform Resource Locator (URL) that specifies the
              location of the user account's picture, if any defined.  The client
              application can use this URL and append the query parameter `size`
              to specify a given pixel resolution of the user account's picture,
              such as `thumbnail`, `small`, `medium`, `large` (cf.
              `settings.IMAGE_PIXEL_RESOLUTIONS['avatar']`).

            * `locale` (required): a `Locale` instance that identifies the
              preferred language of the user, or English by default.
        """
        if REGEX_PATTERN_EMAIL_ADDRESS.match(full_name):
            return self.get_accounts_by_contacts([ Contact.ContactName.EMAIL, input ])

        if full_name.isdigit():
            return self.get_accounts_by_contacts([ Contact.ContactName.PHONE, input ])

        keywords = self.__string_to_keywords(full_name)

        with self.acquire_rdbms_connection(auto_commit=False, connection=connection) as connection:
            cursor = connection.execute(
                """
                SELECT account_id,
                       full_name,
                       username,
                       picture_id,
                       locale
                  FROM account
                  INNER JOIN (
                      SELECT account_id,
                             COUNT(*) AS score
                        FROM account_index
                        INNER JOIN account
                          USING (account_id)
                        WHERE keyword IN (%[keywords]s)
                          AND (%(account_id)s IS NULL OR account_id <> %(account_id)s)
                          AND object_status IN (%(OBJECT_STATUS_PENDING)s, %(OBJECT_STATUS_ENABLED)s) 
                          GROUP BY account_id) AS foo
                  USING (account_id)
                  ORDER BY score DESC,
                           account_id DESC -- @hack: to preserve order of accounts with same score from an offset to anoth
                  LIMIT %(limit)s
                  OFFSET %(offset)s
                """,
                {
                    'OBJECT_STATUS_ENABLED': ObjectStatus.enabled,
                    'OBJECT_STATUS_PENDING': ObjectStatus.pending,
                    'account_id': account_id,
                    'keywords': keywords,
                    'limit': min(limit, self.MAXIMUM_LIMIT) or self.MAXIMUM_LIMIT,
                    'offset': offset
                })

            accounts = [
                row.get_object({
                    'account_id': cast.string_to_uuid,
                    'locale': Locale,
                    'picture_id': cast.string_to_uuid})
                for row in cursor.fetch_all()]

            for account in accounts:
                account.picture_url = self.build_picture_url(account.picture_id)

            return accounts

    def set_full_name(self, app_id, account_id, full_name):
        """
        Update the complete full_name of a user.


        :param app_id: identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        :param account_id: identification of the user's account.

        :param full_name: complete full name of the user as given by the user
            himself, i.e., untrusted information.


        :return: an instance containing the following members:

            * `account_id` (required): identification of the user's account.

            * `full_name` (required): the new complete full name of the user as
              given by the user himself.

            * `update_time` (required): time of the most recent modification of
              the properties of the user's account.


        :raise DeletedObjectException: if the user's account has been deleted.

        :raise DisabledObjectException: if the user's account has been
            disabled.

        :raise Undefined ObjectException: if the specified identification
            doesn't refer to a user account registered to the platform.
        """
        with self.acquire_rdbms_connection(auto_commit=True) as connection:
            cursor = connection.execute(
                """
                UPDATE
                    account
                  SET
                    full_name = %(full_name)s,
                    update_time = current_timestamp
                  WHERE
                    account_id = %(account_id)s
                  RETURNING
                    account_id,
                    full_name,
                    object_status,
                    update_time
                """,
                {
                    'account_id': account_id,
                    'full_name': full_name.strip()
                })
            row = cursor.fetch_one()
            if row is None:
                raise self.UndefinedObjectException()

            account = row.get_object({
                'account_id': cast.string_to_uuid,
                'update_time': cast.string_to_timestamp
            })

            if account.object_status == ObjectStatus.disabled:
                raise self.DisabledObjectException()
            elif account.object_status == ObjectStatus.deleted:
                raise self.DeletedObjectException()

            del account.object_status

            # Re-index this account with this new full_name.
            self.__index_account(account_id, full_name)

            return account

    def sign_in_with_username(self, app_id, username, password):
        """
        Sign-in the user against the platform providing a username and a
        password.


        :param app_id: identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        :param username: the username of the user account.

        :param password: the password of the user account.


        :return: a session instance containing the following members:
                 * `account_id`: identification of the account of the user.
                 * `expiration_time`: time when the login session will
                   expire.
                 * `session_id`: identification of the login session of the
                   user.


        :raise DeletedObjectException: if the user account has been deleted.

        :raise DisabledObjectException: if the user account has been disabled.

        :raise AuthenticationFailureException: if the given username and/or
               password don't match any account registered against the
               platform.
        """
        with self.acquire_rdbms_connection() as connection:
            cursor = connection.execute(
                """
                SELECT account_id,
                       password,
                       object_status
                  FROM account
                  WHERE lower(username) = lower(%(username)s)
                  """,
                {
                    'OBJECT_STATUS_ENABLED': ObjectStatus.enabled,
                    'username': username.strip()
                })
            row = cursor.fetch_one()
            if row is None:
                # @note: do not inform that no user has been registered with this
                # username, which might be sensitive information.
                raise self.AuthenticationFailureException()

            account = row.get_object({ 'account_id': cast.string_to_uuid })
            if account.object_status == ObjectStatus.disabled:
                raise self.DisabledObjectException('This user account has been disabled')
            elif account.object_status == ObjectStatus.deleted:
                raise self.DeletedObjectException('This user account has been deleted')
            elif hashlib.md5(password.encode()).hexdigest() != account.password:
                raise self.AuthenticationFailureException()

        return SessionService().create_session(app_id, account.account_id)

    def sign_in_with_contact(
            self,
            app_id,
            contact,
            password,
            allow_unverified_contact=True,
            connection=None,
            session_duration=None):
        """
        Sign-in the user against the platform providing a contact information,
        such as an email address or a phone number, and a password.


        :param app_id: identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        :param contact: a tuple composed of 2 items representing a contact
            information of a registered:

            * `name`: item of the enumeration `Contact.ContactName`.

            * `value`: value of this contact information

        :param password: the password of the user account.

        :param allow_unverified_contact: indicate whether the user is allowed
            to sign-in with a contact not yet verified.

        :param connection: An `RdbmsConnection` object supporting the Python
            clause `with ...:`.

        :param session_duration: Login session duration, expressed in
            seconds, corresponding to the interval of time between the
            creation of the token and the expiration of this login session.


        :return: a session instance containing the following members:

            * `account_id`: identification of the account of the user.

            * `expiration_time`: time when the login session will expire.

            * `full_name`: complete full name of the user as given by the user
              himself, i.e., untrusted information, or as determined from his
              email address as for a ghost account.

            * `is_verified`: indicate whether this contact information has been
              verified, whether it has been grabbed from a trusted Social
              Networking Service (SNS), or whether through a challenge/response
              process.  The user should be reminded to confirm his contact
              information if not already verified, or the user would take the
              chance to have his account suspended.

            * `is_primary`: indicate whether this contact information is the
              primary one for the given property.

            * `session_id`: identification of the login session of the user.

            * `username`: also known as screen name or nickname, username is
              chosen by the end user to identify himself when accessing the
              platform and communicating with others online.  A username should be
              totally made-up pseudonym, not reveal the real name of the person.
              The username is unique across the platform.  A username is not case
              sensitive.


        :raise AuthenticationFailureException: If the given contact
            information and/or password don't match any account registered
            against the platform.

        :raise DeletedObjectException: If the user account has been deleted.

        :raise DisabledObjectException: If the user account has been disabled.

        :raise UnverifiedContactException: If the contact of this user has not
            been verified yet, while the parameter `allow_unverified_contact`
            has been passed with the value `False`.
        """
        with self.acquire_rdbms_connection(auto_commit=True, connection=connection) as connection:
            # Retrieve the identification of the user account corresponding to this
            # contact information, including the hashed version of its password as
            # the method `get_account` doesn't return it for security reason.
            cursor = connection.execute(
                """
                SELECT 
                    account_id,
                    password,
                    is_primary,
                    is_verified
                  FROM
                    account_contact
                  INNER JOIN account
                    USING (account_id)
                  WHERE
                    name = %(name)s
                    AND lower(value) = lower(%(value)s)
                    AND account_contact.object_status = %(OBJECT_STATUS_ENABLED)s
                """,
                {
                    'OBJECT_STATUS_ENABLED': ObjectStatus.enabled,
                    'name': contact.name,
                    'value': contact.value.strip()
                })
            row = cursor.fetch_one()
            if row is None:
                # @note: do not inform that no user has been registered with this
                #     contact information, which might be sensitive information.
                raise self.AuthenticationFailureException()

            account_contact = row.get_object({
                'account_id': cast.string_to_uuid,
                'object_status': ObjectStatus
            })

            if not account_contact.is_verified and not allow_unverified_contact:
                raise self.UnverifiedContactException('This contact information has not been verified yet')

            account = self.get_account(account_contact.account_id, check_status=True)

            if hashlib.md5(password.encode()).hexdigest() != account_contact.password:
                raise self.AuthenticationFailureException()

            session = SessionService().create_session(
                app_id,
                account.account_id,
                connection=connection,
                session_duration=session_duration)

            session.is_primary = account_contact.is_primary
            session.is_verified = account_contact.is_verified
            session.__dict__.update(account.__dict__)

        return session

    def sign_out(self, app_id, session):
        """
        Sign out the specified user from his login session.


        :param app_id: Identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        :param session: An object containing the following attributes:

            * `account_id` (required): Identification of the account of the a user.

            * `session_id` (required): Identification of the user's session.


        :raise IllegalAccessException: If the specified login session doesn't
            belong to the specified user.

        :raise UndefinedObjectException: If the specified identification
            doesn't refer to any user login session registered against the
            platform.
        """
        SessionService().drop_session(app_id, session)

    def sign_up(
            self,
            account_type=AccountType.standard,
            action_type=None,
            app_id=None,
            auto_sign_in=False,
            bypass_recaptcha=True,
            connection=None,
            contact=None,
            context=None,
            deriving_table_name=None,
            enable_account=True,
            full_name=None,
            has_been_verified=False,
            password=None,
            locale=None,
            recaptcha=None,
            set_pending_if_unverified_contact=False,
            to_be_verified=False,
            username=None):
        """
        Register a new user account to the platform.

        A user account is identified by a contact or/and a username, except
        account that is created from a 3rd-party Social Networking Service
        (SNS), in which case contacts and username are optional.

        A password is mandatory except for botnet, ghost, and SNS user
        accounts.

        The specified contact CANNOT be already registered and verified by
        another user account.

        If the specified contact has been already registered but not verified
        yet, the function doesn't create a new account but returns the user
        account which this contact is associated to.


        :param app_id: identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        :param account_type: an item of `AccountService.AccountType` that
            describes the context that caused the registration of this user
            account.

        :param action_type: indicate the type of the action that initiates
            the request for verifying the specified contact information.

        :param contact: an instance `Contact`.

        :param context: a JSON expression corresponding to the context in
            which this contact has been added and need to be verified.

        :param deriving_table_name: Name of the table, deriving from the base
            table `account`, in which to insert the information of the account
            of the user to create.

        :param username:  a name used to gain access to a the platform.  The
            username MUST be unique among all the usernames already registered
            by other users to the platform.  This argument is optional if and
            only if contact information has been passed.

        :param password: password associated to the user account.  A password
            is required if the parameter `set_enabled` is `True`.

        :param full_name: complete full name of the user.

        :param locale: a `Locale` instance referencing the preferred
            language of the user.

        :param auto_signin: indicate whether the platform is requested to
            sign-in this user once the sign-up procedure completes
            successfully.

        :param enable_account: indicate whether this user account is immediately
            enabled, or whether it needs to be flagged as pending until the
            user takes some action, such as, for instance, confirming his
            contact information.

        :param set_pending_if_unverified_contact: indicate whether to set the
            account of this user in a pending status if the specified contact
            information has not been verified.

        :param to_be_verified: indicate whether the platform needs to send a
            request to the user to verify his contact information.  This
            argument cannot be set to `True` if the argument `has_been_verified`
            has been set to `True`.


        :return: an instance containing the following attributes:

            * `account_id` (required): identification of the account of the
              user.

            * `creation_time` (required): time when this account has been
              registered.  This information should be stored by the client
              application to manage its cache of accounts.

            * `expiration_time` (optional): time when the login session will
              expire.  This information is provided if the client application
              requires the platform to automatically sign-in the user (cf.
              parameter `auto_sigin`).

            * `locale` (required): an instance `Locale` specifying the preferred
              language of the user.


            * `object_status` (required): current status of this user account.

            * `session_id` (optional): identification of the login session of
              the user.  This information is provided if the client application
              requires the platform to automatically sign-in the user (cf.
              parameter `auto_sigin`).


        :raise ContactAlreadyUsedException: if one or more contacts are
            already associated and verified for a user account.

        :raise InvalidArgumentException: if one or more arguments are not
            compliant with their required format, if some required information
            is missing.

        :raise UsernameAlreadyUsedException: if the specified username is
            already associated with an existing user account.
        """
        if account_type not in AccountService.AccountType:
            raise self.InvalidArgumentException('Unsupported type "%s" of user account' % str(account_type))

        # A user name must be provided when the given contact information has
        # not be verified.  The reason is if another user provides the same
        # contact information and he passes the verification challenge, this
        # identification will be reallocated to this second user account,
        # meaning that the first user won't have any more identification to
        # sign-in to the platform.
        if not username and not contact and account_type not in [ AccountService.AccountType.sns, AccountService.AccountType.ghost ]:
            raise self.InvalidArgumentException('A username and/or a contact information MUST be provided')

        if username:
            username = username.strip().lower()
            if not self.is_username_available(app_id, username):
                raise self.UsernameAlreadyUsedException('This username is already associated with an existing user account')

        if password is None and enable_account and account_type not in [
                AccountService.AccountType.sns,
                AccountService.AccountType.ghost,
                AccountService.AccountType.botnet ]:
            raise self.InvalidArgumentException('A password is required for registering a user account')

        if password:
            password = password.strip()
            if not AccountService.REGEX_PASSWORD.match(password):
                raise self.InvalidArgumentException('The password is of an invalid format')
            password = hashlib.md5(password.encode()).hexdigest()

        if full_name:
            full_name = full_name.strip()
            if len(full_name) == 0:
                full_name = None

        # The creation of a user account requires to pass a reCAPTCHA
        # challenge, except under the following conditions:
        #
        # * The function is explicitly requested to bypass the reCAPTCHA
        #   challenge, which option is useful for internal service usage only,
        #   when creating a new user account who authenticates with
        #   credentials on trusted 3rd party platforms, such as an OAuth
        #   access token.
        # * The environment stage of the platform is development or
        #   integration.
        # * The user account to be created is either a botnet or a test
        #   account.
        if recaptcha:
            (recaptcha_private_key, client_ip_address, recaptcha_challenge, recaptcha_response) = recaptcha
            if not recaptcha.verify(recaptcha_private_key, client_ip_address, recaptcha_challenge, recaptcha_response):
                raise self.IllegalAccessException('Incorrect reCAPTCHA response')

        with self.acquire_rdbms_connection(
                auto_commit=True,
                connection=connection) as connection:

            # # Register the account with the provided information.
            # account_status = ObjectStatus.enabled if (set_enabled and (not set_pending_if_unverified_contact or verified_contacts)) \
            #         else ObjectStatus.pending

            cursor = connection.execute(
                f"""
                INSERT INTO {deriving_table_name or 'account'}(
                    full_name,
                    username,
                    password,
                    locale,
                    account_type,
                    object_status,
                    app_id)
                  VALUES 
                    (%(full_name)s,
                    %(username)s,
                    %(password)s,
                    %(locale)s,
                    %(account_type)s,
                    %(object_status)s,
                    %(app_id)s)
                  RETURNING 
                    account_id,
                    locale,
                    object_status,
                    creation_time
                """,
                {
                    'account_type': account_type,
                    'app_id': app_id,
                    'full_name': full_name,
                    'locale': locale or DEFAULT_LOCALE,
                    'object_status': ObjectStatus.enabled if enable_account else ObjectStatus.pending,
                    'password': password,
                    'username': username
                })

            account = cursor.fetch_one().get_object({
                'account_id': cast.string_to_uuid,
                'creation_time': cast.string_to_timestamp,
                'locale': cast.string_to_locale })

            # Index the user with his full_name.
            if full_name and account_type in [
                AccountService.AccountType.standard,
                AccountService.AccountType.sns,
                AccountService.AccountType.ghost
            ]:
                self.__index_account(account.account_id, full_name)

            # Add the specified contact to the user account.
            if contact:
                ContactService().add_contact(
                    account.account_id,
                    contact,
                    # action_type=action_type,
                    connection=connection,
                    context=context,
                    has_been_verified=has_been_verified,
                    locale=locale,
                    to_be_verified=to_be_verified)

            if auto_sign_in:
                account_session = SessionService().create_session(
                    app_id,
                    account.account_id,
                    connection=connection)

                account_session.creation_time = account.creation_time
                account_session.locale = account.locale
                account_session.object_status = account.object_status

        return account_session if auto_sign_in else account

    @classmethod
    def store_picture_image_file(
            cls,
            picture_id,
            image,
            image_file_format=DEFAULT_IMAGE_FILE_FORMAT,
            image_quality=DEFAULT_IMAGE_QUALITY):
        """
        Store the image data of the avatar/photo of an account to the temporary
        directory of the local Network File System (NFS).  This file will be
        read by background tasks for additional processing.

        :param picture_id: The identification of the photo of a user account.

        :param image: An object `PIL.Image`.

        :param image_file_format: Image file format to store the image with
            (cf. https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).

        :param image_quality: The image quality to store locally, on a scale from `1`
            (worst) to `95` (best).  Values above `95` should be avoided; `100`
            disables portions of the JPEG compression algorithm, and results
            in large files with hardly any gain in image quality.


        :return: The absolute file path name of the photo image stored in the
            local Network File System (NFS)
        """
        # Create the path of the folder to store the image file in.
        path = os.path.join(
            settings.CDN_NFS_ROOT_PATH,
            cls.CDN_BUCKET_NAME_AVATAR,
            file_util.build_tree_pathname(str(picture_id)))

        file_util.make_directory_if_not_exists(path)

        # Define the name and the extension of the image file to create.
        if not image_file_format:
            image_file_format = DEFAULT_IMAGE_FILE_FORMAT

        file_extension = DEFAULT_IMAGE_FILE_FORMAT_EXTENSIONS.get(image_file_format, image_file_format)
        file_path_name = os.path.join(path, f'{str(picture_id)}.{file_extension}')

        # Save the image with the specified format in its folder.
        image.save(
            file_path_name,
            format=DEFAULT_IMAGE_FILE_FORMAT,
            quality=image_quality or DEFAULT_IMAGE_QUALITY)

        return file_path_name

    def set_avatar_status(
            self,
            picture_id,
            object_status,
            connection=None):
        # Update the status of the account's picture.
        with self.acquire_rdbms_connection(auto_commit=True, connection=connection) as connection:
            cursor = connection.execute(
                """
                UPDATE 
                    account_picture
                  SET 
                    object_status = %(object_status)s,
                    update_time = current_timestamp
                  WHERE
                    account_id = %(account_id)s
                    AND object_status NOT IN (%(object_status)s, %(OBJECT_STATUS_DELETED)s)
                  RETURNING
                    account_id,
                    picture_id,
                    update_time
                """,
                {
                    'OBJECT_STATUS_DELETED': ObjectStatus.deleted,
                    'object_status': object_status,
                    'picture_id': picture_id
                })

            # Retrieve the updated information of this picture.
            row = cursor.fetch_one()
            if row is None:
                raise self.UndefinedObjectException(f"Undefined or unchanged status of picture {picture_id}")

            picture = row.get_object({
                'account_id': cast.string_to_uuid,
                'picture_id': cast.string_to_uuid,
                'update_time': cast.string_to_timestamp
            })

            # If a picture other than the one currently active is enabled, replace
            # the latter with the picture passed to this function.
            if object_status == ObjectStatus.enabled:
                connection.execute(
                    """
                    UPDATE 
                        account
                      SET 
                        picture_id = %(picture_id)s,
                        update_time = current_timestamp
                      WHERE
                        account_id = %(account_id)s
                    """,
                    {
                        'account_id': picture.account_id,
                        'picture_id': picture_id
                    })

                connection.execute(
                    """
                    UPDATE 
                        account_picture
                      SET 
                        object_status = %(OBJECT_STATUS_DISABLED)s,
                        update_time = current_timestamp
                      WHERE
                        account_id = %(account_id)s
                        AND object_status = %(OBJECT_STATUS_ENABLED)s)
                    """,
                    {
                        'OBJECT_STATUS_DISABLED': ObjectStatus.disabled,
                        'OBJECT_STATUS_ENABLED': ObjectStatus.enabled,
                        'account_id': picture.account_id
                    })

            return picture

    def upload_avatar(
            self,
            app_id,
            account_id,
            uploaded_file,
            connection=None):
        """
        Upload a new picture of this user account, also known as the avatar,
        which is the graphical representation of the user.


        :param app_id: identification of the client application such as a Web,
            a desktop, or a mobile application, that accesses the service.

        :param account_id: identification of the account of the user on behalf
            of whom the picture files are added to the platform.

        :param uploaded_file: an instance `HttpRequest.HttpRequestUploadedFile`.

        :param connection: a `RdbmsConnection` instance to be used
            supporting the Python clause `with ...:`.


        :return: an instance containing the following members:

            * `file_name` (required): the original local file name as the
            `filename` parameter of the `Content-Disposition` header.

            * `picture_id` (required): identification of the new avatar of the
                user's account as registered to the platform.

            * `picture_url` (required): Uniform Resource Locator (URL) that
              specifies the location of the user's avatar.  The client application
              can use this URL and append the query parameter `size` to specify
              a given pixel resolution of the photo, such as `thumbnail`,
              `small`, `medium`, or `large`.

            * `update_time` (required): time of the most recent modification of
              the properties of the user's account.  This information should be
              stored by the client application to manage its cache of user
              accounts.


        :raise DeletedObjectException: if the user's account has been deleted.

        :raise DisabledObjectException: if the user's account has been
            disabled.

        :raise InvalidOperationException: if the format of the uploaded image
            is not supported.

        :raise UndefinedObjectException: if the specified identification
            doesn't refer to a user account registered to the platform.
        """
        # Retrieve the pixel resolution of the photo image, and check whether
        # it respects the minimal size required.  If not, ignore this photo.
        try:
            string_io_stream = io.BytesIO(uploaded_file.data)
            image = image_util.convert_image_to_rgb_mode(Image.open(string_io_stream))
            image_width, image_height = image.size
        except:
            import traceback
            traceback.print_exc()
            raise self.InvalidOperationException("Unsupported image file format")

        # Store the watermark file in the temporary directory of the local
        # Network File System (NFS).  This file will be read by background task
        # for additional processing.
        with self.acquire_rdbms_connection(auto_commit=True, connection=connection) as connection:
            # Register the new avatar of the user's account.
            picture_id = uuid.uuid1()

            cursor = connection.execute(
                """
                UPDATE 
                    account
                  SET
                    picture_id = %(picture_id)s,
                    update_time = current_timestamp
                  WHERE
                    account_id =%(account_id)s
                  RETURNING
                    account_id,
                    picture_id,
                    object_status,
                    update_time
                """,
                {
                    'account_id': account_id,
                    'picture_id': picture_id
                })
            row = cursor.fetch_one()
            if row is None:
                raise self.UndefinedObjectException("The user account is not registered to the platform")

            # Retrieve the properties of the avatar to return to the client
            # application.
            account_avatar = row.get_object({
                'account_id': cast.string_to_uuid,
                'picture_id': cast.string_to_uuid,
                'update_time': cast.string_to_timestamp
            })

            if account_avatar.object_status == ObjectStatus.disabled:
                raise self.DisabledObjectException()
            elif account_avatar.object_status == ObjectStatus.deleted:
                raise self.DeletedObjectException()

            del account_avatar.object_status

            # Complete the properties of the watermark.
            account_avatar.picture_url = os.path.join(
                settings.CDN_URL_HOSTNAME,
                self.CDN_BUCKET_NAME_AVATAR,
                str(account_avatar.picture_id))
            account_avatar.file_name = uploaded_file.file_name

            # Store the image file of the avatar to the platform's CDN.
            picture_path_name = os.path.join(
                settings.CDN_NFS_ROOT_PATH,
                self.CDN_BUCKET_NAME_AVATAR,
                file_util.build_tree_pathname(str(picture_id)))

            file_util.make_directory_if_not_exists(picture_path_name)

            with open(os.path.join(picture_path_name, str(picture_id)), 'wb') as handle:
                handle.write(uploaded_file.data)

            # Generate multiple resolutions of the photo for various client
            # applications' usages.
            for (logical_size, scaled_image) in \
                    image_util.generate_multiple_pixel_resolutions(
                        image, settings.IMAGE_PIXEL_RESOLUTIONS['avatar'],
                        does_crop=True,
                        filter=image_util.Filter.AntiAlias):
                scaled_image.save(
                    os.path.join(
                        settings.CDN_NFS_ROOT_PATH,
                        self.CDN_BUCKET_NAME_AVATAR,
                        file_util.build_tree_file_pathname(f'{picture_id}_{logical_size}.jpg')),
                    'JPEG', quality=75)

        return account_avatar
