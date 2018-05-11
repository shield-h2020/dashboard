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


@given(re.compile(u'The Tenant Admin creates a User from (.*)'))
def tenant_admin_create_user(step, user_file):
    # In a proper API usage, the caller needs to supply the correct tenant user group ID, so the user to create
    # belongs to the appropriate group.
    # In this test environment, this must be simulated by providing the group code in the input data, have the test
    # code lookup the proper group ID and replace this data in the one to provide to the API.

    file = os.path.join(world.env['data']['input_data'], user_file)
    with open(file) as f:
        user_data = json.load(f)

    print('tenant info\n' + pformat(world.my_context['tenant_info']))

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

    # Create the tenant user.
    url = world.endpoints['tenant_users'].format(world.my_context['tenant_info']['tenant_id'])
    print('url: ' + url)

    http_post_json(step, url=url, data=user_data, auth=(world.my_context['tenant_admin']['token']['id'], ''))
    expected_status_code(step, http_utils.HTTP_201_CREATED)

    # The tenant user data is stored into the testing context for later usage.
    url = world.endpoints['tenant_user_specific'].format(step.context.api['response']['json']['user_id'],
                                                         world.my_context['tenant_info']['tenant_id'])

    print('url: ' + url)

    http_get(step, url=url, auth=(world.my_context['tenant_admin']['token']['id'], ''))
    expected_status_code(step, http_utils.HTTP_200_OK)

    world.my_context['tenant_user_info'] = step.context.api['response']['json']


@when(u'The Tenant Admin deletes the User')
def tenant_admin_delete_user(step):
    print('tenant_user_info\n' + pformat(world.my_context['tenant_user_info']))

    print('tenant_user\n' + pformat(world.my_context['tenant_user']))

    url = world.endpoints['tenant_user_specific'].format(world.my_context['tenant_user_info']['user_id'],
                                                         world.my_context['tenant_info']['tenant_id'])

    print('url: ' + url)

    http_get(step, url=url, auth=(world.my_context['tenant_admin']['token']['id'], ''))
    user_info = step.context.api['response']['json']

    set_http_headers(step, {'If-Match': user_info['_etag']})
    http_delete(step, url=url, auth=(world.my_context['tenant_admin']['token']['id'], ''))
    expected_status_code(step, http_utils.HTTP_204_NO_CONTENT)


@when(u'The Tenant User lists the users')
def tenant_user_list_users(step):
    url = world.endpoints['tenant_users'].format(world.my_context['tenant_info']['tenant_id'])
    http_get(step, url=url, auth=(world.my_context['tenant_user']['token']['id'], ''))


@when(u'The Tenant User lists itself')
def tenant_user_info(step):
    url = world.endpoints['tenant_user_specific'].format(world.my_context['tenant_user_info']['user_id'],
                                                         world.my_context['tenant_info']['tenant_id'])

    print('url: ' + url)

    http_get(step, url=url, auth=(world.my_context['tenant_user']['token']['id'], ''))

    print('user_info\n' + pformat(step.context.api['response']['json']))


@when(re.compile(u'The Tenant User updates from (.*)'))
def tenant_user_update(step, update_file):
    print('tenant_user_info\n' + pformat(world.my_context['tenant_user_info']))

    print('tenant_user\n' + pformat(world.my_context['tenant_user']))

    file = os.path.join(world.env['data']['input_data'], update_file)
    with open(file) as f:
        user_data = json.load(f)

    user_data['group_id'] = world.my_context['tenant_user_info']['group_id']

    url = world.endpoints['tenant_user_specific'].format(world.my_context['tenant_user_info']['user_id'],
                                                         world.my_context['tenant_info']['tenant_id'])

    print('url: ' + url)
    print('url: ' + url)

    http_get(step, url=url, auth=(world.my_context['tenant_user']['token']['id'], ''))
    user_info = step.context.api['response']['json']

    print('user_info before\n' + pformat(user_info))

    set_http_headers(step, {'If-Match': user_info['_etag']})
    http_put_json(step, url=url, data=user_data, auth=(world.my_context['tenant_user']['token']['id'], ''))
    expected_status_code(step, http_utils.HTTP_200_OK)

    http_get(step, url=url, auth=(world.my_context['tenant_user']['token']['id'], ''))

    print('user_info\n' + pformat(step.context.api['response']['json']))


@when(re.compile(u'The Tenant User patches from (.*)'))
def tenant_user_patch(step, update_file):
    print('tenant_user_info\n' + pformat(world.my_context['tenant_user_info']))

    print('tenant_user\n' + pformat(world.my_context['tenant_user']))

    file = os.path.join(world.env['data']['input_data'], update_file)
    with open(file) as f:
        user_data = json.load(f)

    user_data['group_id'] = world.my_context['tenant_user_info']['group_id']

    url = world.endpoints['tenant_user_specific'].format(world.my_context['tenant_user_info']['user_id'],
                                                         world.my_context['tenant_info']['tenant_id'])

    print('url: ' + url)
    print('url: ' + url)

    http_get(step, url=url, auth=(world.my_context['tenant_user']['token']['id'], ''))
    user_info = step.context.api['response']['json']

    print('user_info before\n' + pformat(user_info))

    set_http_headers(step, {'If-Match': user_info['_etag']})
    http_patch_json(step, url=url, data=user_data, auth=(world.my_context['tenant_user']['token']['id'], ''))

    expected_status_code(step, http_utils.HTTP_200_OK)

    http_get(step, url=url, auth=(world.my_context['tenant_user']['token']['id'], ''))

    print('user_info\n' + pformat(step.context.api['response']['json']))


@when(u'The Tenant User deletes itself')
def tenant_user_delete(step):
    print('tenant_user_info\n' + pformat(world.my_context['tenant_user_info']))

    print('tenant_user\n' + pformat(world.my_context['tenant_user']))

    url = world.endpoints['tenant_user_specific'].format(world.my_context['tenant_user_info']['user_id'],
                                                         world.my_context['tenant_info']['tenant_id'])

    print('url: ' + url)

    http_get(step, url=url, auth=(world.my_context['tenant_user']['token']['id'], ''))
    user_info = step.context.api['response']['json']

    set_http_headers(step, {'If-Match': user_info['_etag']})
    http_delete(step, url=url, auth=(world.my_context['tenant_user']['token']['id'], ''))
    expected_status_code(step, http_utils.HTTP_204_NO_CONTENT)


@given(re.compile(u'The Platform Admin creates a Developer from (.*)'))
def platform_admin_create_developer(step, user_file):
    # In a proper API usage, the caller needs to supply the correct tenant user group ID, so the user to create
    # belongs to the appropriate group.
    # In this test environment, this must be simulated by providing the group code in the input data, have the test
    # code lookup the proper group ID and replace this data in the one to provide to the API.

    file = os.path.join(world.env['data']['input_data'], user_file)
    with open(file) as f:
        user_data = json.load(f)

    print('tenant info\n' + pformat(world.my_context['tenant_info']))

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

    # Create the tenant user.
    url = world.endpoints['tenant_users'].format(world.my_context['tenant_info']['tenant_id'])
    print('url: ' + url)

    http_post_json(step, url=url, data=user_data, auth=(world.my_context['platform_admin']['token']['id'], ''))
    expected_status_code(step, http_utils.HTTP_201_CREATED)

    # The tenant user data is stored into the testing context for later usage.
    url = world.endpoints['tenant_user_specific'].format(step.context.api['response']['json']['user_id'],
                                                         world.my_context['tenant_info']['tenant_id'])

    print('url: ' + url)

    http_get(step, url=url, auth=(world.my_context['platform_admin']['token']['id'], ''))
    expected_status_code(step, http_utils.HTTP_200_OK)

    world.my_context['developer_info'] = step.context.api['response']['json']

