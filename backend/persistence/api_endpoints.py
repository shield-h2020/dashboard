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


import api_model
from api_endpoint_utils import EndpointHelper
from api_endpoints_def import Endpoint, EndpointVar
from security import LoginAuth

login = {
    'item_title':            'login',
    'description':           'Authentication & Authorization',
    'authentication':        LoginAuth,
    'resource_methods':      ['POST', 'GET'],

    # Allow 'token' to be returned with POST responses
    'extra_response_fields': ['token'],

    # We also disable endpoint caching as we don't want client apps to
    # cache account data.
    'cache_control':         '',
    'cache_expires':         0
    }

login_user = {
    'item_title':            'login_user',
    'description':           'Authentication & Authorization',
    'url':                   'login_user',
    'authentication':        LoginAuth,
    'resource_methods':      ['POST', 'GET'],

    # Allow 'token' to be returned with POST responses
    'extra_response_fields': ['token'],

    # We also disable endpoint caching as we don't want client apps to
    # cache account data.
    'cache_control':         '',
    'cache_expires':         0
    }

policies = {
    'item_title':       'policies',
    'description':      'Security recommendations',
    'schema':           api_model.policy_model,
    'resource_methods': ['POST', 'GET'],
    'item_methods':     ['GET', 'PATCH'],
    # 'allowed_roles': ['admin'],
    # 'allowed_write_roles': ['xpto']
    }

policies_admin = {
    'item_title':       'admin policies',
    'url':              'admin/policies',
    'schema':           api_model.policy_model,
    'datasource':       {
        'source': 'policies'
        },
    'resource_methods': ['POST'],
    'item_methods':     []
    }

tenant_scopes = {
    'item_title':         EndpointHelper.get_name(Endpoint.TENANT_SCOPES),
    'url':                EndpointHelper.get_url(Endpoint.TENANT_SCOPES),
    'additional_lookup':  {
        'url':   'regex("[\w]+")',
        'field': 'code'
        },
    'resource_methods':   EndpointHelper.get_resource_methods(Endpoint.TENANT_SCOPES),
    'allowed_roles':      [EndpointHelper.get_resource_policies(Endpoint.TENANT_SCOPES)],
    'item_methods':       EndpointHelper.get_item_methods(Endpoint.TENANT_SCOPES),
    'allowed_item_roles': [EndpointHelper.get_item_policies(Endpoint.TENANT_SCOPES)],
    'schema':             EndpointHelper.get_schema(Endpoint.TENANT_SCOPES)
    }

tenant_groups = {
    'item_title':         EndpointHelper.get_name(Endpoint.TENANT_GROUPS),
    'url':                EndpointHelper.get_url(Endpoint.TENANT_GROUPS),
    'additional_lookup':  {
        'url':   'regex("[\w]+")',
        'field': 'code'
        },
    'resource_methods':   EndpointHelper.get_resource_methods(Endpoint.TENANT_GROUPS),
    'allowed_roles':      [EndpointHelper.get_resource_policies(Endpoint.TENANT_GROUPS)],
    'item_methods':       EndpointHelper.get_item_methods(Endpoint.TENANT_GROUPS),
    'allowed_item_roles': [EndpointHelper.get_item_policies(Endpoint.TENANT_GROUPS)],
    'schema':             EndpointHelper.get_schema(Endpoint.TENANT_GROUPS)
    }

tenant_roles = {
    'item_title':         EndpointHelper.get_name(Endpoint.TENANT_ROLES),
    'url':                EndpointHelper.get_url(Endpoint.TENANT_ROLES),
    'additional_lookup':  {
        'url':   'regex("[\w]+")',
        'field': 'code'
        },
    'resource_methods':   EndpointHelper.get_resource_methods(Endpoint.TENANT_ROLES),
    'allowed_roles':      [EndpointHelper.get_resource_policies(Endpoint.TENANT_ROLES)],
    'item_methods':       EndpointHelper.get_item_methods(Endpoint.TENANT_ROLES),
    'allowed_item_roles': [EndpointHelper.get_item_policies(Endpoint.TENANT_ROLES)],
    'schema':             EndpointHelper.get_schema(Endpoint.TENANT_ROLES)
    }

tenant_scope_groups = {
    'item_title':         EndpointHelper.get_name(Endpoint.TENANT_SCOPE_GROUPS),
    'url':                EndpointHelper.get_url(Endpoint.TENANT_SCOPE_GROUPS),
    'additional_lookup':  {
        'url':   'regex("[\w]+")',
        'field': 'code'
        },
    'resource_methods':   EndpointHelper.get_resource_methods(Endpoint.TENANT_SCOPE_GROUPS),
    'allowed_roles':      [EndpointHelper.get_resource_policies(Endpoint.TENANT_SCOPE_GROUPS)],
    'item_methods':       EndpointHelper.get_item_methods(Endpoint.TENANT_SCOPE_GROUPS),
    'allowed_item_roles': [EndpointHelper.get_item_policies(Endpoint.TENANT_SCOPE_GROUPS)],
    'schema':             EndpointHelper.get_schema(Endpoint.TENANT_SCOPE_GROUPS)
    }

tenant_group_roles = {
    'item_title':         EndpointHelper.get_name(Endpoint.TENANT_GROUP_ROLES),
    'url':                EndpointHelper.get_url(Endpoint.TENANT_GROUP_ROLES),
    'additional_lookup':  {
        'url':   'regex("[\w]+")',
        'field': 'code'
        },
    'resource_methods':   EndpointHelper.get_resource_methods(Endpoint.TENANT_GROUP_ROLES),
    'allowed_roles':      [EndpointHelper.get_resource_policies(Endpoint.TENANT_GROUP_ROLES)],
    'item_methods':       EndpointHelper.get_item_methods(Endpoint.TENANT_GROUP_ROLES),
    'allowed_item_roles': [EndpointHelper.get_item_policies(Endpoint.TENANT_GROUP_ROLES)],
    'schema':             EndpointHelper.get_schema(Endpoint.TENANT_GROUP_ROLES)
    }

tenants_catalogue = {
    'item_title':            EndpointHelper.get_name(Endpoint.TENANTS),
    'url':                   EndpointHelper.get_url(Endpoint.TENANTS),
    'extra_response_fields': [EndpointVar.__TENANT_ID__],
    'resource_methods':      EndpointHelper.get_resource_methods(Endpoint.TENANTS),
    'allowed_roles':         [EndpointHelper.get_resource_policies(Endpoint.TENANTS)],
    'item_methods':          [],
    'schema':                EndpointHelper.get_schema(Endpoint.TENANTS)
    }

tenant = {
    'item_title':            EndpointHelper.get_name(Endpoint.TENANTS),
    'url':                   EndpointHelper.get_url(Endpoint.TENANTS),
    'item_lookup_field':     EndpointVar.__TENANT_ID__,
    'item_url':              EndpointVar.__TENANT_ID_FMT__,
    'extra_response_fields': [EndpointVar.__TENANT_ID__],
    'resource_methods':      [],
    'item_methods':          EndpointHelper.get_item_methods(Endpoint.TENANTS),
    'allowed_item_roles':    [EndpointHelper.get_item_policies(Endpoint.TENANTS)],
    'schema':                tenants_catalogue['schema'],
    'datasource':            {
        'source': 'tenants_catalogue'
        }
    }

tenant_users_catalogue = {
    'item_title':            EndpointHelper.get_name(Endpoint.TENANT_USERS),
    'url':                   EndpointHelper.get_url(Endpoint.TENANT_USERS),
    'extra_response_fields': [EndpointVar.__USER_ID__],
    'resource_methods':      EndpointHelper.get_resource_methods(Endpoint.TENANT_USERS),
    'allowed_roles':         [EndpointHelper.get_resource_policies(Endpoint.TENANT_USERS)],
    'item_methods':          [],
    'schema':                EndpointHelper.get_schema(Endpoint.TENANT_USERS)
    }

tenant_user = {
    'item_title':            EndpointHelper.get_name(Endpoint.TENANT_USERS),
    'url':                   EndpointHelper.get_url(Endpoint.TENANT_USERS),
    'item_lookup_field':     EndpointVar.__USER_ID__,
    'item_url':              EndpointVar.__USER_ID_FMT__,
    'extra_response_fields': [EndpointVar.__USER_ID__],
    'resource_methods':      [],
    'item_methods':          EndpointHelper.get_item_methods(Endpoint.TENANT_USERS),
    'allowed_item_roles':    [EndpointHelper.get_item_policies(Endpoint.TENANT_USERS)],
    'schema':                tenant_users_catalogue['schema'],
    'datasource':            {
        'source': 'tenant_users_catalogue'
        }
    }

vnsfs_catalogue = {
    'item_title':            EndpointHelper.get_name(Endpoint.VNSFS),
    'url':                   EndpointHelper.get_url(Endpoint.VNSFS),
    'extra_response_fields': [EndpointVar.__USER_ID__],
    'resource_methods':      EndpointHelper.get_resource_methods(Endpoint.VNSFS),
    'allowed_roles':         [EndpointHelper.get_resource_policies(Endpoint.VNSFS)],
    'item_methods':          [],
    'schema':                EndpointHelper.get_schema(Endpoint.VNSFS)
    }

vnsf = {
    'item_title':            EndpointHelper.get_name(Endpoint.VNSFS),
    'url':                   EndpointHelper.get_url(Endpoint.VNSFS),
    'item_lookup_field':     EndpointVar.__USER_ID__,
    'item_url':              EndpointVar.__USER_ID_FMT__,
    'extra_response_fields': [EndpointVar.__USER_ID__],
    'resource_methods':      [],
    'item_methods':          EndpointHelper.get_item_methods(Endpoint.VNSFS),
    'allowed_item_roles':    [EndpointHelper.get_item_policies(Endpoint.VNSFS)],
    'schema':                vnsfs_catalogue['schema'],
    'datasource':            {
        'source': 'vnsfs_catalogue'
        }
    }

nss_catalogue = {
    'item_title':         'nss_catalogue',
    'url':                'catalogue/tenants/<regex(".*"):tenant_id>/nss',
    'resource_methods':   ['POST', 'GET'],
    'allowed_roles':      [{'POST': 'nss_catalogue:create', 'GET': 'nss_catalogue:read'}],
    'item_methods':       ['GET', 'PUT', 'DELETE'],
    'allowed_item_roles': [
        {'GET': 'nss_catalogue:read_ns', 'PUT': 'nss_catalogue:update_ns', 'DELETE': 'nss_catalogue:delete_ns'}],
    'schema':             api_model.nss_catalogue_model
    }

nss_inventory = {
    'item_title':         'nss_inventory',
    'url':                'inventory/tenants/<regex(".*"):tenant_id>/nss',
    'resource_methods':   ['POST', 'GET'],
    'allowed_roles':      [{'POST': 'nss_inventory:create', 'GET': 'nss_inventory:read'}],
    'item_methods':       ['GET', 'PUT', 'DELETE'],
    'allowed_item_roles': [
        {'GET': 'nss_inventory:read_ns', 'PUT': 'nss_inventory:update_ns', 'DELETE': 'nss_catalogue:delete_ns'}],
    'schema':             api_model.nss_inventory_model
    }
