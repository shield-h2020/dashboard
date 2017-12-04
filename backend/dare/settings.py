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

# NOTE: this shall be removed once AAA is in place.
VNSFO_TENANT_ID = os.environ.get('VNSFO_TENANT_ID', '__no_tenant_set__')

###
#   Message Queue
###

# Server hostname or IP.
MSGQ_HOST = os.environ.get('MSGQ_HOST', 'localhost')

# Server port
MSGQ_PORT = os.environ.get('MSGQ_PORT', '5672')

# Message queue exchangers.
MSGQ_EXCHANGE_DASHBOARD = os.environ.get('MSGQ_EXCHANGE_DASHBOARD', '__MSGQ_EXCHANGE_SHIELD_DASHBOARD__')
MSGQ_EXCHANGE_TYPE = 'topic'

# DARE message queue settings.
MSGQ_DARE = os.environ.get('MSGQ_DARE', '__no_DARE_queue_set__')
MSGQ_DARE_ACK = bool(os.environ.get('MSGQ_DARE_ACK', False))
MSGQ_DARE_TOPIC = os.environ.get('MSGQ_DARE_TOPIC', 'shield.dare.policy')

###
#   Websocket
###

# Server hostname or IP.
SKT_HOST = os.environ.get('SKT_HOST', 'localhost')
SKT_PORT = os.environ.get('SKT_PORT', '8888')

###
#   Policy persistence
#
BACKENDAPI_PROTOCOL = os.environ.get('BACKENDAPI_PROTOCOL', None)
BACKENDAPI_HOST = os.environ.get('BACKENDAPI_HOST', 'localhost')
BACKENDAPI_PORT = os.environ.get('BACKENDAPI_PORT', 3030)
BACKENDAPI_URL = '{}://{}:{}'.format(BACKENDAPI_PROTOCOL, BACKENDAPI_HOST, BACKENDAPI_PORT)

__policy_rest__ = {
    'persist_policy': {
        'url': '{}/{}'.format(BACKENDAPI_URL, 'admin/policies'),
        'headers': {'Content-Type': 'application/json'}
    }
}

POLICYAPI_PERSIST_URL = __policy_rest__['persist_policy']['url']
POLICYAPI_PERSIST_HEADERS = __policy_rest__['persist_policy']['headers']

###
#   Policy schema
###

POLICYSCHEMA_FILE = 'schema/mspl.xsd'
