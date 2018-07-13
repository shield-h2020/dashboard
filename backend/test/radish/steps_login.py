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
from pprint import pformat

import os
import re
from dashboardtestingutils.steps_utils import *
from dashboardutils import http_utils
from radish import given, when, world


def logon_into_tenant(step, user, password):
    set_http_headers(step, {'Shield-Authz-Scope': world.my_context['tenant_info']['tenant_name']})
    http_post_json(step, url=world.endpoints['login'], auth=(user, password))
    expected_status_code(step, http_utils.HTTP_201_CREATED)


def user_login(step, credentials_file):
    file = os.path.join(world.env['data']['input_data'], credentials_file)
    with open(file) as f:
        login_data = json.load(f)

    set_http_headers(step, {'Shield-Authz-Scope': login_data['tenant']})

    http_post_json(step, url=world.endpoints['login'], auth=(login_data['username'], login_data['password']))
    expected_status_code(step, http_utils.HTTP_201_CREATED)


@given(u'The Platform Admin is logged in')
def platform_admin_login(step):
    set_http_headers(step, {'Shield-Authz-Scope': world.env['hosts']['aaa']['svc_admin_scope']})
    http_post_json(step, url=world.endpoints['login'],
                   auth=(world.env['hosts']['aaa']['svc_admin_user'], world.env['hosts']['aaa']['svc_admin_pass']))
    expected_status_code(step, http_utils.HTTP_201_CREATED)

    world.my_context['platform_admin'] = step.context.api['response']['json']


@when(u'The Tenant Admin is logged in')
def tenant_admin_login(step):
    logon_into_tenant(step, world.my_context['tenant_admin_info']['name'],
                      world.my_context['tenant_admin_info']['password'])
    world.my_context['tenant_admin'] = step.context.api['response']['json']


@given(u'The Tenant User is logged in')
def tenant_user_login(step):
    logon_into_tenant(step, world.my_context['tenant_user_info']['name'],
                      world.my_context['tenant_user_info']['password'])
    world.my_context['tenant_user'] = step.context.api['response']['json']


@when(u'The Developer is logged in')
def developer_login(step):
    logon_into_tenant(step, world.my_context['developer_info']['name'], world.my_context['developer_info']['password'])
    world.my_context['developer'] = step.context.api['response']['json']


@given(re.compile(u'The User logs in with (.*)'))
def tenant_admin_login(step, credentials_file):
    user_login(step, credentials_file)
    world.my_context['user'] = step.context.api['response']['json']

    print('logged user:\n' + pformat(world.my_context['user']))


@given(re.compile(u'The User logs in using (.*)'))
def login(step, credentials_file):
    user_login(step, credentials_file)

    world.my_context['user'] = step.context.api['response']['json']

    print('logged user:\n' + pformat(world.my_context['user']))

    # The tenant data is stored into the testing context for later usage.
    url = world.endpoints['tenant_info'].format(world.my_context['user']['token']['user']['domain']['id'])
    http_get(step, url=url, auth=(world.my_context['platform_admin']['token']['id'], ''))
    expected_status_code(step, http_utils.HTTP_200_OK)

    world.my_context['tenant_info'] = step.context.api['response']['json']


@when(u'The New User logs in')
def login(step):
    logon_into_tenant(step, world.my_context['tenant_user_info']['name'],
                      world.my_context['tenant_user_info']['password'])
    world.my_context['tenant_user'] = step.context.api['response']['json']
