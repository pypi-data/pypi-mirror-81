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

from majormode.perseus.constant.contact import ContactName
from majormode.perseus.constant.http import HttpMethod
from majormode.perseus.model.contact import Contact
from majormode.perseus.model.locale import DEFAULT_LOCALE
from majormode.perseus.model.obj import Object
from majormode.perseus.service.base_http_handler import HttpRequest
from majormode.perseus.service.base_http_handler import HttpRequestHandler
from majormode.perseus.service.base_http_handler import http_request
from majormode.perseus.service.account.contact_service import ContactService
from majormode.perseus.service.account.account_service import AccountService
from majormode.perseus.utils import cast


class AccountServiceHttpRequestHandler(HttpRequestHandler):
    @http_request(
        r'^/account/contact/(name)/availability$',
        http_method=HttpMethod.GET,
        authentication_required=False)
    def is_contact_available(self, request, name):
        value = request.get_argument(
            'value',
            data_type=HttpRequest.ArgumentDataType.string,
            is_required=True)

        contact = Contact(cast.string_to_enum(name.upper(), ContactName), value)
        is_available, is_verified = ContactService().is_contact_available(contact)

        return Object(is_available=is_available, is_verified=is_verified)

    # @http_request(
    #     r'^/account/password/reset/request$',
    #     http_method=HttpMethod.POST,
    #     authentication_required=False)
    # def request_password_reset(self, request):
    #     email_address = request.get_argument(
    #         'email_address',
    #         data_type=HttpRequest.ArgumentDataType.string,
    #         is_required=True)
    #
    #     return AccountService().request_password_reset(request.app_id, Contact(ContactName.EMAIL, email_address))





























































    # @http_request(
    #     r'^/account/password$',
    #     http_method=HttpMethod.PUT,
    #     authentication_required=True)
    # def change_password(self, request):
    #     old_password = request.get_argument('old_password')
    #     new_password = request.get_argument('new_password')
    #     return AccountService().change_password(request.app_id, request.account_id, old_password, new_password)
    #
    # @http_request(r'^/account$',
    #               http_method=HttpMethod.GET,
    #               authentication_required=False)
    # def get_accounts(self, request):
    #     account_id_list = request.get_argument('ids',
    #             data_type=HttpRequest.ArgumentDataType.list,
    #             item_data_type=HttpRequest.ArgumentDataType.uuid,
    #             is_required=False)
    #
    #     include_pending = request.get_argument('include_pending',
    #             data_type=HttpRequest.ArgumentDataType.boolean,
    #             is_required=False,
    #             default_value=False)
    #
    #     start_time = request.get_argument('start_time',
    #             data_type=HttpRequest.ArgumentDataType.timestamp,
    #             is_required=False)
    #
    #     if account_id_list is None:
    #         account_id_list = request.get_argument('emails',
    #                 data_type=HttpRequest.ArgumentDataType.list)
    #
    #     return AccountService().get_accounts(request.app_id, account_id_list,
    #             account_id=request.account_id,
    #             include_pending=include_pending,
    #             start_time=start_time)
    #
    # @http_request(
    #     r'/account/contact/verification/(request_id:uuid)$',
    #     http_method=HttpMethod.GET,
    #     authentication_required=False)
    # def get_contact_verification_request(self, request, request_id):
    #     return ContactService().get_contact_verification_request(request_id)
    #
    # @http_request(
    #     r'^/account/password/reset/request/(request_id:uuid)$',
    #     http_method=HttpMethod.GET,
    #     authentication_required=False)
    # def get_password_reset_request(self, request, request_id):
    #     check_access = request.get_argument('check_access',
    #             data_type=HttpRequest.ArgumentDataType.boolean,
    #             is_required=False,
    #             default_value=False)
    #
    #     check_app = request.get_argument('check_app',
    #             data_type=HttpRequest.ArgumentDataType.boolean,
    #             is_required=False,
    #             default_value=False)
    #
    #     check_status = request.get_argument('check_status',
    #             data_type=HttpRequest.ArgumentDataType.boolean,
    #             is_required=False,
    #             default_value=False)
    #
    #     return AccountService().get_password_reset_request(request.app_id, request_id,
    #             account_id=request.account_id,
    #             check_access=check_access,
    #             check_app=check_app,
    #             check_status=check_status)
    #
    # @http_request(
    #     r'^/account/sns/deletion/request/(request_id:uuid)$',
    #     http_method=HttpMethod.GET,
    #     authentication_required=False)
    # def get_sns_data_deletion(self, request, request_id):
    #     return AccountService().get_sns_data_deletion(request.app_id, request_id)
    #
    # @http_request(
    #     r'^/account/username/availability$',
    #     http_method=HttpMethod.POST,
    #     authentication_required=False)
    # def is_username_available(self, request):
    #     username = request.get_argument('value',
    #             data_type=HttpRequest.ArgumentDataType.string,
    #             is_required=True)
    #
    #     return AccountService().is_username_available(request.app_id, username)
    #
    # @http_request(
    #     r'^/account/(name)/verification/(request_id:uuid)$',
    #     http_method=HttpMethod.GET,
    #     authentication_required=False)
    # def is_contact_verification_request(self, request, name, request_id):
    #     return AccountService().is_contact_verification_request(
    #         request.app_id,
    #         cast.string_to_enum(name.upper(), ContactName),
    #         request_id)
    #
    # @http_request(
    #     r'/account/sns/deletion/request$',
    #     http_method=HttpMethod.POST,
    #     authentication_required=False)
    # def request_sns_data_deletion(self, request):
    #     sns_name = request.get_argument(
    #         'sns_name',
    #         data_type=HttpRequest.ArgumentDataType.string,
    #         is_required=True)
    #
    #     sns_app_id = request.get_argument(
    #         'sns_app_id',
    #         data_type=HttpRequest.ArgumentDataType.string,
    #         is_required=True)
    #
    #     sns_user_id = request.get_argument(
    #         'sns_user_id',
    #         data_type=HttpRequest.ArgumentDataType.string,
    #         is_required=True)
    #
    #     return AccountService().request_sns_data_deletion(request.app_id, sns_name, sns_app_id, sns_user_id)
    #
    # @http_request(
    #     r'^/account/password/reset$',
    #     http_method=HttpMethod.POST,
    #     authentication_required=False)
    # def reset_password(self, request):
    #     request_id = request.get_argument('request_id')
    #     new_password = request.get_argument('new_password')
    #     return AccountService().reset_password(request.app_id, request_id, new_password)
    #
    # @http_request(
    #     r'^/account/full_name$',
    #     http_method=HttpMethod.PUT,
    #     authentication_required=True,
    #     sensitive_data=True)
    # def set_full_name(self, request):
    #     full_name = request.get_argument(
    #         'full_name',
    #         data_type=HttpRequest.ArgumentDataType.string,
    #         is_required=True)
    #     return AccountService().set_full_name(request.app_id, request.account_id, full_name)
    #
    # @http_request(
    #     r'^/account/avatar$',
    #     http_method=HttpMethod.PUT,
    #     authentication_required=True,
    #     signature_required=True)
    # def upload_avatar(self, request):
    #     if len(request.uploaded_files) != 1:
    #         raise AccountService.IllegalOperationException("One and only one avatar image MUST be uploaded")
    #
    #     return AccountService().upload_avatar(request.app_id, request.account_id, request.uploaded_files[0])

    # @deprecated: the sign-in method should not be surfaced as it is
    # generally customised by each online service inheriting from the
    # Perseus server platform's code base.
    #
    # @http_request(r'^/account/session$',
    #               http_method=HttpMethod.POST,
    #               authentication_required=False,
    #               sensitive_data=True)
    # def sign_in(self, request):
    #     provider_name = request.get_argument('provider_name', is_required=False)
    #
    #     # If no OAuth 2 Service Provider identification is passed along the
    #     # HTTP request, then perform the sign in of the user using the
    #     # explicit method with the credentials that are passed along the HTTP
    #     # request, i.e., the email address and the password of the user.
    #     if provider_name is None:
    #         email_address = request.get_argument('email_address')
    #         password = request.get_argument('password')
    #         return AccountService().sign_in_with_contact(request.app_id, ('EMAIL', email_address), password)
    #
    #     # When OAuth 2 Service Provider identification is passed along the
    #     # HTTP request, then perform the sign in of the user using the
    #     # implicit method with Open Authorization (OAuth).
    #     else:
    #         user_id = request.get_argument('user_id')
    #         access_token = request.get_argument('access_token')
    #         return AccountService().sign_in_with_oauth(request.app_id, provider_name, user_id, access_token)
    #

    # @deprecated: need to be implement by the custom server application.
    # @http_request(r'^/account/session$',
    #               http_method=HttpMethod.DELETE,
    #               authentication_required=True)
    # def sign_out(self, request):
    #     return AccountService().sign_out(request.app_id, request.account_id, request.session.session_id)


    # @deprecated: the sign-up method should not be surfaced as it is
    # generally customised by each online service inheriting from the
    # Perseus server platform's code base.
    #
    # @http_request(r'^/account$',
    #               http_method=HttpMethod.POST,
    #               authentication_required=False)
    # def sign_up(self, request):
    #     auto_sign_in = request.get_argument('auto_sign_in',
    #             argument_passing=HttpRequest.ArgumentPassing.query_string,
    #             data_type=HttpRequest.ArgumentDataType.boolean,
    #             is_required=False,
    #             default_value=False)
    #
    #     provider_name = request.get_argument('provider_name',
    #             is_required=False)
    #
    #     # If no OAuth 2 Service Provider identification is passed along the
    #     # HTTP request, then perform the sign up of the user using the
    #     # explicit method with the credentials that are passed along the HTTP
    #     # request, i.e., the email address and the password of the user.
    #     #
    #     # @note: on environment stages other than development, the user is
    #     # required to provide a succeeded reCAPTCHA challenge.
    #     if provider_name is None:
    #         contacts = request.get_argument('contacts',
    #                 data_type=HttpRequest.ArgumentDataType.list,
    #                 is_required=False)
    #
    #         if contacts:
    #             try:
    #                 contacts = [ (cast.string_to_enum(contact[0], AccountService.ContactPropertyName),
    #                               contact[1],
    #                               contact[2] if len(contact) == 3 else True)
    #                         for contact in contacts ]
    #             except:
    #                 raise AccountService.InvalidArgumentException('Invalid contact information')
    #
    #         password = request.get_argument('password',
    #                 data_type=HttpRequest.ArgumentDataType.string,
    #                 is_required=True)
    #
    #         full_name = request.get_argument('full_name',
    #                 data_type=HttpRequest.ArgumentDataType.list,
    #                 is_required=False)
    #
    #         account_type = request.get_argument('account_type',
    #                 data_type=HttpRequest.ArgumentDataType.enumeration,
    #                 enumeration=AccountService.AccountType,
    #                 default_value = AccountService.AccountType.standard,
    #                 is_required=False)
    #
    #         locale = request.get_argument('locale',
    #                 data_type=HttpRequest.ArgumentDataType.locale,
    #                 default_value=DEFAULT_LOCALE,
    #                 is_required=False)
    #
    #         recaptcha_parameters = request.get_argument('recaptcha',
    #                 data_type=HttpRequest.ArgumentDataType.dictionary,
    #                 default_value=dict(),
    #                 is_required=False)
    #         if recaptcha_parameters:
    #             recaptcha_private_key = recaptcha_parameters.get('private_key')
    #             recaptcha_challenge = recaptcha_parameters.get('challenge')
    #             recaptcha_response = recaptcha_parameters.get('response')
    #
    #         return AccountService().sign_up(app_id=request.app_id,
    #                 account_type=account_type,
    #                 contacts=contacts,
    #                 full_name=full_name,
    #                 password=password,
    #                 locale=locale,
    #                 recaptcha=recaptcha_parameters and (recaptcha_private_key, request.client_ip_address, recaptcha_challenge, recaptcha_response),
    #                 auto_sign_in=auto_sign_in)

#         # When OAuth 2 Service Provider identification is passed along the
#         # HTTP request, then perform the sign up of the user using the
#         # implicit method with Open Authorization (OAuth).
#         else:
#             #user_id = request.get_argument('user_id')
#             #oauth_consumer_key = request.get_argument('oauth_consumer_key')
#             #oauth_consumer_secret = request.get_argument('oauth_consumer_secret')
#             access_token = request.get_argument('access_token',
#                 is_required=True)
#
#             locale = request.get_argument('locale', is_required=False, default_value=DEFAULT_LOCALE,
#                 data_type=HttpRequest.ArgumentDataType.locale)
#
#             return AccountService().sign_up_with_oauth(request.app_id, provider_name, access_token,
#                 #user_id, oauth_consumer_key, oauth_consumer_secret, access_token,
#                 locale=locale,
#                 auto_sign_in=auto_sign_in)
