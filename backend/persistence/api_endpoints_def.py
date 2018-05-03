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
from dashboardutils import http_utils
from enum import Enum


class EndpointVar(object):
    __ID_FMT__ = 'regex("[a-f0-9]*")'

    __TENANT_ID_FMT__ = __ID_FMT__
    __TENANT_ID__ = 'tenant_id'
    __TENANT_ID_URL__ = '<{}:{}>'.format(__TENANT_ID_FMT__, __TENANT_ID__)

    __USER_ID_FMT__ = __ID_FMT__
    __USER_ID__ = 'user_id'
    __USER_ID_URL__ = '<{}:{}>'.format(__USER_ID_FMT__, __USER_ID__)


class EndpointParam(object):
    __QUERY_KEYWORD__ = 'where'
    __TENANT_ID_QUERY__ = '{}={{"{}": "<id_here>"}}'.format(__QUERY_KEYWORD__, EndpointVar.__TENANT_ID__)


# TODO where query parameter should be OpenAPI 3 and JSON object
# (https://swagger.io/docs/specification/describing-parameters/#schema-vs-content-8)

class Endpoint(Enum):
    __NAME__ = 'name'
    __URL__ = 'url'
    __DOC_ID_VAR__ = 'doc_id_var'  # Used to overwrite the contents of the documentation generated for an item.
    __SCHEMA__ = 'schema'
    __RESOURCE__ = 'resource'
    __ITEM__ = 'item'
    __POLICY__ = 'policy'
    __DOCS__ = 'docs'

    __HTTP_POST__ = 'POST'
    __HTTP_GET__ = 'GET'
    __HTTP_PUT__ = 'PUT'
    __HTTP_PATCH__ = 'PATCH'
    __HTTP_DELETE__ = 'DELETE'

    TENANTS = {__NAME__:       'tenants',
               __URL__:        'catalogue/tenants',
               __DOC_ID_VAR__: 'tenantsId',
               __SCHEMA__:     api_model.tenant_catalogue_model,
               __RESOURCE__:   {
                   __HTTP_POST__: {
                       __POLICY__: 'tenants:create',
                       __DOCS__:   {
                           'summary':     'Defines a new tenant',
                           'description': 'Creates a new tenant along with the associated roles so users can be '
                                          'assigned to the tenant.',
                           'responses':   http_utils.responses_read
                           }
                       },
                   __HTTP_GET__:  {
                       __POLICY__: 'tenants:read',
                       __DOCS__:   {
                           'summary':     'Lists tenants',
                           'description': 'Shows all the available tenants along with their properties.',
                           'responses':   http_utils.responses_read
                           }
                       }
                   },
               __ITEM__:       {
                   __HTTP_GET__:    {
                       __POLICY__: 'tenants:read_tenant',
                       __DOCS__:   {
                           'summary':     'Shows a tenant details',
                           'description': 'Provides detailed information on a tenant.',
                           'responses':   http_utils.responses_read
                           }
                       },
                   __HTTP_PUT__:    {
                       __POLICY__: 'tenants:update_tenant',
                       __DOCS__:   {
                           'summary':     'Updates a tenant',
                           'description': 'Updates the details on a tenant.',
                           'responses':   http_utils.responses_read
                           }
                       },
                   __HTTP_DELETE__: {
                       __POLICY__: 'tenants:delete_tenant',
                       __DOCS__:   {
                           'summary':     'Defines a new tenant',
                           'description': 'Creates a new tenant.',
                           'responses':   http_utils.responses_read
                           }
                       }
                   }
               }

    TENANT_USERS = {__NAME__:       'tenant_users',
                    __URL__:        'catalogue/users',
                    __DOC_ID_VAR__: 'tenant_usersId',
                    __SCHEMA__:     api_model.tenant_users_catalogue,
                    __RESOURCE__:   {
                        __HTTP_POST__: {
                            __POLICY__: 'tenant_users:create',
                            __DOCS__:   {
                                'summary':     'Defines a new tenant',
                                'description': 'Creates a new tenant.',
                                'responses':   http_utils.responses_read
                                }
                            },
                        __HTTP_GET__:  {
                            __POLICY__: 'tenant_users:read',
                            __DOCS__:   {
                                'summary':     'Defines a new tenant',
                                'description': 'Creates a new tenant.',
                                'responses':   http_utils.responses_read
                                }
                            }
                        },
                    __ITEM__:       {
                        __HTTP_GET__:    {
                            __POLICY__: 'tenant_users:read_user',
                            __DOCS__:   {
                                'summary':     'Defines a new tenant',
                                'description': 'Creates a new tenant.',
                                'parameters':  [
                                    {
                                        'in':          'query',
                                        'name':        EndpointParam.__QUERY_KEYWORD__,
                                        'required':    True,
                                        'description': 'Tenant ID where to look for the user. Format: ' +
                                                       EndpointParam.__TENANT_ID_QUERY__,
                                        'type':        'string'
                                        }],
                                'responses':   http_utils.responses_read
                                }
                            },
                        __HTTP_PUT__:    {
                            __POLICY__: 'tenant_users:update_user',
                            __DOCS__:   {
                                'summary':     'Defines a new tenant',
                                'description': 'Creates a new tenant.',
                                'responses':   http_utils.responses_read
                                }
                            },
                        __HTTP_PATCH__:  {
                            __POLICY__: 'tenant_users:update_user',
                            __DOCS__:   {
                                'summary':     'Defines a new tenant',
                                'description': 'Creates a new tenant.',
                                'responses':   http_utils.responses_read
                                }
                            },
                        __HTTP_DELETE__: {
                            __POLICY__: 'tenant_users:delete_user',
                            __DOCS__:   {
                                'summary':     'Defines a new tenant',
                                'description': 'Creates a new tenant.',
                                'responses':   http_utils.responses_read
                                }
                            }
                        }
                    }
