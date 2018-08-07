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

# VNSF message queue settings
MSGQ_VNSF = os.environ.get('MSGQ_VNSF', '__no_VNSF_queue_set__')
MSGQ_VNSF_ACK = bool(os.environ.get('MSGQ_VNSF_ACK', False))
MSGQ_VNSF_TOPIC = os.environ.get('MSGQ_VNSF_TOPIC', 'shield.notifications.vnsf')

# Trust Monitor message queue settings
MSGQ_TM = os.environ.get('MSGQ_TM', "__no_TM_queue_set__")
MSGQ_TM_ACK = bool(os.environ.get('MSGQ_TM_ACT', False))
MSGQ_TM_TOPIC = os.environ.get('MSGQ_TM_TOPIC', 'shield.notifications.tm')


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
        'url':     '{}/{}'.format(BACKENDAPI_URL, 'admin/policies'),
        'headers': {'Content-Type': 'application/json'}
        }
    }

POLICYAPI_PERSIST_URL = __policy_rest__['persist_policy']['url']
POLICYAPI_PERSIST_HEADERS = __policy_rest__['persist_policy']['headers']

###
#   Notification persistence
###

__vnsf_notification_rest__ = {
    'persist_notification': {
        'url':     '{}/{}'.format(BACKENDAPI_URL, 'admin/notifications'),
        'headers': {'Content-Type': 'application/json'}
        }
    }

NOTIFICATION_API_PERSIST_URL = __vnsf_notification_rest__['persist_notification']['url']
NOTIFICATION_API_PERSIST_HEADERS = __vnsf_notification_rest__['persist_notification']['headers']

###
#   Association Tenant IP
###

TENANT_IP_PROTOCOL = os.environ.get('TENANT_IP_PROTOCOL', None)
TENANT_IP_HOST = os.environ.get('TENANT_IP_HOST', 'localhost')
TENANT_IP_PORT = os.environ.get('TENANT_IP_PORT', -1)
TENANT_IP_URL = '{}://{}:{}'.format(TENANT_IP_PROTOCOL, TENANT_IP_HOST, TENANT_IP_PORT)

__association_rest__ = {
    'association': {
        'url':     '{}/{}'.format(TENANT_IP_URL, 'tenant_ips'),
        'headers': {'Content-Type': 'application/json'}
        }
    }

ASSOCIATION_API_URL = __association_rest__['association']['url']
ASSOCIATION_API_HEADERS = __association_rest__['association']['headers']


###
#   Association vNSF Instance
###
VNSF_INSTANCE_PROTOCOL = os.environ.get('TENANT_IP_PROTOCOL', None)
VNSF_INSTANCE_HOST = os.environ.get('TENANT_IP_HOST', 'localhost')
VNSF_INSTANCE_PORT = os.environ.get('TENANT_IP_PORT', -1)
VNSF_INSTANCE_URL = '{}://{}:{}'.format(VNSF_INSTANCE_PROTOCOL, VNSF_INSTANCE_HOST, VNSF_INSTANCE_PORT)

__tm_association_rest__ = {
    'tm_association': {
        'url':     '{}/{}'.format(VNSF_INSTANCE_URL, 'tenant_vnsfs'),
        'headers': {'Content-Type': 'application/json'}
        }
    }

TM_ASSOCIATION_API_URL = __tm_association_rest__['tm_association']['url']
TM_ASSOCIATION_API_HEADERS = __tm_association_rest__['tm_association']['headers']


###
#   Schemas
###

POLICYSCHEMA_FILE = 'schema/mspl.xsd'
