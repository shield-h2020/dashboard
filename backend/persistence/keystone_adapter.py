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


class KeystoneAuthzApi(AaaApi):
    # The dictionary is used only for fast lookup, hence the values are meaningful.
    _roles_to_use = {
        'shield_tenant_admin': 'dummy',
        'shield_tenant_user':  'dummy'
        }

    _group_roles = {
        'shield_tenant_admins': 'shield_tenant_admin',
        'shield_tenant_users':  'shield_tenant_user'
        }

    login = 'auth/tokens?nocatalog'
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

    def __init__(self, protocol, host, port, username, password, service_admin, logger=None):
        super().__init__(protocol, host, port, username, password, service_admin, logger)

        self.logger = logger or logging.getLogger(__name__)

        self.service_token = self._service_login(username, password, service_admin)

        self.roles_available = self._get_roles()

    def _service_login(self, username, password, scope):
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

        self.logger.debug('authentication: ' + pformat(authentication))

        url = self.api_basepath + '/' + KeystoneAuthzApi.login

        try:
            r = requests.post(url, json=authentication, verify=False)

            if len(r.text) > 0:
                self.logger.debug(r.text)

            if not r.status_code == http_utils.HTTP_201_CREATED:
                # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['POLICY_ISSUE'],
                #                     [[url, r.status_code]])
                raise PermissionError

            token = r.json()
            token['token']['id'] = r.headers['X-Subject-Token']

            return token

        except requests.exceptions.ConnectionError:
            # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['VNSFO_UNREACHABLE'],
            #                     [[url]])
            raise requests.exceptions.ConnectionError

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
            r = requests.post(url, headers=headers, json=domain, verify=False)

            if len(r.text) > 0:
                self.logger.debug(r.text)

            if r.status_code == http_utils.HTTP_409_CONFLICT:
                raise FileExistsError

            if not r.status_code == http_utils.HTTP_201_CREATED:
                # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['POLICY_ISSUE'],
                #                     [[url, r.status_code]])
                raise PermissionError

            domain_data = r.json()

            self.logger.debug('domain created:\n' + pformat(domain_data))

            if domain_data['domain']['enabled'] is not True:
                raise FileNotFoundError

            groups_data = self._create_groups(domain_data['domain']['id'])

            domain_data['domain']['groups'] = groups_data

            return domain_data

        except requests.exceptions.ConnectionError:
            # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['VNSFO_UNREACHABLE'],
            #                     [[url]])
            raise requests.exceptions.ConnectionError

    def remove_tenant(self, tenant):
        self.logger.debug('tenant data: ' + pformat(tenant))

        self.set_tenant_status(tenant['tenant_id'], enabled=False)
        self._delete_tenant(tenant['tenant_id'])

    def get_tenant(self, tenant):

        url = self.api_basepath + '/' + KeystoneAuthzApi.tenant_query.format(tenant)

        headers = {'X-Auth-Token': self.service_token['token']['id']}

        try:
            r = requests.get(url, headers=headers, verify=False)

            if len(r.text) > 0:
                self.logger.debug(r.text)

            if not r.status_code == http_utils.HTTP_200_OK:
                # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['POLICY_ISSUE'],
                #                     [[url, r.status_code]])
                raise PermissionError

            return r.json()

        except requests.exceptions.ConnectionError:
            # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['VNSFO_UNREACHABLE'],
            #                     [[url]])
            raise requests.exceptions.ConnectionError

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
            r = requests.patch(url, headers=headers, json=domain, verify=False)

            if len(r.text) > 0:
                self.logger.debug(r.text)

            if not r.status_code == http_utils.HTTP_200_OK:
                # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['POLICY_ISSUE'],
                #                     [[url, r.status_code]])
                raise PermissionError

            domain_data = r.json()

            if domain_data['domain']['enabled'] is not enabled:
                raise FileNotFoundError

        except requests.exceptions.ConnectionError:
            # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['VNSFO_UNREACHABLE'],
            #                     [[url]])
            raise requests.exceptions.ConnectionError

    def _delete_tenant(self, tenant_id):
        url = self.api_basepath + '/' + KeystoneAuthzApi.for_tenant.format(tenant_id)

        headers = {'X-Auth-Token': self.service_token['token']['id']}

        try:
            r = requests.delete(url, headers=headers, verify=False)

            if len(r.text) > 0:
                self.logger.debug(r.text)

            if not r.status_code == http_utils.HTTP_204_NO_CONTENT:
                # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['POLICY_ISSUE'],
                #                     [[url, r.status_code]])
                raise PermissionError

        except requests.exceptions.ConnectionError:
            # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['VNSFO_UNREACHABLE'],
            #                     [[url]])
            raise requests.exceptions.ConnectionError

    def _create_groups(self, tentant_id):
        groups = [
            {
                "group": {
                    "description": "Tenant Admins",
                    "domain_id":   tentant_id,
                    "name":        "shield_tenant_admins",
                    "role_id":     self.roles_available['shield_tenant_admin']['role_id']
                    }
                },
            {
                "group": {
                    "description": "Tenant Users",
                    "domain_id":   tentant_id,
                    "name":        "shield_tenant_users",
                    "role_id":     self.roles_available['shield_tenant_user']['role_id']
                    }
                }
            ]

        url = self.api_basepath + '/' + KeystoneAuthzApi.groups

        headers = {'X-Auth-Token': self.service_token['token']['id']}

        try:

            for i, group in enumerate(groups):
                self.logger.debug('create group\n' + pformat(group))

                r = requests.post(url, headers=headers, json=group, verify=False)

                if len(r.text) > 0:
                    self.logger.debug(r.text)

                if r.status_code == http_utils.HTTP_409_CONFLICT:
                    raise FileExistsError

                if not r.status_code == http_utils.HTTP_201_CREATED:
                    # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['POLICY_ISSUE'],
                    #                     [[url, r.status_code]])
                    raise PermissionError

                group_data = r.json()

                self._add_role_to_group(tentant_id, group_data['group']['id'], groups[i]['group']['role_id'])

                # Set data which is only available once the group is created in the external authorization system.
                groups[i]['group']['group_id'] = group_data['group']['id']

            return groups

        except requests.exceptions.ConnectionError:
            # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['VNSFO_UNREACHABLE'],
            #                     [[url]])
            raise requests.exceptions.ConnectionError

    def _get_roles(self):

        url = self.api_basepath + '/' + KeystoneAuthzApi.roles

        headers = {'X-Auth-Token': self.service_token['token']['id']}

        try:
            r = requests.get(url, headers=headers, verify=False)

            if len(r.text) > 0:
                self.logger.debug(r.text)

            if not r.status_code == http_utils.HTTP_200_OK:
                # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['POLICY_ISSUE'],
                #                     [[url, r.status_code]])
                raise PermissionError

            roles_data = r.json()

            roles_available = dict()

            # As the external authorization system provides a list of roles, we need to go through it ignoring the
            # "irrelevant" ones.
            for role in roles_data['roles']:
                role_found = self._roles_to_use.get(role['name'], None)

                if role_found is None:
                    # Ignore roles not relevant for the business logic.
                    continue

                roles_available[role['name']] = {'role_id': role['id']}

            return roles_available

        except requests.exceptions.ConnectionError:
            # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['VNSFO_UNREACHABLE'],
            #                     [[url]])
            raise requests.exceptions.ConnectionError

    def _add_role_to_group(self, tenant_id, group_id, role_id):

        url = self.api_basepath + '/' + KeystoneAuthzApi.for_group_role.format(tenant_id, group_id, role_id)

        headers = {'X-Auth-Token': self.service_token['token']['id']}

        try:
            r = requests.put(url, headers=headers, verify=False)

            if len(r.text) > 0:
                self.logger.debug(r.text)

            if not r.status_code == http_utils.HTTP_204_NO_CONTENT:
                # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['POLICY_ISSUE'],
                #                     [[url, r.status_code]])
                raise PermissionError

        except requests.exceptions.ConnectionError:
            # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['VNSFO_UNREACHABLE'],
            #                     [[url]])
            raise requests.exceptions.ConnectionError

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

            r = requests.post(url, headers=headers, json=user, verify=False)

            if len(r.text) > 0:
                self.logger.debug(r.text)

            if r.status_code == http_utils.HTTP_409_CONFLICT:
                raise FileExistsError

            if not r.status_code == http_utils.HTTP_201_CREATED:
                # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['POLICY_ISSUE'],
                #                     [[url, r.status_code]])
                raise PermissionError

            user_data = r.json()

            if not user_data['user']['domain_id'] == tenant_id:
                # Something fishy here.
                raise EnvironmentError

            user_data['user']['tenant_id'] = tenant_id

            del user_data['user']['domain_id']
            del user_data['user']['links']

            return user_data

        except requests.exceptions.ConnectionError:
            # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['VNSFO_UNREACHABLE'],
            #                     [[url]])
            raise requests.exceptions.ConnectionError

    def create_tenant_user(self, tenant_id, user_data):
        created_user = self._create_user(tenant_id, user_data)
        self._add_user_to_group(created_user['user']['id'], user_data['group_id'])

        return created_user

    def _add_user_to_group(self, user_id, group_id):

        url = self.api_basepath + '/' + KeystoneAuthzApi.for_group_user.format(group_id, user_id)

        headers = {'X-Auth-Token': self.service_token['token']['id']}

        try:
            r = requests.put(url, headers=headers, verify=False)

            if len(r.text) > 0:
                self.logger.debug(r.text)

            if not r.status_code == http_utils.HTTP_204_NO_CONTENT:
                # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['POLICY_ISSUE'],
                #                     [[url, r.status_code]])
                raise PermissionError

        except requests.exceptions.ConnectionError:
            # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['VNSFO_UNREACHABLE'],
            #                     [[url]])
            raise requests.exceptions.ConnectionError
