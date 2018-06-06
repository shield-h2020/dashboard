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
from pprint import pformat

import api_endpoints
import os
import settings as cfg
from api_endpoints_def import EndpointParam
from eve.auth import BasicAuth, TokenAuth
from flask import request, g
from keystone_adapter import KeystoneAuthzApi
from oslo_config import cfg as oslocfg
from oslo_policy import policy

oslocfg.CONF()

enforcer = policy.Enforcer(oslocfg.CONF, policy_file=os.path.abspath('policy.json'))

enforcer.check_rules(True)
enforcer.load_rules(True)

logger = logging.getLogger(__name__)


class LoginAuth(BasicAuth):
    logger = logging.getLogger(__name__)

    def check_auth(self, username, password, allowed_roles, resource, method):
        aaa = KeystoneAuthzApi(protocol=cfg.AAA_PROTOCOL,
                               host=cfg.AAA_HOST,
                               port=cfg.AAA_PORT,
                               username=cfg.AAA_SVC_ADMIN_USER,
                               password=cfg.AAA_SVC_ADMIN_PASS,
                               service_admin=cfg.AAA_SVC_ADMIN_SCOPE)

        g.token = aaa.password_login(username=username, password=password,
                                     scope=request.headers.get('Shield-Authz-Scope'))

        return True


class TokenAuthzOslo(TokenAuth):
    logger = logging.getLogger(__name__)

    # Which key to lookup in the endpoint definition to retrieve the roles allowed to use the endpoint.
    __roles_lookup_key__ = {
        'resource':               'allowed_roles',
        'item_lookup':            'allowed_item_roles',
        'item_additional_lookup': 'allowed_item_roles'
        }

    def check_auth(self, token, allowed_roles, resource, method):

        try:
            endpoint_settings = getattr(api_endpoints, resource)
        except TypeError:
            self.logger.error('"home" has no endpoint data')
            return True
        except AttributeError:
            self.logger.error('No API endpoint defined for: ' + resource)
            return False

        self.logger.debug('endpoint data: ' + pformat(endpoint_settings))

        aaa = KeystoneAuthzApi(protocol=cfg.AAA_PROTOCOL,
                               host=cfg.AAA_HOST,
                               port=cfg.AAA_PORT,
                               username=cfg.AAA_SVC_ADMIN_USER,
                               password=cfg.AAA_SVC_ADMIN_PASS,
                               service_admin=cfg.AAA_SVC_ADMIN_SCOPE)

        # Let the connection exception pass through as it's properly tailored to convey to the caller.
        token_data = aaa.get_token_data(token)
        user_token = aaa.token_login(token, token_data['token']['user']['domain']['id'])

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
