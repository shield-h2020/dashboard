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


import json
import logging
from pprint import pprint, pformat

import api_endpoints
import os
import requests
import settings as cfg
from api_endpoints_def import EndpointParam
from dashboardutils import http_utils
from eve.auth import BasicAuth, TokenAuth
from flask import request, g
from oslo_config import cfg as oslocfg
from oslo_policy import policy

oslocfg.CONF()

enforcer = policy.Enforcer(oslocfg.CONF, policy_file=os.path.abspath('policy.json'))

enforcer.check_rules(True)
enforcer.load_rules(True)

logger = logging.getLogger(__name__)


def password_login(username, password, scope):
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

    aaa_api_basepath = http_utils.build_url(server=cfg.AAA_HOST, port=cfg.AAA_PORT, basepath='v3',
                                            protocol=cfg.AAA_PROTOCOL)

    url = '{}/auth/tokens?nocatalog'.format(aaa_api_basepath)

    pprint(authentication)

    try:
        r = requests.post(url, json=authentication, verify=False)

        if len(r.text) > 0:
            logger.debug(r.text)

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


def token_login(token, scope_id):
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

    aaa_api_basepath = http_utils.build_url(server=cfg.AAA_HOST, port=cfg.AAA_PORT, basepath='v3',
                                            protocol=cfg.AAA_PROTOCOL)

    url = '{}/auth/tokens?nocatalog'.format(aaa_api_basepath)

    pprint(authentication)

    try:
        r = requests.post(url, json=authentication, verify=False)

        if len(r.text) > 0:
            logger.debug(r.text)

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


def get_token_data(token):
    service_token = password_login(username=cfg.AAA_SVC_ADMIN_USER,
                                   password=cfg.AAA_SVC_ADMIN_PASS,
                                   scope=cfg.AAA_SVC_ADMIN_SCOPE)

    aaa_api_basepath = http_utils.build_url(server=cfg.AAA_HOST, port=cfg.AAA_PORT, basepath='v3',
                                            protocol=cfg.AAA_PROTOCOL)

    url = '{}/auth/tokens?allow_expired=False'.format(aaa_api_basepath)

    headers = {'X-Auth-Token': service_token['token']['id'], 'X-Subject-Token': token}

    try:
        r = requests.get(url, headers=headers, verify=False)

        if len(r.text) > 0:
            logger.debug(r.text)

        if not r.status_code == http_utils.HTTP_200_OK:
            # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['POLICY_ISSUE'],
            #                     [[url, r.status_code]])
            raise FileNotFoundError

        token = r.json()
        del token['token']['methods']
        del token['token']['audit_ids']

        return token

    except requests.exceptions.ConnectionError:
        # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['VNSFO_UNREACHABLE'],
        #                     [[url]])
        raise requests.exceptions.ConnectionError


class RolesAuth(BasicAuth):
    logger = logging.getLogger(__name__)

    def check_auth(self, username, password, allowed_roles, resource, method):
        # # use Eve's own db driver; no additional connections/resources are used
        # accounts = app.data.driver.db['accounts']
        # lookup = {'username': username}
        # if allowed_roles:
        #     # only retrieve a user if his roles match ``allowed_roles``
        #     lookup['roles'] = {'$in': allowed_roles}
        # account = accounts.find_one(lookup)
        # return account and check_password_hash(account['password'], password)

        scope = request.headers.get('Shield-Authz-Scope')
        print('domain')
        print(scope)

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

        aaa_api_basepath = http_utils.build_url(server=cfg.AAA_HOST, port=cfg.AAA_PORT, basepath='v3',
                                                protocol=cfg.AAA_PROTOCOL)

        url = '{}/auth/tokens?nocatalog'.format(aaa_api_basepath)

        # headers = {'Content-Type': 'application/json'}

        pprint(authentication)

        print('user: {} | pass: {} | allowed_roles: {} | resource: {} | method: {}'.format(username, password,
                                                                                           allowed_roles, resource,
                                                                                           method))

        try:
            r = requests.post(url, json=authentication, verify=False)

            if len(r.text) > 0:
                RolesAuth.logger.debug(r.text)

            if not r.status_code == http_utils.HTTP_201_CREATED:
                # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['POLICY_ISSUE'],
                #                     [[url, r.status_code]])
                raise PermissionError

            authn = r.json()
            pprint(authn)

            roles = [role['name'] for role in authn['token']['roles']]
            self.logger.debug('roles: {}'.format(roles))

            authz = False
            for role in roles:
                if role in allowed_roles:
                    authz = True
                    break

            print('authz: {}'.format(authz))

            return authz

        except requests.exceptions.ConnectionError:
            # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['VNSFO_UNREACHABLE'],
            #                     [[url]])
            raise requests.exceptions.ConnectionError


class LoginAuth(BasicAuth):
    logger = logging.getLogger(__name__)

    def check_auth(self, username, password, allowed_roles, resource, method):
        # # use Eve's own db driver; no additional connections/resources are used
        # accounts = app.data.driver.db['accounts']
        # lookup = {'username': username}
        # if allowed_roles:
        #     # only retrieve a user if his roles match ``allowed_roles``
        #     lookup['roles'] = {'$in': allowed_roles}
        # account = accounts.find_one(lookup)
        # return account and check_password_hash(account['password'], password)

        scope = request.headers.get('Shield-Authz-Scope')
        print('domain')
        print(scope)

        authentication = {
            'auth': {
                'identity': {
                    'methods':  ['password'],
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

        aaa_api_basepath = http_utils.build_url(server=cfg.AAA_HOST, port=cfg.AAA_PORT, basepath='v3',
                                                protocol=cfg.AAA_PROTOCOL)

        url = '{}/auth/tokens?nocatalog'.format(aaa_api_basepath)

        # headers = {'Content-Type': 'application/json'}

        pprint(authentication)

        print('user: {} | pass: {} | allowed_roles: {} | resource: {} | method: {}'.format(username, password,
                                                                                           allowed_roles, resource,
                                                                                           method))

        try:
            r = requests.post(url, json=authentication, verify=False)

            if len(r.text) > 0:
                RolesAuth.logger.debug(r.text)

            if not r.status_code == http_utils.HTTP_201_CREATED:
                # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['POLICY_ISSUE'],
                #                     [[url, r.status_code]])
                raise PermissionError
                # return False

        except requests.exceptions.ConnectionError:
            # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['VNSFO_UNREACHABLE'],
            #                     [[url]])
            raise requests.exceptions.ConnectionError

        print('headers')
        print(r.headers)

        g.token = r.json()
        g.token['token']['id'] = r.headers['X-Subject-Token']
        del g.token['token']['methods']
        del g.token['token']['audit_ids']

        return True


class TokenAuth(TokenAuth):
    logger = logging.getLogger(__name__)

    def check_auth(self, token, allowed_roles, resource, method):
        # # use Eve's own db driver; no additional connections/resources are used
        # accounts = app.data.driver.db['accounts']
        # lookup = {'username': username}
        # if allowed_roles:
        #     # only retrieve a user if his roles match ``allowed_roles``
        #     lookup['roles'] = {'$in': allowed_roles}
        # account = accounts.find_one(lookup)
        # return account and check_password_hash(account['password'], password)

        service_token = password_login(username=cfg.AAA_SVC_ADMIN_USER,
                                       password=cfg.SHIELD_SVC_ADMIN_PASS,
                                       scope=cfg.SHIELD_SVC_ADMIN_SCOPE)

        aaa_api_basepath = http_utils.build_url(server=cfg.AAA_HOST, port=cfg.AAA_PORT, basepath='v3',
                                                protocol=cfg.AAA_PROTOCOL)

        url = '{}/auth/tokens?allow_expired=False'.format(aaa_api_basepath)

        headers = {'X-Auth-Token': service_token['token']['id'], 'X-Subject-Token': token}

        print('token: {} | allowed_roles: {} | resource: {} | method: {}'.format(token, allowed_roles, resource,
                                                                                 method))

        try:
            r = requests.get(url, headers=headers, verify=False)

            if len(r.text) > 0:
                RolesAuth.logger.debug(r.text)

            print('status: ' + str(r.status_code))

            if not r.status_code == http_utils.HTTP_200_OK:
                # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['POLICY_ISSUE'],
                #                     [[url, r.status_code]])
                raise PermissionError

            user_token = r.json()
            pprint(user_token)

            roles = [role['name'] for role in user_token['token']['roles']]
            self.logger.debug('roles: {}'.format(roles))

            authorized = False
            for role in roles:
                if role in allowed_roles:
                    authorized = True
                    break

            print('authz: {}'.format(authorized))

            return authorized

        except requests.exceptions.ConnectionError:
            # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['VNSFO_UNREACHABLE'],
            #                     [[url]])
            raise requests.exceptions.ConnectionError


class TokenAuthzOslo(TokenAuth):
    logger = logging.getLogger(__name__)

    # Which key to lookup in the endpoint definition to retrieve the roles allowed to use the endpoint.
    __roles_lookup_key__ = {
        'resource':               'allowed_roles',
        'item_lookup':            'allowed_item_roles',
        'item_additional_lookup': 'allowed_item_roles'
        }

    def check_auth(self, token, allowed_roles, resource, method):

        self.logger.debug('request')
        self.logger.debug(request)
        self.logger.debug('args')
        self.logger.debug(request.args)

        self.logger.debug('request.path')
        self.logger.debug(request.path)

        self.logger.debug('request.script_root')
        self.logger.debug(request.script_root)

        self.logger.debug('request.url')
        self.logger.debug(request.url)

        self.logger.debug('request.base_url')
        self.logger.debug(request.base_url)

        self.logger.debug('request.url_root')
        self.logger.debug(request.url_root)

        self.logger.debug('request.endpoint')
        self.logger.debug(request.endpoint)

        self.logger.debug('request.url_rule.methods')
        self.logger.debug(request.url_rule.methods)

        self.logger.debug('request.view_args')
        self.logger.debug(request.view_args)

        try:
            endpoint_settings = getattr(api_endpoints, resource)
        except TypeError:
            self.logger.error('"home" has no endpoint data')
            return True
        except AttributeError:
            self.logger.error('No API endpoint defined for: ' + resource)
            return False

        self.logger.debug('endpoint data: ' + pformat(endpoint_settings))

        try:

            token_data = get_token_data(token)
            user_token = token_login(token, token_data['token']['user']['domain']['id'])

            # Policy matching is based on URI arguments and query parameters.
            target = dict()
            for key in request.view_args:
                target[key] = request.view_args[key]

            self.logger.debug('go for request.args')

            if len(request.args) > 0:
                for lookup in request.args.getlist(EndpointParam.__QUERY_KEYWORD__):
                    self.logger.debug('lookup: ' + pformat(lookup))
                    data = json.loads(lookup)
                    self.logger.debug('data: ' + pformat(data))
                    for key in data:
                        target[key] = data[key]

            self.logger.debug('target: ' + pformat(target))

            # Credentials eagerly retrieved from the user token.
            credentials = dict()
            credentials['user_id'] = user_token['token']['user']['id']
            credentials['user_name'] = user_token['token']['user']['name']
            credentials['tenant_id'] = user_token['token']['user']['domain']['id']
            credentials['tenant_name'] = user_token['token']['user']['domain']['name']
            credentials['roles'] = [role['name'] for role in user_token['token']['roles']]

            self.logger.debug('credentials: ' + pformat(credentials))

            # Key to look for in the endpoint definition when retrieving the authorization policy associated with the
            # endpoint.
            roles_key = request.endpoint.split('|')
            policy_data = endpoint_settings.get(self.__roles_lookup_key__[roles_key[1]], None)
            if policy_data is None:
                raise NotImplementedError('policy: {} | key: {}'.format(policy_data, roles_key[1]))

            policy = policy_data[0][method]
            self.logger.debug("policy to check for: '{}'".format(policy))

            return enforcer.enforce(rule=policy, target=target, creds=credentials, do_raise=True)

        except requests.exceptions.ConnectionError:
            # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['VNSFO_UNREACHABLE'],
            #                     [[url]])
            raise requests.exceptions.ConnectionError

    def create_tenant(self, token, allowed_roles, resource, method):

        self.logger.debug('request')
        self.logger.debug(request)
        self.logger.debug('args')
        self.logger.debug(request.args)

        self.logger.debug('request.path')
        self.logger.debug(request.path)

        self.logger.debug('request.script_root')
        self.logger.debug(request.script_root)

        self.logger.debug('request.url')
        self.logger.debug(request.url)

        self.logger.debug('request.base_url')
        self.logger.debug(request.base_url)

        self.logger.debug('request.url_root')
        self.logger.debug(request.url_root)

        self.logger.debug('request.endpoint')
        self.logger.debug(request.endpoint)

        self.logger.debug('request.url_rule.methods')
        self.logger.debug(request.url_rule.methods)

        self.logger.debug('request.view_args')
        self.logger.debug(request.view_args)

        print('where: ' + pformat(request.args[0]))
        print('where: ' + pformat(request.args[0]))

        try:
            endpoint_settings = getattr(api_endpoints, resource)
        except TypeError:
            self.logger.error('"home" has no endpoint data')
            return True
        except AttributeError:
            self.logger.error('No API endpoint defined for: ' + resource)
            return False

        self.logger.debug('endpoint data: ' + pformat(endpoint_settings))

        service_token = password_login(username=cfg.AAA_SVC_ADMIN_USER,
                                       password=cfg.SHIELD_SVC_ADMIN_PASS,
                                       scope=cfg.SHIELD_SVC_ADMIN_SCOPE)

        url = '{}/auth/tokens?allow_expired=False'.format(aaa_api_basepath)

        headers = {'X-Auth-Token': service_token['token']['id'], 'X-Subject-Token': token}

        self.logger.debug(
                'token: {} | allowed_roles: {} | resource: {} | method: {}'.format(token, allowed_roles, resource,
                                                                                   method))

        try:
            r = requests.get(url, headers=headers, verify=False)

            if len(r.text) > 0:
                RolesAuth.logger.debug(r.text)

            self.logger.debug('status: ' + str(r.status_code))

            if not r.status_code == http_utils.HTTP_200_OK:
                # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['POLICY_ISSUE'],
                #                     [[url, r.status_code]])
                raise PermissionError

            # Policy matching is based on URI arguments.
            target = dict()
            for key in request.view_args:
                target[key] = request.view_args[key]

            self.logger.debug('target: ' + pformat(target))

            # Credentials eagerly retrieved from the user token.
            user_token = r.json()
            credentials = dict()
            credentials['user_id'] = user_token['token']['user']['id']
            credentials['user_name'] = user_token['token']['user']['name']
            credentials['tenant_id'] = user_token['token']['user']['domain']['id']
            credentials['tenant_name'] = user_token['token']['user']['domain']['name']
            credentials['roles'] = [role['name'] for role in user_token['token']['roles']]

            self.logger.debug('credentials: ' + pformat(credentials))

            # Key to look for in the endpoint definition when retrieving the authorization policy associated with the
            # endpoint.
            roles_key = request.endpoint.split('|')
            policy_data = endpoint_settings.get(self.__roles_lookup_key__[roles_key[1]], None)
            if policy_data is None:
                raise NotImplementedError('policy: {} | key: {}'.format(policy_data, roles_key[1]))

            policy = policy_data[0][method]
            self.logger.debug("policy to check for: '{}'".format(policy))

            return enforcer.enforce(rule=policy, target=target, creds=credentials, do_raise=True)

        except requests.exceptions.ConnectionError:
            # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['VNSFO_UNREACHABLE'],
            #                     [[url]])
            raise requests.exceptions.ConnectionError
