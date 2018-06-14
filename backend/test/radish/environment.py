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

import os

from radish import world

world.env = {
    'hosts': {
        'backend_api': {
            'host': '{}://{}:{}'.format(os.environ['BACKENDAPI_PROTOCOL'], os.environ['BACKENDAPI_HOST'],
                                        os.environ['BACKENDAPI_PORT'])
        },
        'tenant_ip_api': {
            'host': '{}://{}:{}'.format(os.environ['TENANT_IP_PROTOCOL'], os.environ['TENANT_IP_HOST'],
                                        os.environ['TENANT_IP_PORT'])
        },
        'msg_q': {
            'host': os.environ['MSGQ_HOST'],
            'port': int(os.environ['MSGQ_PORT']),
            'exchange': os.environ['MSGQ_EXCHANGE_DASHBOARD'],
            'exchange_type': os.environ['MSGQ_EXCHANGE_TYPE'],
            'topic': os.environ['MSGQ_DARE_TOPIC']
        },
        'vnsf_msg_q': {
            'host': os.environ['MSGQ_HOST'],
            'port': int(os.environ['MSGQ_PORT']),
            'exchange': os.environ['MSGQ_EXCHANGE_DASHBOARD'],
            'exchange_type': os.environ['MSGQ_EXCHANGE_TYPE'],
            'topic': os.environ['MSGQ_VNSF_TOPIC']
        },
        'socket_server': {
            'host': 'ws://{}:{}'.format(os.environ['SKT_HOST'],
                                         os.environ['SKT_PORT'])
        },
        'vnsfo': {
            'host': '{}://{}:{}/{}'.format(os.environ['VNSFO_PROTOCOL'], os.environ['VNSFO_HOST'],
                                           os.environ['VNSFO_PORT'], os.environ['VNSFO_API'])
        }
    },
    'data': {
        'input_data': os.environ['FOLDER_TESTS_INPUT_DATA'],
        'expected_output': os.environ['FOLDER_TESTS_EXPECTED_OUTPUT'],
    },
    'mock': {
        'vnsfo_data': os.environ['FOLDER_TESTS_MOCK_VNSFO_DATA'],
        'vnsfo_folder': os.path.join(os.environ['CNTR_FOLDER_VNSFO'], os.environ['VNSFO_API']),

        # Association Mocks
        'association_ip_data': os.environ['FOLDER_TESTS_MOCK_ASSOCIATION_DATA'],
        'association_ip_folder': os.environ['CNTR_FOLDER_VNSFO']
    }
}
world.endpoints = {
    'policies_latest': '{}/{}?where={{"status": "Not applied"}}&sort=[("_updated", -1)]&max_results=1'.format(
        world.env['hosts']['backend_api']['host'], 'policies'),
    'policies_admin': '{}/{}'.format(world.env['hosts']['backend_api']['host'], 'admin/policies'),
    'policies_apply': '{}/{}'.format(world.env['hosts']['backend_api']['host'], 'policies'),

    'vnsf_notifications_latest': '{}/{}?sort=[("_updated", -1)]&max_results=1'.format(
        world.env['hosts']['backend_api']['host'], 'notifications')
}

world.mock_vnsfo_endpoints = {
    'apply_policy': 'vnsf/action'
}

world.sockets_endpoints = {
    'policy': '{}/policy'.format(world.env['hosts']['socket_server']['host']),
    'vnsf_notification': '{}/vnsf/notifications/{}'.format(world.env['hosts']['socket_server']['host'], '{}')
}
