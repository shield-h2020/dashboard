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

    TENANT_SCOPES = {__NAME__:     'tenant_scopes',
                     __URL__:      'definitions/tenant_scopes',
                     __SCHEMA__:   api_model.tenant_scopes_model,
                     __RESOURCE__: {
                         __HTTP_POST__: {
                             __POLICY__: 'tenant_scopes:create',
                             __DOCS__:   {
                                 'summary':     'TBD',
                                 'description': 'TBD',
                                 'responses':   http_utils.responses_read
                                 }
                             },
                         __HTTP_GET__:  {
                             __POLICY__: 'tenant_scopes:read',
                             __DOCS__:   {
                                 'summary':     'TBD',
                                 'description': 'TBD',
                                 'responses':   http_utils.responses_read
                                 }
                             }
                         },
                     __ITEM__:     {
                         __HTTP_GET__:    {
                             __POLICY__: 'tenant_scopes:read_scope',
                             __DOCS__:   {
                                 'summary':     'TBD',
                                 'description': 'TBD',
                                 'responses':   http_utils.responses_read
                                 }
                             },
                         __HTTP_PUT__:    {
                             __POLICY__: 'tenant_scopes:update_scope',
                             __DOCS__:   {
                                 'summary':     'TBD',
                                 'description': 'TBD',
                                 'responses':   http_utils.responses_read
                                 }
                             },
                         __HTTP_DELETE__: {
                             __POLICY__: 'tenant_scopes:delete_scope',
                             __DOCS__:   {
                                 'summary':     'TBD',
                                 'description': 'TBD',
                                 'responses':   http_utils.responses_read
                                 }
                             }
                         }
                     }

    TENANT_GROUPS = {__NAME__:     'tenant_groups',
                     __URL__:      'definitions/tenant_groups',
                     __SCHEMA__:   api_model.tenant_groups_model,
                     __RESOURCE__: {
                         __HTTP_POST__: {
                             __POLICY__: 'tenant_groups:create',
                             __DOCS__:   {
                                 'summary':     'TBD',
                                 'description': 'TBD',
                                 'responses':   http_utils.responses_read
                                 }
                             },
                         __HTTP_GET__:  {
                             __POLICY__: 'tenant_groups:read',
                             __DOCS__:   {
                                 'summary':     'TBD',
                                 'description': 'TBD',
                                 'responses':   http_utils.responses_read
                                 }
                             }
                         },
                     __ITEM__:     {
                         __HTTP_GET__:    {
                             __POLICY__: 'tenant_groups:read_group',
                             __DOCS__:   {
                                 'summary':     'TBD',
                                 'description': 'TBD',
                                 'responses':   http_utils.responses_read
                                 }
                             },
                         __HTTP_PUT__:    {
                             __POLICY__: 'tenant_groups:update_group',
                             __DOCS__:   {
                                 'summary':     'TBD',
                                 'description': 'TBD',
                                 'responses':   http_utils.responses_read
                                 }
                             },
                         __HTTP_DELETE__: {
                             __POLICY__: 'tenant_groups:delete_group',
                             __DOCS__:   {
                                 'summary':     'TBD',
                                 'description': 'TBD',
                                 'responses':   http_utils.responses_read
                                 }
                             }
                         }
                     }

    TENANT_ROLES = {__NAME__:     'tenant_roles',
                    __URL__:      'definitions/tenant_roles',
                    __SCHEMA__:   api_model.tenant_roles_model,
                    __RESOURCE__: {
                        __HTTP_POST__: {
                            __POLICY__: 'tenant_roles:create',
                            __DOCS__:   {
                                'summary':     'TBD',
                                'description': 'TBD',
                                'responses':   http_utils.responses_read
                                }
                            },
                        __HTTP_GET__:  {
                            __POLICY__: 'tenant_roles:read',
                            __DOCS__:   {
                                'summary':     'TBD',
                                'description': 'TBD',
                                'responses':   http_utils.responses_read
                                }
                            }
                        },
                    __ITEM__:     {
                        __HTTP_GET__:    {
                            __POLICY__: 'tenant_roles:read_role',
                            __DOCS__:   {
                                'summary':     'TBD',
                                'description': 'TBD',
                                'responses':   http_utils.responses_read
                                }
                            },
                        __HTTP_PUT__:    {
                            __POLICY__: 'tenant_roles:update_role',
                            __DOCS__:   {
                                'summary':     'TBD',
                                'description': 'TBD',
                                'responses':   http_utils.responses_read
                                }
                            },
                        __HTTP_DELETE__: {
                            __POLICY__: 'tenant_roles:delete_role',
                            __DOCS__:   {
                                'summary':     'TBD',
                                'description': 'TBD',
                                'responses':   http_utils.responses_read
                                }
                            }
                        }
                    }

    TENANT_SCOPE_GROUPS = {__NAME__:     'tenant_scope_groups',
                           __URL__:      'definitions/tenant_scope_groups',
                           __SCHEMA__:   api_model.tenant_scope_groups_model,
                           __RESOURCE__: {
                               __HTTP_POST__: {
                                   __POLICY__: 'tenant_scope_groups:create',
                                   __DOCS__:   {
                                       'summary':     'TBD',
                                       'description': 'TBD',
                                       'responses':   http_utils.responses_read
                                       }
                                   },
                               __HTTP_GET__:  {
                                   __POLICY__: 'tenant_scope_groups:read',
                                   __DOCS__:   {
                                       'summary':     'TBD',
                                       'description': 'TBD',
                                       'responses':   http_utils.responses_read
                                       }
                                   }
                               },
                           __ITEM__:     {
                               __HTTP_GET__:    {
                                   __POLICY__: 'tenant_scope_groups:read_scope',
                                   __DOCS__:   {
                                       'summary':     'TBD',
                                       'description': 'TBD',
                                       'responses':   http_utils.responses_read
                                       }
                                   },
                               __HTTP_PUT__:    {
                                   __POLICY__: 'tenant_scope_groups:update_scope',
                                   __DOCS__:   {
                                       'summary':     'TBD',
                                       'description': 'TBD',
                                       'responses':   http_utils.responses_read
                                       }
                                   },
                               __HTTP_DELETE__: {
                                   __POLICY__: 'tenant_scope_groups:delete_scope',
                                   __DOCS__:   {
                                       'summary':     'TBD',
                                       'description': 'TBD',
                                       'responses':   http_utils.responses_read
                                       }
                                   }
                               }
                           }

    TENANT_GROUP_ROLES = {__NAME__:     'tenant_group_roles',
                          __URL__:      'definitions/tenant_group_roles',
                          __SCHEMA__:   api_model.tenant_group_roles_model,
                          __RESOURCE__: {
                              __HTTP_POST__: {
                                  __POLICY__: 'tenant_group_roles:create',
                                  __DOCS__:   {
                                      'summary':     'TBD',
                                      'description': 'TBD',
                                      'responses':   http_utils.responses_read
                                      }
                                  },
                              __HTTP_GET__:  {
                                  __POLICY__: 'tenant_group_roles:read',
                                  __DOCS__:   {
                                      'summary':     'TBD',
                                      'description': 'TBD',
                                      'responses':   http_utils.responses_read
                                      }
                                  }
                              },
                          __ITEM__:     {
                              __HTTP_GET__:    {
                                  __POLICY__: 'tenant_group_roles:read_role',
                                  __DOCS__:   {
                                      'summary':     'TBD',
                                      'description': 'TBD',
                                      'responses':   http_utils.responses_read
                                      }
                                  },
                              __HTTP_PUT__:    {
                                  __POLICY__: 'tenant_group_roles:update_role',
                                  __DOCS__:   {
                                      'summary':     'TBD',
                                      'description': 'TBD',
                                      'responses':   http_utils.responses_read
                                      }
                                  },
                              __HTTP_DELETE__: {
                                  __POLICY__: 'tenant_group_roles:delete_role',
                                  __DOCS__:   {
                                      'summary':     'TBD',
                                      'description': 'TBD',
                                      'responses':   http_utils.responses_read
                                      }
                                  }
                              }
                          }

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

    VNSFS = {__NAME__:       'vnsfs',
             __URL__:        'catalogue/vnsfs',
             __DOC_ID_VAR__: 'vnsfsId',
             __SCHEMA__:     api_model.vnsfs_catalogue_model,
             __RESOURCE__:   {
                 __HTTP_POST__: {
                     __POLICY__: 'vnsfs:create',
                     __DOCS__:   {
                         'summary':     'Registers a new vNSF',
                         'description': 'Performs the vNSF onboarding process. Upon successful completion, a new vNSF '
                                        'is added to the catalogue and associated with the Developer doing the '
                                        'onboarding operation.',
                         'responses':   http_utils.responses_read
                         }
                     },
                 __HTTP_GET__:  {
                     __POLICY__: 'vnsfs:read',
                     __DOCS__:   {
                         'summary':     'Lists vNSFs associated with a Developer',
                         'description': 'Shows all the registered vNSFs and their properties for a given Developer.',
                         'responses':   http_utils.responses_read
                         }
                     }
                 },
             __ITEM__:       {
                 __HTTP_GET__:    {
                     __POLICY__: 'vnsfs:read_vnsf',
                     __DOCS__:   {
                         'summary':     'Shows a vNSF details',
                         'description': 'Provides detailed information on a vNSF.',
                         'responses':   http_utils.responses_read
                         }
                     },
                 __HTTP_DELETE__: {
                     __POLICY__: 'vnsfs:delete_vnsf',
                     __DOCS__:   {
                         'summary':     'Decommissions a vNSF',
                         'description': 'Marks the vNSF as not available for usage.',
                         'responses':   http_utils.responses_read
                         }
                     }
                 }
             }
