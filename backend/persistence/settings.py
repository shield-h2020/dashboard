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


import api_endpoints
import os

BACKENDAPI_PORT = int(os.environ.get('BACKENDAPI_PORT', 4000))

MONGO_HOST = os.environ.get('DATASTORE_HOST', 'dashboard-persistence')
MONGO_PORT = os.environ.get('DATASTORE_PORT', 27017)
MONGO_USERNAME = os.environ.get('DATASTORE_USERNAME', 'user')
MONGO_PASSWORD = os.environ.get('DATASTORE_PASSWORD', 'user')
MONGO_DBNAME = os.environ.get('DATASTORE_DBNAME', 'shield-dashboard')

VNSFO_PROTOCOL = os.environ.get('VNSFO_PROTOCOL', 'http')
VNSFO_HOST = os.environ.get('VNSFO_HOST', '__missing_vnsfo_host__')
VNSFO_PORT = os.environ.get('VNSFO_PORT', '')
VNSFO_API = os.environ.get('VNSFO_API', '__missing_vnsfo_api_basepath__')

AAA_PROTOCOL = os.environ.get('AAA_PROTOCOL', 'http')
AAA_HOST = os.environ.get('AAA_HOST', '__missing_aaa_host__')
AAA_PORT = os.environ.get('AAA_PORT', 0)
AAA_SVC_ADMIN_SCOPE = os.environ.get('AAA_SVC_ADMIN_SCOPE', '__missing_svc_scope__')
AAA_SVC_ADMIN_USER = os.environ.get('AAA_SCV_ADMIN_USER', '__missing_svc_admin_user__')
AAA_SVC_ADMIN_PASS = os.environ.get('AAA_SCV_ADMIN_PASS', '__missing_svc_admin_user__')

# NOTE: this shall be removed once AAA is in place.
VNSFO_TENANT_ID = os.environ.get('VNSFO_TENANT_ID', '__no_tenant_set__')

X_DOMAINS = '*'  # CORS-related settings.
X_HEADERS = ['Content-Type', 'If-Match', 'Authorization', 'Shield-Authz-Scope']

# We enable standard client cache directives for all resources exposed by the
# API. We can always override these global settings later.
CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

# Date format for fields to store - ISO 8601.
DATETIME_FIELDS_INPUT_FMT = '%Y-%m-%dT%H:%M:%S'

XML = False

# Schema definition, based on Cerberus grammar. Check the Cerberus project
# (https://github.com/pyeve/cerberus) for details.

# https://github.com/pyeve/eve-swagger#description-fields-on-the-swagger-docs
TRANSPARENT_SCHEMA_RULES = True

# The DOMAIN dict explains which resources will be available and how they will
# be accessible to the API consumer.
DOMAIN = {
    'login':                  api_endpoints.login,
    'login_user':             api_endpoints.login_user,
    'tenant_scopes':          api_endpoints.tenant_scopes,
    'tenant_groups':          api_endpoints.tenant_groups,
    'tenant_roles':           api_endpoints.tenant_roles,
    'tenant_scope_groups':    api_endpoints.tenant_scope_groups,
    'tenant_group_roles':     api_endpoints.tenant_group_roles,
    'tenants_catalogue':      api_endpoints.tenants_catalogue,
    'tenant':                 api_endpoints.tenant,
    'tenant_users_catalogue': api_endpoints.tenant_users_catalogue,
    'tenant_user':            api_endpoints.tenant_user,
    'vnsfs_catalogue':        api_endpoints.vnsfs_catalogue,
    'vnsf':                   api_endpoints.vnsf,
    'nss_catalogue':          api_endpoints.nss_catalogue,
    'nss_inventory':          api_endpoints.nss_inventory,
    'ns_instance':            api_endpoints.ns_instance,
    'policies':               api_endpoints.policies,
    'policies_admin':         api_endpoints.policies_admin,
    'validations':            api_endpoints.validations,
    'notifications':          api_endpoints.notifications,
    'notifications_admin':    api_endpoints.notifications_admin,
    'tenant_ips':             api_endpoints.tenant_ip_association
    }
