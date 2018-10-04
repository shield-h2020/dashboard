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


from datetime import datetime

import os
from radish import world

world.env = {
    'hosts': {
        'backend_api':   {
            'host': '{}://{}:{}'.format(os.environ['BACKENDAPI_PROTOCOL'], os.environ['BACKENDAPI_HOST'],
                                        os.environ['BACKENDAPI_PORT'])
            },
        'tenant_ip_api': {
            'host': '{}://{}:{}'.format(os.environ['TENANT_IP_PROTOCOL'], os.environ['TENANT_IP_HOST'],
                                        os.environ['TENANT_IP_PORT'])
            },
        'mspl_msg_q':    {
            'host':          os.environ['MSGQ_HOST'],
            'port':          int(os.environ['MSGQ_PORT']),
            'exchange':      os.environ['MSGQ_EXCHANGE_DASHBOARD'],
            'exchange_type': os.environ['MSGQ_EXCHANGE_TYPE'],
            'topic':         os.environ['MSGQ_DARE_TOPIC']
            },
        'vnsf_msg_q':    {
            'host':          os.environ['MSGQ_HOST'],
            'port':          int(os.environ['MSGQ_PORT']),
            'exchange':      os.environ['MSGQ_EXCHANGE_DASHBOARD'],
            'exchange_type': os.environ['MSGQ_EXCHANGE_TYPE'],
            'topic':         os.environ['MSGQ_VNSF_TOPIC']
            },
        'tm_msg_q':      {
            'host':          os.environ['MSGQ_HOST'],
            'port':          int(os.environ['MSGQ_PORT']),
            'exchange':      os.environ['MSGQ_EXCHANGE_DASHBOARD'],
            'exchange_type': os.environ['MSGQ_EXCHANGE_TYPE'],
            'topic':         os.environ['MSGQ_TM_TOPIC']
            },
        'attack_msg_q':  {
            'host':          os.environ['MSGQ_HOST'],
            'port':          int(os.environ['MSGQ_PORT']),
            'exchange':      os.environ['MSGQ_EXCHANGE_DASHBOARD'],
            'exchange_type': os.environ['MSGQ_EXCHANGE_TYPE'],
            'topic':         os.environ['MSGQ_ATTACK_TOPIC']
            },
        'socket_server': {
            'host': 'ws://{}:{}'.format(os.environ['SKT_HOST'],
                                        os.environ['SKT_PORT'])
            },
        'vnsfo':         {
            'host': '{}://{}:{}/{}'.format(os.environ['VNSFO_PROTOCOL'], os.environ['VNSFO_HOST'],
                                           os.environ['VNSFO_PORT'], os.environ['VNSFO_API'])
            },
        'aaa':           {
            'host':            '{}://{}:{}/v3'.format(os.environ['AAA_PROTOCOL'], os.environ['AAA_HOST'],
                                                      os.environ['AAA_PORT']),
            'svc_admin_scope': os.environ['AAA_SVC_ADMIN_SCOPE'],
            'svc_admin_user':  os.environ['AAA_SCV_ADMIN_USER'],
            'svc_admin_pass':  os.environ['AAA_SCV_ADMIN_PASS']
            },
        'influxdb':      {
            'host':           f"{os.environ['INFLUXDB_PROTOCOL']}://{os.environ['INFLUXDB_HOST']}:"
                              f"{os.environ['INFLUXDB_PORT']}",
            'admin_username': os.environ.get('INFLUXDB_ADMIN_USER'),
            'username':       os.environ.get('INFLUXDB_USER'),
            'admin_password': os.environ.get('INFLUXDB_ADMIN_PASSWORD'),
            'password':       os.environ.get('INFLUXDB_USER_PASSWORD')
            }

        },
    'data':  {
        'input_data':      os.environ['FOLDER_TESTS_INPUT_DATA'],
        'expected_output': os.environ['FOLDER_TESTS_EXPECTED_OUTPUT'],
        },
    'mock':  {
        'vnsfo_data':         os.environ['FOLDER_TESTS_MOCK_VNSFO_DATA'],
        'vnsfo_folder':       os.path.join(os.environ['CNTR_FOLDER_VNSFO'], os.environ['VNSFO_API']),

        # Association Mocks
        'tenant_ip_data':     os.environ['FOLDER_TESTS_MOCK_TENANT_IP_DATA'],
        'tenant_ip_folder':   os.environ['CNTR_FOLDER_VNSFO'],

        # Tenant vNSF Association Mocks
        'tenant_vnsf_data':   os.environ['FOLDER_TESTS_MOCK_TENANT_VNSF_DATA'],
        'tenant_vnsf_folder': os.environ['CNTR_FOLDER_VNSFO']

        }
    }

world.endpoints = {
    'login':                      '{}/{}'.format(world.env['hosts']['backend_api']['host'], 'login'),

    'tenant_scopes':              '{}/{}'.format(world.env['hosts']['backend_api']['host'],
                                                 'definitions/tenant_scopes'),

    'tenant_scope_specific':      '{}/{}/{{}}'.format(world.env['hosts']['backend_api']['host'],
                                                      'definitions/tenant_scopes'),

    'tenant_scope_specific_code': '{}/{}?where={{{{"code": "{{}}"}}}}'.format(world.env['hosts']['backend_api']['host'],
                                                                              'definitions/tenant_scopes'),

    'tenant_groups':              '{}/{}'.format(world.env['hosts']['backend_api']['host'],
                                                 'definitions/tenant_groups'),

    'tenant_group_specific':      '{}/{}/{{}}'.format(world.env['hosts']['backend_api']['host'],
                                                      'definitions/tenant_groups'),

    'tenant_group_specific_code': '{}/{}?where={{{{"code": "{{}}"}}}}'.format(world.env['hosts']['backend_api']['host'],
                                                                              'definitions/tenant_groups'),

    'tenant_roles':               '{}/{}'.format(world.env['hosts']['backend_api']['host'],
                                                 'definitions/tenant_roles'),

    'tenant_role_specific':       '{}/{}/{{}}'.format(world.env['hosts']['backend_api']['host'],
                                                      'definitions/tenant_roles'),

    'tenant_role_specific_code':  '{}/{}?where={{{{"code": "{{}}"}}}}'.format(world.env['hosts']['backend_api']['host'],
                                                                              'definitions/tenant_roles'),

    'tenant_scope_groups':        '{}/{}'.format(world.env['hosts']['backend_api']['host'],
                                                 'definitions/tenant_scope_groups'),

    'tenant_group_roles':         '{}/{}'.format(world.env['hosts']['backend_api']['host'],
                                                 'definitions/tenant_group_roles'),

    'tenants':                    '{}/{}'.format(world.env['hosts']['backend_api']['host'], 'catalogue/tenants'),

    'tenant_info':                '{}/{}/{{}}'.format(world.env['hosts']['backend_api']['host'],
                                                      'catalogue/tenants'),

    'tenant_info_by_name':        '{}/{}?where={{{{"tenant_name": "{{}}"}}}}'.format(
            world.env['hosts']['backend_api']['host'],
            'catalogue/tenants'),

    'tenant_users':               '{}/{}?where={{{{"tenant_id": "{{}}"}}}}'.format(
            world.env['hosts']['backend_api']['host'], 'catalogue/users'),

    'tenant_user_specific':       '{}/{}/{{}}?where={{{{"tenant_id": "{{}}"}}}}'.format(
            world.env['hosts']['backend_api']['host'], 'catalogue/users'),

    'nss_catalogue':              '{}/{}'.format(world.env['hosts']['backend_api']['host'], 'catalogue/nss'),

    'vnsfs_catalogue':            '{}/{}'.format(world.env['hosts']['backend_api']['host'], 'catalogue/vnsfs'),

    'nss_inventory':              '{}/{}?where={{{{"tenant_id": "{{}}"}}}}'.format(
            world.env['hosts']['backend_api']['host'], 'inventory/nss'),

    'mspl_latest':                '{}/{}?where={{"status": "Not applied"}}&sort=[("_updated", '
                                  '-1)]&max_results=1'.format(
            world.env['hosts']['backend_api']['host'], 'policies'),

    'policies_admin':             '{}/{}'.format(world.env['hosts']['backend_api']['host'], 'admin/policies'),

    'mspl_apply':             '{}/{}'.format(world.env['hosts']['backend_api']['host'], 'policies'),

    'vnsf_notifications_latest':  '{}/{}?sort=[("_updated", -1)]&max_results=1&where={{"type": "VNSF"}}&xpto="{'
                                  '}"'.format(
            world.env['hosts']['backend_api']['host'], 'notifications', datetime.now()),

    'tm_notifications_latest':    '{}/{}?sort=[("_updated", -1)]&max_results=1&where={{"type": '
                                  '"TRUST_MONITOR"}}&xpto="{}"'.format(
            world.env['hosts']['backend_api']['host'], 'notifications', datetime.now()),

    'validations':                '{}/{}'.format(world.env['hosts']['backend_api']['host'], 'validations'),
    'influx_query':               f"{world.env['hosts']['influxdb']['host']}/query"
    }

world.sockets_endpoints = {
    'mspl_notification': '{}/policy/{}'.format(world.env['hosts']['socket_server']['host'], '{}'),
    'vnsf_notification': '{}/vnsf/notifications/{}'.format(world.env['hosts']['socket_server']['host'], '{}'),
    'tm_notification':   '{}/tm/notifications/{}'.format(world.env['hosts']['socket_server']['host'], '{}')
    }
