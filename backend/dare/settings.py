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

# vNSFO message queue settings
MSGQ_VNSFO = os.environ.get('MSGQ_VNSFO', '__no_VNSFO_queue_set__')
MSGQ_VNSFO_ACK = bool(os.environ.get('MSGQ_VNSFO_ACK', False))
MSGQ_VNSFO_TOPIC = os.environ.get('MSGQ_VNSFO_TOPIC', 'shield.notifications.vnsfo')

# VNSF message queue settings
MSGQ_VNSF = os.environ.get('MSGQ_VNSF', '__no_VNSF_queue_set__')
MSGQ_VNSF_ACK = bool(os.environ.get('MSGQ_VNSF_ACK', False))
MSGQ_VNSF_TOPIC = os.environ.get('MSGQ_VNSF_TOPIC', 'shield.notifications.vnsf')

# Trust Monitor message queue settings
MSGQ_TM = os.environ.get('MSGQ_TM', "__no_TM_queue_set__")
MSGQ_TM_ACK = bool(os.environ.get('MSGQ_TM_ACT', False))
MSGQ_TM_TOPIC = os.environ.get('MSGQ_TM_TOPIC', 'shield.notifications.tm')

# CSV attack message queue settings
MSGQ_ATTACK = os.environ.get('MSGQ_ATTACK', '__no_CSV_queue_set__')
MSGQ_ATTACK_ACK = bool(os.environ.get('MSGQ_ATTACK_ACK', True))
MSGQ_ATTACK_TOPIC = os.environ.get('MSGQ_ATTACK_TOPIC', 'shield.notifications.csv')


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


###
#   vNSFO API
#
VNSFOAPI_PROTOCOL = os.environ.get('VNSFO_PROTOCOL', 'None')
VNSFOAPI_HOST = os.environ.get('VNSFO_HOST', None)
VNSFOAPI_PORT = os.environ.get('VNSFO_PORT', None)


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
#  vNSFO Notification persistence
###

__vnsfo_notification_rest__ = {
    'persist_vnsfo_notification': {
        'url':     '{}/{}'.format(BACKENDAPI_URL, 'admin/vnsfo/notifications'),
        'headers': {'Content-Type': 'application/json'}
        },
    'inventory_nss': {
        'url':     '{}/{}'.format(BACKENDAPI_URL, 'inventory/nss'),
        'headers': {'Content-Type': 'application/json'}
        }
    }

VNSFO_NOTIFICATION_API_PERSIST_HOST_URL = __vnsfo_notification_rest__['persist_vnsfo_notification']['url']
VNSFO_NOTIFICATION_API_PERSIST_HOST_HEADERS = __vnsfo_notification_rest__['persist_vnsfo_notification']['headers']
VNSFO_NOTIFICATION_API_INVENTORY_NSS_URL = __vnsfo_notification_rest__['inventory_nss']['url']
VNSFO_NOTIFICATION_API_INVENTORY_NSS_HEADERS = __vnsfo_notification_rest__['inventory_nss']['headers']

###
#  Trusted Monitor Notification persistence
###

__tm_notification_rest__ = {
    'persist_host_notification': {
        'url':     f'{BACKENDAPI_URL}/admin/tm/notifications',
        'headers': {'Content-Type': 'application/json'}
        },
    'persist_vnsf_notification': {
        'url': f'{BACKENDAPI_URL}/admin/tm/vnsf/notifications',
        'headers': {'Content-Type': 'application/json'}
        }
    }

TM_NOTIFICATION_API_PERSIST_HOST_URL = __tm_notification_rest__['persist_host_notification']['url']
TM_NOTIFICATION_API_PERSIST_HOST_HEADERS = __tm_notification_rest__['persist_host_notification']['headers']
TM_NOTIFICATION_API_PERSIST_VNSF_URL = __tm_notification_rest__['persist_vnsf_notification']['url']
TM_NOTIFICATION_API_PERSIST_VNSF_HEADERS = __tm_notification_rest__['persist_vnsf_notification']['headers']

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
#   Tenant Endpoint
###
__tenant_rest__ = {
    'tenant': {
        'url':     '{}/{}/{}'.format(TENANT_IP_URL, 'catalogue/tenants', {}),
        'headers': {'Content-Type': 'application/json'}
        }
    }
TENANT_API_URL = __tenant_rest__['tenant']['url']
TENANT_API_HEADERS = __tenant_rest__['tenant']['headers']


###
#   Association vNSF Instance
###
VNSF_INSTANCE_PROTOCOL = os.environ.get('TENANT_IP_PROTOCOL', None)
VNSF_INSTANCE_HOST = os.environ.get('TENANT_IP_HOST', 'localhost')
VNSF_INSTANCE_PORT = os.environ.get('TENANT_IP_PORT', -1)
VNSF_INSTANCE_URL = '{}://{}:{}'.format(VNSF_INSTANCE_PROTOCOL, VNSF_INSTANCE_HOST, VNSF_INSTANCE_PORT)

__mspl_association_rest__ = {
    'mspl_association': {
        'url':     '{}/{}'.format(VNSF_INSTANCE_URL, 'tenant_vnsfs'),
        'headers': {'Content-Type': 'application/json'}
        }
    }

MSPL_ASSOCIATION_API_URL = __mspl_association_rest__['mspl_association']['url']
MSPL_ASSOCIATION_API_HEADERS = __mspl_association_rest__['mspl_association']['headers']

__tm_association_rest__ = {
    'tm_association': {
        'url':     '{}/{}'.format(VNSF_INSTANCE_URL, 'tenant_vnsfs'),
        'headers': {'Content-Type': 'application/json'}
        }
    }

TM_ASSOCIATION_API_URL = __tm_association_rest__['tm_association']['url']
TM_ASSOCIATION_API_HEADERS = __tm_association_rest__['tm_association']['headers']

TM_ATTESTATION_MESSAGE = 'New attestation data available'


###
#   Tenant <-> vNSF Instances Association
###
__tenant_vnsf_instance_association_rest__ = {
    'tenant_vnsf_instance_association': {
        'url':      '{}/{}'.format(BACKENDAPI_URL, 'tenant_vnsfs'),
        'headers': {'Content-Type': 'application/json'}
    }
}

TENANT_VNSF_INSTANCE_ASSOCIATION_URL = __tenant_vnsf_instance_association_rest__['tenant_vnsf_instance_association']['url']
TENANT_VNSF_INSTANCE_ASSOCIATION_HEADERS = __tenant_vnsf_instance_association_rest__['tenant_vnsf_instance_association']['headers']


###
#   Start Billing NS Usage
###
__billing_ns_start_usage_rest__ = {
    'billing_ns_start_usage': {
        'url':      '{}/{}'.format(BACKENDAPI_URL, 'billing/ns/start'),
        'headers': {'Content-Type': 'application/json'}
    }
}

START_BILLING_NS_USAGE_URL = __billing_ns_start_usage_rest__['billing_ns_start_usage']['url']
START_BILLING_NS_USAGE_HEADERS = __billing_ns_start_usage_rest__['billing_ns_start_usage']['headers']


###
#   Schemas
###

POLICYSCHEMA_FILE = 'schema/mspl.xsd'

###
# InfluxDB variables
###

INFLUXDB_PROTOCOL = os.environ.get('INFLUXDB_PROTOCOL', 'http')
INFLUXDB_HOST = os.environ.get('INFLUXDB_HOST', 'influx-persistence')
INFLUXDB_PORT = os.environ.get('INFLUXDB_PORT', 8086)
INFLUXDB_USER = os.environ.get('INFLUXDB_USER', '')
INFLUXDB_USER_PASSWORD = os.environ.get('INFLUXDB_USER_PASSWORD', '')
INFLUXDB_DB = os.environ.get('INFLUXDB_DB', '')
INFLUXDB_URL = f'{INFLUXDB_PROTOCOL}://{INFLUXDB_HOST}:{INFLUXDB_PORT}/write?db={INFLUXDB_DB}'
INFLUXDB_BATCH_SIZE = 7500
INFLUXDB_REQUEST_TIMEOUT = 10
