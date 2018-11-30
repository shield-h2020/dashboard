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
from radish import when, world


@when(re.compile(u'The Developer onboards a (.*)'))
def onboard_vnsf(step, vnsf_file):
    print('developer_info\n' + pformat(world.my_context['developer_info']))

    print('developer\n' + pformat(world.my_context['developer']))

    print('xpto')
    print('xpto')

    data = {'developer_id': world.my_context['developer']['token']['user']['id']}

    file = os.path.join(world.env['data']['input_data'], vnsf_file)
    files = {'package': open(file, 'rb')}

    http_post_file(step, url=world.endpoints['vnsfs'], files=files, data=data,
                   auth=(world.my_context['developer']['token']['id'], ''))


@when(re.compile(u'The Platform Admin enrolls a NS from (.*)'))
def user_enrolls_ns(step, file):
    file = os.path.join(world.env['data']['input_data'], file)
    with open(file) as f:
        http_post_json(step, url=world.endpoints['nss_catalogue'], data=json.load(f),
                       auth=(world.my_context['platform_admin']['token']['id'], ''))


@when(re.compile(u'The Platform Admin enrolls a vNSF from (.*)'))
def user_enrolls_vnsf(step, file):
    file = os.path.join(world.env['data']['input_data'], file)
    with open(file) as f:
        http_post_json(step, url=world.endpoints['vnsfs_catalogue'], data=json.load(f),
                       auth=(world.my_context['platform_admin']['token']['id'], ''))


@when(re.compile(u'The User enrolls a NS from (.*)'))
def user_enrolls_ns(step, ns_file):
    url = world.endpoints['nss_catalogue'].format(world.my_context['user']['token']['user']['domain']['id'])
    print('url: ' + url)

    file = os.path.join(world.env['data']['input_data'], ns_file)
    with open(file) as f:
        http_post_json(step, url=url, data=json.load(f), auth=(world.my_context['user']['token']['id'], ''))


@when(re.compile(u'The User enrolls a vNSF from (.*)'))
def user_enrolls_vnsf(step, vnsf_file):
    url = world.endpoints['vnsfs_catalogue'].format(world.my_context['user']['token']['user']['domain']['id'])
    print('url: ' + url)

    file = os.path.join(world.env['data']['input_data'], vnsf_file)
    with open(file) as f:
        http_post_json(step, url=url, data=json.load(f), auth=(world.my_context['user']['token']['id'], ''))


@when(re.compile(u'The User provisions a NS from (.*)'))
def user_provisions_ns(step, ns_file):
    file = os.path.join(world.env['data']['input_data'], ns_file)
    with open(file) as f:
        service_data = json.load(f)

    http_get(step, url=world.endpoints['nss_catalogue'], auth=(world.my_context['user']['token']['id'], ''))
    expected_status_code(step, http_utils.HTTP_200_OK)

    nss_data = step.context.api['response']['json']
    print('network services:\n' + pformat(nss_data))

    # Get the service ID using the tag from the input data.
    service_id = None
    for service in nss_data['_items']:
        print('service:\n' + pformat(service))
        for tag in service['custom_tags']:
            if tag == service_data['service_tag']:
                service_id = service['_id']
                break

        if service_id is not None:
            break

    print('service id: ' + service_id)
    print('service id: ' + service_id)

    assert service_id is not None, service_id

    del service_data['service_tag']
    service_data['ns_id'] = service_id
    service_data['status'] = 'available'

    print('service data:\n' + pformat(service_data))

    url = world.endpoints['nss_inventory'].format(world.my_context['user']['token']['user']['domain']['id'])

    print('url: ' + url)

    http_post_json(step, url=url, data=service_data, auth=(world.my_context['user']['token']['id'], ''))
