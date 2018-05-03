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


@given(u'The Platform Admin is logged in')
def platform_admin_login(step):
    set_http_headers(step, {'Shield-Authz-Scope': world.env['hosts']['aaa']['svc_admin_scope']})
    http_post_json(step, url=world.endpoints['login'],
                   auth=(world.env['hosts']['aaa']['svc_admin_user'], world.env['hosts']['aaa']['svc_admin_pass']))
    expected_status_code(step, http_utils.HTTP_201_CREATED)

    world.my_context['platform_admin'] = step.context.api['response']['json']


@given(u'The Tenant Admin is logged in')
def tenant_admin_login(step):
    set_http_headers(step, {'Shield-Authz-Scope': world.my_context['tenant_info']['tenant_name']})
    http_post_json(step, url=world.endpoints['login'], auth=(
        world.my_context['tenant_admin_info']['name'],
        world.my_context['tenant_admin_info']['password']))
    expected_status_code(step, http_utils.HTTP_201_CREATED)

    world.my_context['tenant_admin'] = step.context.api['response']['json']


@given(u'The Tenant User is logged in')
def tenant_user_login(step):
    set_http_headers(step, {'Shield-Authz-Scope': world.my_context['tenant_info']['tenant_name']})
    http_post_json(step, url=world.endpoints['login'], auth=(
        world.my_context['tenant_user_info']['name'],
        world.my_context['tenant_user_info']['password']))
    expected_status_code(step, http_utils.HTTP_201_CREATED)

    world.my_context['tenant_user'] = step.context.api['response']['json']


@given(re.compile(u'The Platform Admin creates a Tenant from (.*)'))
def platform_admin_create_tenant(step, tenant_file):
    file = os.path.join(world.env['data']['input_data'], tenant_file)
    with open(file) as f:
        http_post_json(step, url=world.endpoints['tenants'], data=json.load(f),
                       auth=(world.my_context['platform_admin']['token']['id'], ''))

    expected_status_code(step, http_utils.HTTP_201_CREATED)

    url = world.endpoints['tenant_info'].format(step.context.api['response']['json']['tenant_id'])
    http_get(step, url=url, auth=(world.my_context['platform_admin']['token']['id'], ''))
    expected_status_code(step, http_utils.HTTP_200_OK)

    world.my_context['tenant_info'] = step.context.api['response']['json']


@given(re.compile(u'The Platform Admin creates a Tenant Admin from (.*)'))
def platform_admin_create_tenant_admin(step, tenant_file):
    file = os.path.join(world.env['data']['input_data'], tenant_file)
    with open(file) as f:
        user_data = json.load(f)

    user_data['group_id'] = world.my_context['tenant_info']['groups'][0]['group']['group_id']

    print('tenant_info\n' + pformat(world.my_context['tenant_info']))

    print('template url for tenant_users: ' + world.endpoints['tenant_users'])

    url = world.endpoints['tenant_users'].format(world.my_context['tenant_info']['tenant_id'])
    print('url: ' + url)
    print('url: ' + url)

    http_post_json(step, url=url, data=user_data, auth=(world.my_context['platform_admin']['token']['id'], ''))

    expected_status_code(step, http_utils.HTTP_201_CREATED)

    url = world.endpoints['tenant_user_specific'].format(step.context.api['response']['json']['user_id'],
                                                         world.my_context['tenant_info']['tenant_id'])

    print('url: ' + url)
    print('url: ' + url)

    http_get(step, url=url, auth=(world.my_context['platform_admin']['token']['id'], ''))
    expected_status_code(step, http_utils.HTTP_200_OK)

    world.my_context['tenant_admin_info'] = step.context.api['response']['json']
    print('tenant_admin_info\n' + pformat(world.my_context['tenant_admin_info']))


@given(re.compile(u'The Tenant Admin creates a User from (.*)'))
def tenant_admin_create_user(step, user_file):
    file = os.path.join(world.env['data']['input_data'], user_file)
    with open(file) as f:
        user_data = json.load(f)

    user_data['group_id'] = world.my_context['tenant_info']['groups'][1]['group']['group_id']

    url = world.endpoints['tenant_users'].format(world.my_context['tenant_info']['tenant_id'])
    print('url: ' + url)
    print('url: ' + url)

    http_post_json(step, url=url, data=user_data, auth=(world.my_context['tenant_admin']['token']['id'], ''))
    expected_status_code(step, http_utils.HTTP_201_CREATED)

    url = world.endpoints['tenant_user_specific'].format(step.context.api['response']['json']['user_id'],
                                                         world.my_context['tenant_info']['tenant_id'])

    print('url: ' + url)
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
