# -*- coding: utf-8 -*-

#  Copyright (c) 2017 SHIELD, UBIWHERE
# ALL RIGHTS RESERVED.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Neither the name of the SHIELD, UBIWHERE nor the names of its
# contributors may be used to endorse or promote products derived from this
# software without specific prior written permission.
#
# This work has been performed in the framework of the SHIELD project,
# funded by the European Commission under Grant number 700199 through the
# Horizon 2020 program. The authors would like to acknowledge the contributions
# of their colleagues of the SHIELD partner consortium (www.shield-h2020.eu).


import logging
from pprint import pformat

import requests
from aaa_api import AaaApi
from dashboardutils import http_utils
from dashboardutils.error_utils import IssueHandling, IssueElement
from werkzeug.exceptions import *


class KeystoneAuthzApi(AaaApi):
    # Define the keystone endpoints to serve the AAA API.
    login = 'auth/tokens?nocatalog'
    tokens = 'auth/tokens?allow_expired=False'
    tenants = 'domains'
    tenant_query = '{}?name={{}}'.format(tenants)
    for_tenant = '{}/{{}}'.format(tenants)
    groups = 'groups'
    for_group = '{}/{{}}'.format(groups)
    roles = 'roles'
    for_role = '{}/{{}}'.format(roles)
    for_group_role = '{}/groups/{{}}/roles/{{}}'.format(for_tenant)
    users = 'users'
    for_group_user = '{}/users/{{}}'.format(for_group)

    __errors = {
        'TENANTS': {
            'CONFLICT_ISSUE': {
                IssueElement.ERROR:     ["User already exists. User: '{}'."],
                IssueElement.EXCEPTION: Conflict("User already exists.")
                },
            'CREATION_ISSUE': {
                IssueElement.ERROR:     ["Domain creation failed as it's not enabled. Data: '{}'."],
                IssueElement.EXCEPTION: InternalServerError("Domain creation failed.")
                },
            'UPDATE_ISSUE':   {
                IssueElement.ERROR:     ["Domain update failed as it's not enabled. Data: '{}'."],
                IssueElement.EXCEPTION: InternalServerError("Domain update failed.")
                }
            },
        'USERS':   {
            'CREATION_ISSUE': {
                IssueElement.ERROR:     ["User creation failed as domain doesn't match. Data: '{}'."],
                IssueElement.EXCEPTION: InternalServerError("User creation failed.")
                }
            },
        'AAA':     {
            'UNREACHABLE': {
                IssueElement.ERROR:     ["AAA system can't be reached at '{}'"],
                IssueElement.EXCEPTION: Conflict("User already exists.")
                }
            }
        }

    def __init__(self, protocol, host, port, username, password, service_admin, logger=None):
        super().__init__(protocol, host, port, username, password, service_admin, logger)

        self.logger = logger or logging.getLogger(__name__)
        self.issue = IssueHandling(self.logger)

        self.service_token = self.password_login(username, password, service_admin)

    def _login(self, authentication):
        """
        Login helper method.

        :param authentication: The authentication data to supply for the login request.
        :return: the login token for the authenticated user.
        """

        self.logger.debug('authentication: ' + pformat(authentication))

        url = self.api_basepath + '/' + KeystoneAuthzApi.login

        try:
            r = http_utils.post_json(url, data=authentication)

            token = r.json()
            token['token']['id'] = r.headers['X-Subject-Token']

            del token['token']['methods']
            del token['token']['audit_ids']

            return token

        except requests.exceptions.ConnectionError:
            self.issue.raise_ex(IssueElement.ERROR, self.__errors['AAA']['UNREACHABLE'], [[url]])

    def password_login(self, username, password, scope):
        """
        Super Administrator login to get the service token for all interactions with the external authorization system.

        :param username:
        :param password:
        :param scope:
        :return:
        """

        authentication = {
            'auth': {
                'identity': {
                    'methods':  [
                        'password'
                        ],
                    'password': {
                        'user': {
                            'name':     username,
                            'domain':   {
                                'name': scope
                                },
                            'password': password
                            }
                        }
                    },
                'scope':    {
                    'domain': {
                        'name': scope
                        }
                    }
                }
            }

        return self._login(authentication)

    def token_login(self, token, scope_id):
        authentication = {
            'auth': {
                'identity': {
                    'methods': [
                        'token'
                        ],
                    'token':   {
                        'id': token
                        }
                    },
                'scope':    {
                    'domain': {
                        'id': scope_id
                        }
                    }
                }
            }

        return self._login(authentication)

    def get_token_data(self, token):
        service_token = self.password_login(username=self.username,
                                            password=self.password,
                                            scope=self.service_admin)

        url = self.api_basepath + '/' + KeystoneAuthzApi.tokens

        headers = {'X-Auth-Token': service_token['token']['id'], 'X-Subject-Token': token}

        # Let the connection exception pass through as it's properly tailored to convey to the caller.
        r = http_utils.get(url, headers=headers)

        token = r.json()
        del token['token']['methods']
        del token['token']['audit_ids']

        return token

    def create_group(self, tenant_id, description, code, role_id):
        group = {
            "group": {
                "description": description,
                "domain_id":   tenant_id,
                "name":        code
                }
            }

        url = self.api_basepath + '/' + KeystoneAuthzApi.groups

        headers = {'X-Auth-Token': self.service_token['token']['id']}

        try:

            self.logger.debug('create group\n' + pformat(group))

            r = http_utils.post_json(url, headers=headers, data=group)

            group_data = r.json()

            self.logger.debug('group created\n' + pformat(group_data))

            self._add_role_to_group(tenant_id, group_data['group']['id'], role_id)

            # Set data which is only available once the group is created in the external authorization system.
            group['group']['group_id'] = group_data['group']['id']

            return group

        except requests.exceptions.ConnectionError:
            self.issue.raise_ex(IssueElement.ERROR, self.__errors['AAA']['UNREACHABLE'], [[url]])

    def create_role(self, role_code, description):
        role = {
            "role": {
                "name": role_code
                }
            }

        self.logger.debug('role to create: ' + pformat(role))

        url = self.api_basepath + '/' + KeystoneAuthzApi.roles

        headers = {'X-Auth-Token': self.service_token['token']['id']}

        try:
            r = http_utils.post_json(url, headers=headers, data=role)

            role_data = r.json()

            self.logger.debug('role created:\n' + pformat(role_data))

            return role_data

        except requests.exceptions.ConnectionError:
            self.issue.raise_ex(IssueElement.ERROR, self.__errors['AAA']['UNREACHABLE'], [[url]])

    def create_tenant(self, tenant, description):
        domain = {
            "domain": {
                "description": description,
                "name":        tenant
                }
            }

        self.logger.debug('domain to create: ' + pformat(domain))

        url = self.api_basepath + '/' + KeystoneAuthzApi.tenants

        headers = {'X-Auth-Token': self.service_token['token']['id']}

        try:
            r = http_utils.post_json(url, headers=headers, data=domain)

            domain_data = r.json()

            if domain_data['domain']['enabled'] is not True:
                self.issue.raise_ex(IssueElement.ERROR, self.__errors['TENANTS']['CREATION_ISSUE'],
                                    [[pformat(domain_data)]])

            self.logger.debug('domain created:\n' + pformat(domain_data))

            return domain_data

        except requests.exceptions.ConnectionError:
            self.issue.raise_ex(IssueElement.ERROR, self.__errors['AAA']['UNREACHABLE'], [[url]])

    def remove_tenant(self, tenant):
        self.logger.debug('tenant data: ' + pformat(tenant))

        self.set_tenant_status(tenant['tenant_id'], enabled=False)
        self._delete_tenant(tenant['tenant_id'])

    def get_tenant(self, tenant):

        url = self.api_basepath + '/' + KeystoneAuthzApi.tenant_query.format(tenant)

        headers = {'X-Auth-Token': self.service_token['token']['id']}

        try:
            r = http_utils.get(url, headers=headers)

            return r.json()

        except requests.exceptions.ConnectionError:
            self.issue.raise_ex(IssueElement.ERROR, self.__errors['AAA']['UNREACHABLE'], [[url]])

    def set_tenant_status(self, tenant_id, enabled):
        domain = {
            "domain": {
                "enabled": bool(enabled)
                }
            }

        self.logger.debug('domain status: ' + pformat(domain))

        url = self.api_basepath + '/' + KeystoneAuthzApi.for_tenant.format(tenant_id)

        headers = {'X-Auth-Token': self.service_token['token']['id']}

        try:
            r = http_utils.patch(url, headers=headers, data=domain)

            domain_data = r.json()

            if domain_data['domain']['enabled'] is not enabled:
                self.issue.raise_ex(IssueElement.ERROR, self.__errors['TENANTS']['UPDATE_ISSUE'],
                                    [[pformat(domain_data)]])

        except requests.exceptions.ConnectionError:
            self.issue.raise_ex(IssueElement.ERROR, self.__errors['AAA']['UNREACHABLE'], [[url]])

    def _delete_tenant(self, tenant_id):
        url = self.api_basepath + '/' + KeystoneAuthzApi.for_tenant.format(tenant_id)

        headers = {'X-Auth-Token': self.service_token['token']['id']}

        try:
            r = http_utils.delete(url, headers=headers)

        except requests.exceptions.ConnectionError:
            self.issue.raise_ex(IssueElement.ERROR, self.__errors['AAA']['UNREACHABLE'], [[url]])

    def _add_role_to_group(self, tenant_id, group_id, role_id):

        url = self.api_basepath + '/' + KeystoneAuthzApi.for_group_role.format(tenant_id, group_id, role_id)

        headers = {'X-Auth-Token': self.service_token['token']['id']}

        try:
            http_utils.put_json(url, headers=headers)

        except requests.exceptions.ConnectionError:
            self.issue.raise_ex(IssueElement.ERROR, self.__errors['AAA']['UNREACHABLE'], [[url]])

    def _create_user(self, tenant_id, user_data):
        user = {
            "user": {
                "domain_id":   tenant_id,
                "name":        user_data['name'],
                "password":    user_data['password'],
                "description": user_data['description'],
                "email":       user_data['email'],
                "enabled":     True
                }
            }

        url = self.api_basepath + '/' + KeystoneAuthzApi.users

        headers = {'X-Auth-Token': self.service_token['token']['id']}

        try:

            self.logger.debug('create user\n' + pformat(user))

            r = http_utils.post_json(url, headers=headers, data=user)

            user_data = r.json()

            if not user_data['user']['domain_id'] == tenant_id:
                # Something fishy here.
                self.issue.raise_ex(IssueElement.ERROR, self.__errors['USERS']['CREATION_ISSUE'], [[user_data]])

            user_data['user']['tenant_id'] = tenant_id

            del user_data['user']['domain_id']
            del user_data['user']['links']

            return user_data

        except requests.exceptions.ConnectionError:
            self.issue.raise_ex(IssueElement.ERROR, self.__errors['AAA']['UNREACHABLE'], [[url]])

    def create_tenant_user(self, tenant_id, user_data):
        created_user = self._create_user(tenant_id, user_data)
        self._add_user_to_group(created_user['user']['id'], user_data['group_id'])

        return created_user

    def create_developer(self, tenant_id, user_data):
        created_user = self._create_user(tenant_id, user_data)
        self._add_user_to_group(created_user['user']['id'], user_data['group_id'])

        return created_user

    def _add_user_to_group(self, user_id, group_id):

        url = self.api_basepath + '/' + KeystoneAuthzApi.for_group_user.format(group_id, user_id)

        headers = {'X-Auth-Token': self.service_token['token']['id']}

        try:
            http_utils.put_json(url, headers=headers)

        except requests.exceptions.ConnectionError:
            self.issue.raise_ex(IssueElement.ERROR, self.__errors['AAA']['UNREACHABLE'], [[url]])
