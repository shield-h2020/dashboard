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


from enum import Enum
import api_model
from dashboardutils import http_utils


class EndpointVar(object):
    __ID_FMT__ = 'regex("[a-f0-9]*")'

    __TENANT_ID_FMT__ = __ID_FMT__
    __TENANT_ID__ = 'tenant_id'
    __TENANT_ID_URL__ = '<{}:{}>'.format(__TENANT_ID_FMT__, __TENANT_ID__)

    __USER_ID_FMT__ = __ID_FMT__
    __USER_ID__ = 'user_id'
    __USER_ID_URL__ = '<{}:{}>'.format(__USER_ID_FMT__, __USER_ID__)

    __NS_ID_FMT__ = __ID_FMT__
    __NS_ID__ = 'ns_id'
    __NS_ID_URL__ = '<{}:{}>'.format(__NS_ID_FMT__, __NS_ID__)


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

    VNSFS_CATALOGUE = {__NAME__:       'vnsfs',
                       __URL__:        'catalogue/vnsfs',
                       __DOC_ID_VAR__: 'nssId',
                       __SCHEMA__:     api_model.nss_catalogue_model,
                       __RESOURCE__:   {
                           __HTTP_POST__: {
                               __POLICY__: 'vnsfs_catalogue:create',
                               __DOCS__:   {
                                   'summary':     'Registers a new vNSF',
                                   'description': 'Performs the vNSF onboarding process. Upon successful completion, '
                                                  'a new vNSF '
                                                  'is added to the catalogue and associated with the Developer doing '
                                                  'the '
                                                  'onboarding operation.',
                                   'responses':   http_utils.responses_read
                                   }
                               },
                           __HTTP_GET__:  {
                               __POLICY__: 'vnsfs_catalogue:read',
                               __DOCS__:   {
                                   'summary':     'Lists vNSFs associated with a Developer',
                                   'description': 'Shows all the registered vNSFs and their properties for a given '
                                                  'Developer.',
                                   'responses':   http_utils.responses_read
                                   }
                               }
                           },
                       __ITEM__:       {
                           __HTTP_GET__:    {
                               __POLICY__: 'vnsfs_catalogue:read_vnsf',
                               __DOCS__:   {
                                   'summary':     'Shows a vNSF details',
                                   'description': 'Provides detailed information on a vNSF.',
                                   'responses':   http_utils.responses_read
                                   }
                               },
                           __HTTP_DELETE__: {
                               __POLICY__: 'vnsfs_catalogue:delete_vnsf',
                               __DOCS__:   {
                                   'summary':     'Decommissions a vNSF',
                                   'description': 'Marks the vNSF as not available for usage.',
                                   'responses':   http_utils.responses_read
                                   }
                               }
                           }
                       }

    NSS_CATALOGUE = {__NAME__:       'nss',
                     __URL__:        'catalogue/nss',
                     __DOC_ID_VAR__: 'nssId',
                     __SCHEMA__:     api_model.nss_catalogue_model,
                     __RESOURCE__:   {
                         __HTTP_POST__: {
                             __POLICY__: 'nss_catalogue:create',
                             __DOCS__:   {
                                 'summary':     'Registers a new NS',
                                 'description': 'Performs the NS onboarding process. Upon successful completion, '
                                                'a new NS '
                                                'is added to the catalogue and associated with the Developer doing the '
                                                'onboarding operation.',
                                 'responses':   http_utils.responses_read
                                 }
                             },
                         __HTTP_GET__:  {
                             __POLICY__: 'nss_catalogue:read',
                             __DOCS__:   {
                                 'summary':     'Lists NSs associated with a Developer',
                                 'description': 'Shows all the registered NSs and their properties for a given '
                                                'Developer.',
                                 'responses':   http_utils.responses_read
                                 }
                             }
                         },
                     __ITEM__:       {
                         __HTTP_GET__:    {
                             __POLICY__: 'nss_catalogue:read_ns',
                             __DOCS__:   {
                                 'summary':     'Shows a NS details',
                                 'description': 'Provides detailed information on a NS.',
                                 'responses':   http_utils.responses_read
                                 }
                             },
                         __HTTP_DELETE__: {
                             __POLICY__: 'nss_catalogue:delete_ns',
                             __DOCS__:   {
                                 'summary':     'Decommissions a NS',
                                 'description': 'Marks the NS as not available for usage.',
                                 'responses':   http_utils.responses_read
                                 }
                             }
                         }
                     }

    NSS_INVENTORY = {__NAME__:       'nss_inventory',
                     __URL__:        'inventory/nss',
                     __DOC_ID_VAR__: 'nssId',
                     __SCHEMA__:     api_model.nss_inventory_model,
                     __RESOURCE__:   {
                         __HTTP_POST__: {
                             __POLICY__: 'nss_inventory:create',
                             __DOCS__:   {
                                 'summary':     'Enrolls a NS in the inventory',
                                 'description': 'Performs the enrollment of a NS to the inventory',
                                 'responses':   http_utils.responses_read
                                 }
                             },
                         __HTTP_GET__:  {
                             __POLICY__: 'nss_inventory:read',
                             __DOCS__:   {
                                 'summary':     'Lists all NSs in the inventory',
                                 'description': 'Shows all the NSs registered in the inventory',
                                 'responses':   http_utils.responses_read
                                 }
                             }
                         },
                     __ITEM__:       {
                         __HTTP_GET__:    {
                             __POLICY__: 'nss_inventory:read_ns',
                             __DOCS__:   {
                                 'summary':     'Obtains a NS from inventory',
                                 'description': 'Provides detailed information of a NS in inventory',
                                 'responses':   http_utils.responses_read
                                 }
                             },
                         __HTTP_DELETE__: {
                             __POLICY__: 'nss_inventory:delete_ns',
                             __DOCS__:   {
                                 'summary':     'Withdraws a NS from inventory',
                                 'description': 'Removes a NS from the inventory',
                                 'responses':   http_utils.responses_read
                                 }
                             },
                         __HTTP_PATCH__: {
                             __POLICY__: 'nss_inventory:update_ns',
                             __DOCS__: {
                                 'summary': 'Updated a NS in the inventory',
                                 'description': 'Changes information of a NS in inventory, namely its status',
                                 'responses': http_utils.responses_read
                                 }
                             }
                         }

                     }

    NSS_INSTANTIATE = {__NAME__:  'nss_instantiate',
                       __URL__:        'nss/instantiate',
                       __DOC_ID_VAR__: 'nssId',
                       __SCHEMA__:     api_model.nss_inventory_model,
                       __RESOURCE__:   {},
                       __ITEM__:       {
                           __HTTP_PATCH__:    {
                               __POLICY__: 'nss_instantiate:update_ns',
                               __DOCS__:   {
                                   'summary':     'Instantiate a Network Service',
                                   'description': 'Instantiate a Network Service in the Orchestrator',
                                   'responses':   http_utils.responses_read
                                   }
                               }
                           }
                       }

    NSS_TERMINATE = {__NAME__: 'nss_terminate',
                     __URL__: 'nss/terminate',
                     __DOC_ID_VAR__: 'nssId',
                     __SCHEMA__: api_model.nss_inventory_model,
                     __RESOURCE__: {},
                     __ITEM__: {
                         __HTTP_PATCH__: {
                             __POLICY__: 'nss_terminate:update_ns',
                             __DOCS__: {
                                 'summary': 'Terminate a Network Service',
                                 'description': 'Terminate a Network Service in the Orchestrator',
                                 'responses': http_utils.responses_read
                                 }
                             }
                         }
                     }

    VALIDATION = {__NAME__:     'validations',
                  __URL__:      'validations',
                  # __DOC_ID_VAR__: 'tenantsId',
                  __SCHEMA__:   api_model.validations_model,
                  __RESOURCE__: {
                      __HTTP_POST__: {
                          __POLICY__: 'validations:create',
                          __DOCS__:   {
                              'summary':     'Defines a new tenant',
                              'description': 'Creates a new tenant along with the associated roles so users can be '
                                             'assigned to the tenant.',
                              'responses':   http_utils.responses_read
                              }
                          },
                      __HTTP_GET__:  {
                          __POLICY__: 'validations:read',
                          __DOCS__:   {
                              'summary':     'Lists tenants',
                              'description': 'Shows all the available tenants along with their properties.',
                              'responses':   http_utils.responses_read
                              }
                          }
                      },
                  __ITEM__:     {
                      __HTTP_GET__:    {
                          __POLICY__: 'validations:read_validation',
                          __DOCS__:   {
                              'summary':     'Shows a tenant details',
                              'description': 'Provides detailed information on a tenant.',
                              'responses':   http_utils.responses_read
                              }
                          },
                      __HTTP_PUT__:    {
                          __POLICY__: 'validations:update_validation',
                          __DOCS__:   {
                              'summary':     'Updates a tenant',
                              'description': 'Updates the details on a tenant.',
                              'responses':   http_utils.responses_read
                              }
                          },
                      __HTTP_DELETE__: {
                          __POLICY__: 'validations:delete_validation',
                          __DOCS__:   {
                              'summary':     'Defines a new tenant',
                              'description': 'Creates a new tenant.',
                              'responses':   http_utils.responses_read
                              }
                          }
                      }
                  }

    TM_ATTEST = {__NAME__:         'tm_attest',
                __URL__:           'tm/attest',
                __SCHEMA__: api_model.tm_attest_node,
                __RESOURCE__: {
                    __HTTP_POST__: {
                        __POLICY__: 'tm_attest:trigger',
                        __DOCS__: {
                            'summary': 'On-demand Attestation of a node',
                            'description': 'Performs the attestation of a specific node',
                            'responses': http_utils.responses_read
                        }
                    },
                }
    }

    TM_ATTEST_ALL = {
                __NAME__:         'tm_attest_all',
                __URL__:           'tm/attest/all',
                __SCHEMA__: api_model.tm_attest_all,
                __RESOURCE__: {
                    __HTTP_POST__: {
                        __POLICY__: 'tm_attest:trigger',
                        __DOCS__: {
                            'summary': 'On-demand Attestation',
                            'description': 'Performs the attestation of all active nodes',
                            'responses': http_utils.responses_read
                        }
                    },
                }
    }

    BILLING_NS = {
        __NAME__: 'network service billing',
        __URL__: 'billing/ns',
        __SCHEMA__: api_model.billing_ns,
        __RESOURCE__: {
            __HTTP_POST__: {
                __POLICY__: 'billing_ns:create',
                __DOCS__: {
                    'summary': 'Establish billing fees for a Network Service',
                    'description': 'Establish billing fees, namely the additional fee, for a particular Network Service',
                    'responses': http_utils.responses_read
                }
            },
            __HTTP_GET__: {
                __POLICY__: 'billing_ns:read',
                __DOCS__: {
                    'summary': 'Obtains the billing fees of a Network Service',
                    'description': 'Obtains the billing fees of a all Network Services',
                    'responses': http_utils.responses_read
                }
            },
            __HTTP_DELETE__: {
                __POLICY__: 'billing_ns:delete',
                __DOCS__: {
                    'summary': 'Delete ALL billing_ns (TEST PURPOSES)',
                    'description': 'Delete ALL billing_ns (TEST PURPOSES)',
                    'responses': http_utils.responses_read
                }
            }

        },
        __ITEM__: {
            __HTTP_GET__: {
                __POLICY__: 'billing_ns:read',
                __DOCS__: {
                    'summary': 'Obtains the billing fees for a particular Network Service',
                    'description': 'Obtains the billing fees of a particular Network Service',
                    'responses': http_utils.responses_read
                }
            },
            __HTTP_PATCH__: {
                __POLICY__: 'billing_ns:update',
                __DOCS__: {
                    'summary': 'Updates the billing fees of a Network Service',
                    'description': 'Updates the `additional_fee` of a particular Network Service',
                    'responses': http_utils.responses_read
                }
            },
            __HTTP_DELETE__: {
                __POLICY__: 'billing_ns:delete',
                __DOCS__: {
                    'summary': 'Remove a billing fee record of a Network Service',
                    'description': 'Remove billing fee record of a Network Service',
                    'responses': http_utils.responses_read
                }
            },
        }

    }

    BILLING_VNSF = {
        __NAME__: 'vnsf billing',
        __URL__: 'billing/vnsf',
        __SCHEMA__: api_model.billing_vnsf,
        __RESOURCE__: {
            __HTTP_POST__: {
                __POLICY__: 'billing_vnsf:create',
                __DOCS__: {
                    'summary': 'Establish billing fees for a vNSF',
                    'description': 'Establish billing fees, namely the fee and support_fee, for a particular vNSF',
                    'responses': http_utils.responses_read
                }
            },
            __HTTP_GET__: {
                __POLICY__: 'billing_vnsf:read',
                __DOCS__: {
                    'summary': 'Obtains the billing fees for a vNSF',
                    'description': 'Obtains the billing fees (fee and support fee) for a particular vNSF',
                    'responses': http_utils.responses_read
                }
            },
            __HTTP_DELETE__: {
                __POLICY__: 'billing_vnsf:delete',
                __DOCS__: {
                    'summary': 'Delete ALL billing_vnsf (TEST PURPOSES)',
                    'description': 'Delete ALL billing_vnsf (TEST PURPOSES)',
                    'responses': http_utils.responses_read
                }
            }
        },
        __ITEM__: {
            __HTTP_GET__: {
                __POLICY__: 'billing_vnsf:read',
                __DOCS__: {
                    'summary': 'Obtains the billing fees for a vNSF',
                    'description': 'Obtains the billing fees (fee and support fee) for a particular vNSF',
                    'responses': http_utils.responses_read
                }
            },
            __HTTP_PATCH__: {
                __POLICY__: 'billing_vnsf:update',
                __DOCS__: {
                    'summary': 'Updates the billing fees of a vNSF',
                    'description': 'Updates the billing fees, namely the fee and support fee, of a particular vNSF',
                    'responses': http_utils.responses_read
                }
            },
            __HTTP_DELETE__: {
                __POLICY__: 'billing_vnsf:delete',
                __DOCS__: {
                    'summary': 'Remove a billing fee record of a vNSF',
                    'description': 'Remove billing fee record of a vNSF',
                    'responses': http_utils.responses_read
                }
            }
        }
    }
    #
    # BILLING_USAGE = {
    #     __NAME__: 'admin billing usage',
    #     __URL__: 'billing/usage',
    #     __SCHEMA__: api_model.billing_usage,
    #     __RESOURCE__: {
    #         __HTTP_GET__: {
    #             __POLICY__: 'billing_usage:read',
    #             __DOCS__: {
    #                 'summary': 'Obtains the general administration billing usage counters for NSs and vNSFs.',
    #                 'description': 'Obtains the general administration billing usage counters for NSs and vNSFs.',
    #                 'responses': http_utils.responses_read
    #             }
    #         }
    #     }
    # }


    BILLING_NS_USAGE = {
        __NAME__: 'start ns instance billing usage',
        __URL__: 'billing/ns/usage',
        __SCHEMA__: api_model.billing_ns_usage,
        __RESOURCE__: {
            __HTTP_GET__: {
                __POLICY__: 'billing_ns_usage:read',
                __DOCS__: {
                    'summary': 'Obtains the billing usage counters for all Network Service Instance',
                    'description': 'Obtains the start and stop dates of billing of NS instances',
                    'responses': http_utils.responses_read
                }
            },
            __HTTP_POST__: {
                __POLICY__: 'billing_ns_usage:create',
                __DOCS__: {
                    'summary': 'Create billing usage counters a Network Service Instance',
                    'description': 'Create billing usage counters a Network Service Instance.',
                    'responses': http_utils.responses_read
                }
            },
            __HTTP_DELETE__: {
                __POLICY__: 'billing_ns_usage:delete',
                __DOCS__: {
                    'summary': 'Delete ALL billing_ns_usage (TEST PURPOSES)',
                    'description': 'Delete ALL billing_ns_usage (TEST PURPOSES)',
                    'responses': http_utils.responses_read
                }
            }
        },
        __ITEM__: {
            __HTTP_GET__: {
                __POLICY__: 'billing_ns_usage:read',
                __DOCS__: {
                    'summary': 'Obtains the billing usage counters for a Network Service Instance',
                    'description': 'Obtains the start and stop dates of billing of particular NS instance',
                    'responses': http_utils.responses_read
                }
            },
            __HTTP_PATCH__: {
                __POLICY__: 'billing_ns_usage:update',
                __DOCS__: {
                    'summary': 'Updates the billing usage counters for a Network Service Instance',
                    'description': 'Updates the billing usage counters for a Network Service Instance.',
                    'responses': http_utils.responses_read
                }
            },

            __HTTP_DELETE__: {
                __POLICY__: 'billing_ns_usage:delete',
                __DOCS__: {
                    'summary': 'Remove a billing usage record of a Network Service',
                    'description': 'Remove a billing usage record of a Network Service',
                    'responses': http_utils.responses_read
                }
            }
        }
    }

    BILLING_VNSF_USAGE = {
        __NAME__: 'start vnsf billing usage',
        __URL__: 'billing/vnsf/usage',
        __SCHEMA__: api_model.billing_vnsf_usage,
        __RESOURCE__: {
            __HTTP_GET__: {
                __POLICY__: 'billing_vnsf_usage:read',
                __DOCS__: {
                    'summary': 'Obtains the billing usage counters for vNSFs',
                    'description': 'Obtains the billing usage counters for vNSFs',
                    'responses': http_utils.responses_read
                }
            },
            __HTTP_POST__: {
                __POLICY__: 'billing_vnsf_usage:create',
                __DOCS__: {
                    'summary': 'Create billing usage counters for vNSFs',
                    'description': 'Create billing usage counters for vNSFs',
                    'responses': http_utils.responses_read
                }
            },
            __HTTP_DELETE__: {
                __POLICY__: 'billing_vnsf_usage:delete',
                __DOCS__: {
                    'summary': 'Delete ALL billing_vnsf_usage (TEST PURPOSES)',
                    'description': 'Delete ALL billing_vnsf_usage (TEST PURPOSES)',
                    'responses': http_utils.responses_read
                }
            }
        },
        __ITEM__: {
            __HTTP_GET__: {
                __POLICY__: 'billing_vnsf_usage:read',
                __DOCS__: {
                    'summary': 'Obtains the billing usage counters for a particular vNSFs',
                    'description': 'Obtains the billing usage counters for a particular vNSFs',
                    'responses': http_utils.responses_read
                }
            },
            __HTTP_PATCH__: {
                __POLICY__: 'billing_vnsf_usage:update',
                __DOCS__: {
                    'summary': 'Updates the billing usage counters for a particular vNSF',
                    'description': 'Updates the billing usage counters for a particular vNSF',
                    'responses': http_utils.responses_read
                }
            },
            __HTTP_DELETE__: {
                __POLICY__: 'billing_vnsf_usage:delete',
                __DOCS__: {
                    'summary': 'Remove a billing usage record of a particular vNSF',
                    'description': 'Remove a billing usage record of a particular vNSF (TEST ONLY)',
                    'responses': http_utils.responses_read
                }
            }
        }
    }

    BILLING_NS_START_USAGE = {
        __NAME__: 'start ns instance billing usage',
        __URL__: 'billing/ns/start',
        __SCHEMA__: api_model.billing_ns_usage,
        __RESOURCE__: {
            __HTTP_POST__: {
                __POLICY__: 'billing_ns_usage:start',
                __DOCS__: {
                    'summary': 'Start billing usage counters for a Network Service Instance',
                    'description': 'Registers the start date of billing of particular NS instance',
                    'responses': http_utils.responses_read
                }
            }
        },
    }

    BILLING_NS_STOP_USAGE = {
        __NAME__: 'stop ns instance billing usage',
        __URL__: 'billing/ns/stop',
        __SCHEMA__: api_model.billing_ns_usage,
        __RESOURCE__: {},
        __ITEM__: {
            __HTTP_PATCH__: {
                __POLICY__: 'billing_ns_usage:stop',
                __DOCS__: {
                    'summary': 'Stop billing usage counters for a Network Service Instance',
                    'description': 'Registers the stop date of billing on a particular NS instance',
                    'responses': http_utils.responses_read
                }
            }
        }
    }

    BILLING_VNSF_START_USAGE = {
        __NAME__: 'start vNSF billing usage',
        __URL__: 'billing/vnsf/start',
        __SCHEMA__: api_model.billing_vnsf_usage,
        __RESOURCE__: {
            __HTTP_POST__: {
                __POLICY__: 'billing_vnsf_usage:start',
                __DOCS__: {
                    'summary': 'Start billing usage counters for a vNSF',
                    'description': 'Start billing usage counters for a vNSF',
                    'responses': http_utils.responses_read
                }
            }
        },
    }

    BILLING_VNSF_STOP_USAGE = {
        __NAME__: 'stop vnsf instance billing usage',
        __URL__: 'billing/vnsf/stop',
        __SCHEMA__: api_model.billing_vnsf_usage,
        __RESOURCE__: {},
        __ITEM__: {
            __HTTP_PATCH__: {
                __POLICY__: 'billing_vnsf_usage:stop',
                __DOCS__: {
                    'summary': 'Stop billing usage counters for a vNSF',
                    'description': 'Stop billing usage counters for a vNSF',
                    'responses': http_utils.responses_read
                }
            }
        }
    }

    BILLING_SUMMARY = {
        __NAME__: 'admin billing summary',
        __URL__: 'billing/summary',
        __SCHEMA__: api_model.billing_summary,
        __RESOURCE__: {
            __HTTP_GET__: {
                __POLICY__: 'billing_summary:read',
                __DOCS__: {
                    'summary': 'Obtains the general administration billing summary counters for NSs and vNSFs.',
                    'description': 'Obtains the general administration billing summary counters for NSs and vNSFs.',
                    'responses': http_utils.responses_read
                }
            },
            __HTTP_DELETE__: {
                __POLICY__: 'billing_summary:delete',
                __DOCS__: {
                    'summary': 'Delete ALL billing_summary (TEST PURPOSES)',
                    'description': 'Delete ALL billing_summary (TEST PURPOSES)',
                    'responses': http_utils.responses_read
                }
            }
        },
        __ITEM__: {
            __HTTP_PATCH__: {
                __POLICY__: 'billing_summary:update',
                __DOCS__: {
                    'summary': 'Updates the general administration billing summary counters for NSs and vNSFs.',
                    'description': 'Updates the general administration billing summary counters for NSs and vNSFs.',
                    'responses': http_utils.responses_read
                }
            }
        }
    }

    BILLING_NS_SUMMARY = {
        __NAME__: 'Keeps record of monthly fees that SecaaS clients own to the ISP',
        __URL__: 'billing/ns/summary',
        __SCHEMA__: api_model.billing_ns_summary,
        __RESOURCE__: {
            __HTTP_GET__: {
                __POLICY__: 'billing_ns_summary:read',
                __DOCS__: {
                    'summary': 'Obtains the billing summary for all Network Service Instances',
                    'description': 'Obtains the billing summary for all Network Service Instances',
                    'responses': http_utils.responses_read
                }
            },
            __HTTP_POST__: {
                __POLICY__: 'billing_ns_summary:create',
                __DOCS__: {
                    'summary': 'Create a billing summary',
                    'description': 'Create a billing summary for a particular tenant and month',
                    'responses': http_utils.responses_read
                }
            },
            __HTTP_DELETE__: {
                __POLICY__: 'billing_ns_summary:delete',
                __DOCS__: {
                    'summary': 'Delete ALL billing_ns_summary (TEST PURPOSES)',
                    'description': 'Delete ALL billing_ns_summary (TEST PURPOSES)',
                    'responses': http_utils.responses_read
                }
            }
        },
        __ITEM__: {
            __HTTP_DELETE__: {
                __POLICY__: 'billing_ns_summary:delete',
                __DOCS__: {
                    'summary': 'Remove a billing summary record',
                    'description': 'Remove a billing summary record. (TESTS ONLY)',
                    'responses': http_utils.responses_read
                }
            }
        }
    }

    BILLING_VNSF_SUMMARY = {
        __NAME__: 'Keeps record of monthly fees that the ISP owns to Developers',
        __URL__: 'billing/vnsf/summary',
        __SCHEMA__: api_model.billing_vnsf_summary,
        __RESOURCE__: {
            __HTTP_GET__: {
                __POLICY__: 'billing_vnsf_summary:read',
                __DOCS__: {
                    'summary': 'Obtains the billing summary for all vNSFs',
                    'description': 'Obtains the billing summary for all vNSFs',
                    'responses': http_utils.responses_read
                }
            },
            __HTTP_POST__: {
                __POLICY__: 'billing_vnsf_summary:create',
                __DOCS__: {
                    'summary': 'Create a billing summary',
                    'description': 'Create a billing summary for a particular Developer and Month',
                    'responses': http_utils.responses_read
                }
            },
            __HTTP_DELETE__: {
                __POLICY__: 'billing_vnsf_summary:delete',
                __DOCS__: {
                    'summary': 'Delete ALL billing_vnsf_summary (TEST PURPOSES)',
                    'description': 'Delete ALL billing_vnsf_summary (TEST PURPOSES)',
                    'responses': http_utils.responses_read
                }
            }
        },
        __ITEM__: {
            __HTTP_DELETE__: {
                __POLICY__: 'billing_vnsf_summary:delete',
                __DOCS__: {
                    'summary': 'Remove a billing vNSF summary record',
                    'description': 'Remove a billing vNSF summary record. (TESTS ONLY)',
                    'responses': http_utils.responses_read
                }
            }
        }
    }

    BILLING_UPDATE = {
        __NAME__: 'update all billing information data',
        __URL__: 'billing/update',
        __SCHEMA__: api_model.billing_update,
        __RESOURCE__: {
            __HTTP_POST__: {
                __POLICY__: 'billing:update',
                __DOCS__: {
                    'summary': 'Update Billing Information Data',
                    'description': 'Update Billing Information Data including NS and vNSF Usages and Summaries',
                    'responses': http_utils.responses_read
                }
            },
        },
    }

    BILLING_CLEAN = {
        __NAME__: 'clean all billing information data',
        __URL__: 'billing/clean',
        __SCHEMA__: api_model.billing_clean,
        __RESOURCE__: {
            __HTTP_POST__: {
                __POLICY__: 'billing:clean',
                __DOCS__: {
                    'summary': 'Clean Billing Information Data',
                    'description': 'Clean Billing Information Data including NS and vNSF Usages and Summaries',
                    'responses': http_utils.responses_read
                }
            },
        },
    }

    BILLING_NS_SIMULATE = {
        __NAME__: 'Simulate billing fees for a particular Network Service',
        __URL__: 'billing/ns/simulate',
        __SCHEMA__: {},
        __RESOURCE__: {
            __HTTP_POST__: {
                __POLICY__: 'billing_ns:simulate',
                __DOCS__: {
                    'summary': 'Simulate billing fees for a particular Network Service',
                    'description': 'Simulate billing fees for a particular Network Service',
                    'responses': http_utils.responses_read
                }
            },
        },
    }
