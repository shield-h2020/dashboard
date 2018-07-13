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


@when(re.compile(u'The Platform Admin creates a Tenant from (.*)'))
def platform_admin_create_tenant(step, tenant_file):
    file = os.path.join(world.env['data']['input_data'], tenant_file)
    with open(file) as f:
        tenant_data = json.load(f)

    # Get the scope ID using the scope code from the input data.
    url = world.endpoints['tenant_scope_specific_code'].format(tenant_data['scope_code'])

    print('url: ' + url)

    http_get(step, url=url, auth=(world.my_context['platform_admin']['token']['id'], ''))
    expected_status_code(step, http_utils.HTTP_200_OK)

    # The tenant creation endpoint expects a scope ID and not a code.
    tenant_data['scope_id'] = step.context.api['response']['json']['_items'][0]['_id']
    del tenant_data['scope_code']

    print('tenant data:\n' + pformat(tenant_data))

    # Create the tenant.
    http_post_json(step, url=world.endpoints['tenants'], data=tenant_data,
                   auth=(world.my_context['platform_admin']['token']['id'], ''))


@given(re.compile(u'The Tenant in use is (.*)'))
def tenant_in_use(step, tenant_file):
    file = os.path.join(world.env['data']['input_data'], tenant_file)
    with open(file) as f:
        tenant_data = json.load(f)

    # The tenant data is stored into the testing context for later usage.
    url = world.endpoints['tenant_info_by_name'].format(tenant_data['tenant_name'])
    print('url: ' + url)

    http_get(step, url=url, auth=(world.my_context['platform_admin']['token']['id'], ''))
    expected_status_code(step, http_utils.HTTP_200_OK)

    # The tenant information is in an array due to the query performed.
    world.my_context['tenant_info'] = step.context.api['response']['json']['_items'][0]


@when(re.compile(u'The Platform Admin creates a Tenant Admin from (.*)'))
def platform_admin_create_tenant_admin(step, tenant_file):
    # In a proper API usage, the caller needs to supply the correct tenant administrator group ID, so the user to create
    # belongs to the appropriate group.
    # In this test environment, this must be simulated by providing the group code in the input data, have the test
    # code lookup the proper group ID and replace this data in the one to provide to the API.

    file = os.path.join(world.env['data']['input_data'], tenant_file)
    with open(file) as f:
        user_data = json.load(f)

    print('tenant_info\n' + pformat(world.my_context['tenant_info']))

    # The tenant the user must belong to has the information on the groups it holds. Simply go through them and find
    # a match to the group code provided in the input data.
    group_id = None
    for group_data in world.my_context['tenant_info']['groups']:
        if group_data['group']['name'] == user_data['group_code']:
            print('group data to set:\n' + pformat(group_data))
            group_id = group_data['group']['group_id']
            break

    if group_id is None:
        raise EnvironmentError

    # The tenant user creation endpoint expects a group ID and not a code.
    user_data['group_id'] = group_id
    del user_data['group_code']

    print('user data:\n' + pformat(user_data))

    print('template url for tenant_users: ' + world.endpoints['tenant_users'])

    # Create the tenant administrator.
    url = world.endpoints['tenant_users'].format(world.my_context['tenant_info']['tenant_id'])
    print('url: ' + url)

    http_post_json(step, url=url, data=user_data, auth=(world.my_context['platform_admin']['token']['id'], ''))

    expected_status_code(step, http_utils.HTTP_201_CREATED)

    # The tenant administrator data is stored into the testing context for later usage.
    url = world.endpoints['tenant_user_specific'].format(step.context.api['response']['json']['user_id'],
                                                         world.my_context['tenant_info']['tenant_id'])

    print('url: ' + url)

    http_get(step, url=url, auth=(world.my_context['platform_admin']['token']['id'], ''))
    expected_status_code(step, http_utils.HTTP_200_OK)

    world.my_context['tenant_admin_info'] = step.context.api['response']['json']
    print('tenant_admin_info\n' + pformat(world.my_context['tenant_admin_info']))


@given(re.compile(u'The Platform Admin creates a Developers Tenant from (.*)'))
def platform_admin_create_developers_tenant(step, tenant_file):
    file = os.path.join(world.env['data']['input_data'], tenant_file)
    with open(file) as f:
        http_post_json(step, url=world.endpoints['tenants'], data=json.load(f),
                       auth=(world.my_context['platform_admin']['token']['id'], ''))

    expected_status_code(step, http_utils.HTTP_201_CREATED)

    url = world.endpoints['tenant_info'].format(step.context.api['response']['json']['tenant_id'])
    http_get(step, url=url, auth=(world.my_context['platform_admin']['token']['id'], ''))
    expected_status_code(step, http_utils.HTTP_200_OK)

    world.my_context['developers_tenant_info'] = step.context.api['response']['json']
