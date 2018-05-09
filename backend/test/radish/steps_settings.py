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
from radish import given, world


@given(re.compile(u'The Platform Admin creates a tenant scope from (.*)'))
def platform_admin_create_tenant_scope(step, scope):
    file = os.path.join(world.env['data']['input_data'], scope)
    with open(file) as f:
        http_post_json(step, url=world.endpoints['tenant_scopes'], data=json.load(f),
                       auth=(world.my_context['platform_admin']['token']['id'], ''))


@given(re.compile(u'The Platform Admin creates a tenant group from (.*)'))
def platform_admin_create_tenant_group(step, group):
    file = os.path.join(world.env['data']['input_data'], group)
    with open(file) as f:
        http_post_json(step, url=world.endpoints['tenant_groups'], data=json.load(f),
                       auth=(world.my_context['platform_admin']['token']['id'], ''))


@given(re.compile(u'The Platform Admin creates a tenant role from (.*)'))
def platform_admin_create_tenant_role(step, role):
    file = os.path.join(world.env['data']['input_data'], role)
    with open(file) as f:
        http_post_json(step, url=world.endpoints['tenant_roles'], data=json.load(f),
                       auth=(world.my_context['platform_admin']['token']['id'], ''))


@given(re.compile(u'The Platform Admin associates groups to a scope from (.*)'))
def platform_admin_create_scope_groups(step, data):
    file = os.path.join(world.env['data']['input_data'], data)
    with open(file) as f:
        groups_data = json.load(f)

    print('scopes:\n' + pformat(groups_data))

    # Get the scope ID using the scope code from the input data.
    url = world.endpoints['tenant_scope_specific_code'].format(groups_data['scope_code'])

    print('url: ' + url)

    http_get(step, url=url, auth=(world.my_context['platform_admin']['token']['id'], ''))
    expected_status_code(step, http_utils.HTTP_200_OK)

    scope_data = step.context.api['response']['json']
    print('scope data:\n' + pformat(scope_data))

    scope_groups = []
    for group_code in groups_data['groups']:
        # Get the group ID using the group code from the input data.
        url = world.endpoints['tenant_group_specific_code'].format(group_code)
        print('url: ' + url)
        http_get(step, url=url, auth=(world.my_context['platform_admin']['token']['id'], ''))
        expected_status_code(step, http_utils.HTTP_200_OK)

        print('group data:\n' + pformat(step.context.api['response']['json']))

        # Save the group ID for later usage.
        scope_groups.append(step.context.api['response']['json']['_items'][0]['_id'])

    print('scope groups:')
    print(scope_groups)

    # Set the groups for the scope defined in the input data.
    url = world.endpoints['tenant_scope_groups'].format(group_code)
    print('url: ' + url)

    scope_groups_data = {
        'name':     groups_data['name'],
        'code':     groups_data['code'],
        'scope_id': scope_data['_items'][0]['_id'],
        'groups':   scope_groups
        }

    print('scope groups data:\n' + pformat(scope_groups_data))

    http_post_json(step, url=world.endpoints['tenant_scope_groups'], data=scope_groups_data,
                   auth=(world.my_context['platform_admin']['token']['id'], ''))


@given(re.compile(u'The Platform Admin associates roles to a group from (.*)'))
def platform_admin_create_group_roles(step, data):
    file = os.path.join(world.env['data']['input_data'], data)
    with open(file) as f:
        roles_data = json.load(f)

    print('roles:\n' + pformat(roles_data))

    # Get the group ID using the group code from the input data.
    url = world.endpoints['tenant_group_specific_code'].format(roles_data['group_code'])

    print('url: ' + url)

    http_get(step, url=url, auth=(world.my_context['platform_admin']['token']['id'], ''))
    expected_status_code(step, http_utils.HTTP_200_OK)

    group_data = step.context.api['response']['json']
    print('role data:\n' + pformat(group_data))

    group_roles = []
    for role_code in roles_data['roles']:
        # Get the role ID using the role code from the input data.
        url = world.endpoints['tenant_role_specific_code'].format(role_code)
        print('url: ' + url)
        http_get(step, url=url, auth=(world.my_context['platform_admin']['token']['id'], ''))
        expected_status_code(step, http_utils.HTTP_200_OK)

        print('role data:\n' + pformat(step.context.api['response']['json']))

        # Save the role ID for later usage.
        group_roles.append(step.context.api['response']['json']['_items'][0]['_id'])

    print('group roles:')
    print(group_roles)

    # Set the roles for the group defined in the input data.
    url = world.endpoints['tenant_group_roles'].format(role_code)
    print('url: ' + url)

    group_roles_data = {
        'name':     roles_data['name'],
        'code':     roles_data['code'],
        'group_id': group_data['_items'][0]['_id'],
        'roles':    group_roles
        }

    print('group roles data:\n' + pformat(group_roles_data))

    http_post_json(step, url=world.endpoints['tenant_group_roles'], data=group_roles_data,
                   auth=(world.my_context['platform_admin']['token']['id'], ''))
