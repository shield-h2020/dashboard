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


policy_model = {
    # The tenant to whom the policy is for.
    'tenant_id':      {
        'description': 'Description of the user resource',
        'type':        'string',
        'empty':       False,
        'required':    True
        },

    # The vNSF instance ID where the policy should be applied.
    'vnsf_id':        {
        'description': 'Description of the user resource',
        'type':        'string',
        'empty':       False,
        'required':    True
        },

    # Time and date when the thread was detected. Format: ISO 8601.
    'detection':      {
        # This field should be of type datetime. The problem here is that datetime isn't JSON serializable so a
        # string must be sent. The trick is to convert the string to a datetime instance in a hook function.
        # The string type caters for the serialization to JSON so the type must match or Cerberus won't validate it
        # and so it never gets to the hook function. Once it gets to the hook function it is converted to datetime
        # and stored. Storing as datetime doesn't seem to be a problem as pymongo doesn't check the instance type (
        # the assumption is that it was previously validated by Cerberus so it won't check it again).
        # This is not the most elegant hack but it seems the most adequate given the constraints.
        'type':     'string',
        'empty':    False,
        'required': True
        },

    # The severity assigned to the threat. Format: user-defined.
    'severity':       {
        'type':     'integer',
        'empty':    False,
        'required': True
        },

    # The applicability of the policy for the tenant in question. Format: user-defined.
    'status':         {
        'type':     'string',
        'empty':    False,
        'required': True
        },

    # The kind of network attack. Format: user-defined.
    'attack':         {
        'type':     'string',
        'empty':    False,
        'required': True
        },

    # The recommendation to counter the threat. Format: user-defined.
    'recommendation': {
        'type':     'string',
        'empty':    False,
        'required': True
        }
    }

tenant_scopes_model = {
    'name':        {
        'description': 'A user friendly name to set for the scope',
        'type':        'string',
        'empty':       False,
        'required':    True
        },

    'code':        {
        'description': 'A user-defined identification used for lookup purposes',
        'type':        'string',
        'empty':       False,
        'required':    True
        },

    'description': {
        'description': 'Additional information on the scope',
        'type':        'string'
        }
    }

tenant_groups_model = {
    'name':        {
        'description': 'A user friendly name to set for the group',
        'type':        'string',
        'empty':       False,
        'required':    True
        },

    'code':        {
        'description': 'A user-defined identification used for lookup purposes',
        'type':        'string',
        'empty':       False,
        'required':    True
        },

    'description': {
        'description': 'Additional information on the group',
        'type':        'string'
        }
    }

tenant_roles_model = {
    'name':        {
        'description': 'A user friendly name to set for the group',
        'type':        'string',
        'empty':       False,
        'required':    True
        },

    'code':        {
        'description': 'A user-defined identification used for lookup purposes',
        'type':        'string',
        'empty':       False,
        'required':    True
        },

    'aaa_id':      {
        'description': 'The ID from the AAA system. Filled once the role is automatically created in the AAA system.',
        'type':        'string'
        },

    'description': {
        'description': 'Additional information on the group',
        'type':        'string'
        }
    }

tenant_scope_groups_model = {
    'name':     {
        'description': 'A user friendly name to set for the scope/groups association',
        'type':        'string',
        'empty':       False,
        'required':    True
        },

    'code':     {
        'description': 'A user-defined identification used for lookup purposes',
        'type':        'string',
        'empty':       False,
        'required':    True
        },

    'scope_id': {
        'description': 'The scope ID to whom the groups are associated with',
        'type':        'objectid',
        'empty':       False,
        'required':    True
        },

    'groups':   {
        'description': 'The group(s) associated with the scope',
        'type':        ['objectid', 'list'],
        'empty':       False,
        'required':    True
        }
    }

tenant_group_roles_model = {
    'name':     {
        'description': 'A user friendly name to set for the group/roles association',
        'type':        'string',
        'empty':       False,
        'required':    True
        },

    'code':     {
        'description': 'A user-defined identification used for lookup purposes',
        'type':        'string',
        'empty':       False,
        'required':    True
        },

    'group_id': {
        'description': 'The group ID to whom the roles are associated with',
        'type':        'objectid',
        'empty':       False,
        'required':    True
        },

    'roles':    {
        'description': 'The role(s) associated with the group',
        'type':        ['objectid', 'list'],
        'empty':       False,
        'required':    True
        }
    }

tenant_catalogue_model = {
    # The tenant to whom the policy is for.
    'tenant_name': {
        'description': 'Description of the user resource',
        'type':        'string',
        'empty':       False,
        'required':    True
        },

    'description': {
        'type':     'string',
        'empty':    False,
        'required': True
        },

    'tenant_id':   {
        'description': 'The tenant ID from the external authorization system',
        'type':        'string'
        },

    'scope_id':    {
        'description': 'Which kind of entity the tenant holds. This is user-defined and can be named at will',
        'type':        'string'
        },

    'groups':      {
        'type':   'list',
        'schema': {
            'group': {
                'type':     'dict',
                'required': True,
                'schema':   {
                    'group_id':    {'type': 'string', 'empty': False, 'required': True},
                    'description': {'type': 'string', 'empty': False, 'required': True},
                    'domain_id':   {'type': 'string', 'empty': False, 'required': True},
                    'name':        {'type': 'string', 'empty': False, 'required': True}
                    }
                }
            }
        }
    }

tenant_users_catalogue = {
    'tenant_id':   {
        'description': 'TBD',
        'type':        'string'
        },

    'user_id':     {
        'description': 'TBD',
        'type':        'string'
        },

    'group_id':    {
        'description': 'TBD',
        'type':        'string',
        'empty':       False,
        'required':    True
        },

    'name':        {
        'description': 'TBD',
        'type':        'string',
        'empty':       False,
        'required':    True
        },

    'password':    {
        'description': 'TBD',
        'type':        'string',
        'empty':       False,
        'required':    True
        },

    'description': {
        'description': 'TBD',
        'type':        'string',
        'empty':       False,
        'required':    True
        },

    'email':       {
        'description': 'TBD',
        'type':        'string',
        'empty':       False,
        'required':    True
        }
    }

vnsfs_catalogue_model = {
    'ref_id':      {
        'description': 'The ID as defined by the system storing the vNSF',
        'type':        'string',
        'empty':       False,
        'required':    True
        },

    'custom_tags': {
        'description': 'User-defined tags',
        'type':        ['string', 'list']
        }
    }

nss_catalogue_model = {
    'ref_id':      {
        'description': 'The ID as defined by the system storing the Network Service',
        'type':        'string',
        'empty':       False,
        'required':    True
        },

    'custom_tags': {
        'description': 'User-defined tags',
        'type':        ['string', 'list']
        }
    }

nss_inventory_model = {
    'tenant_id': {
        'description': 'The tenant ID to whom the Network Service is instantiated',
        'type':        'string'
        },

    'ns_id':     {
        'description': 'The Store catalogue ID',
        'type':        'string',
        'empty':       False,
        'required':    True
        },

    'status':    {
        'type':     'string',
        'empty':    False,
        'allowed':  ["available", "configuring", "running"],
        'required': True
        },

    'instance_id': {
        'description': 'The instance id of NS when running/instantiated',
        'type':     'string',
        'empty':    True,
        'required': False
        }

    }

validations_model = {
    'result':   {
        'type':     'dict',
        'required': True,
        'schema':   {
            'error_count':   {'type': 'integer', 'empty': False, 'required': True},
            'warning_count': {'type': 'integer', 'empty': False, 'required': True},
            'issues':        {'type': 'string'}
            }
        },

    'topology': {
        'type':     'dict',
        'required': True,
        'schema':   {
            'graph': {'type': 'string'}
            }
        },

    'fwgraph':  {
        'type':     'dict',
        'required': True,
        'schema':   {
            'graph': {'type': 'string'}
            }
        },

    'log':      {
        'type': 'string'
        }
    }

notification_model = {
    "tenant_id": {
        "type":     "string",
        "empty":    False,
        "required": True
        },
    "type":      {
        "type":     "string",
        "empty":    False,
        "required": True
        },
    "data":      {
        "type":     "string",
        "empty":    False,
        "required": True
        }
    }

notification_tm_host_model = {
    # The type must be enhanced with allow unknown on its definition
    "type":      {
        "type":     "string",
        "empty":    False,
        "required": True
        }
    }

notification_tm_vnsf_model = {
    # The type must be enhanced with allow unknown on its definition
    "tenant_id": {
        "type":     "string",
        "empty":    False,
        "required": True
        },
    "time": {
        "type":     "string",
        "empty":    False,
        "required": True
        },
    "vnsfs": {
        "type":     "list",
        "empty":    False,
        "required": True,
        "schema": {
            "vnsf_id":      {
                "type":     "string",
                "empty":    False,
                "required": True
                },
            "vnsfd_name": {
                "type": "string",
                "empty": False,
                "required": True
                },
            "trust": {
                "type": "boolean",
                "empty": False,
                "required": True,
                },
            "ns_id": {
                "type": "string",
                "empty": False,
                "required": True
                },
            "container": {
                "type": "string",
                "empty": False,
                "required": True
                },
            "remediation": {
                "type": "dict",
                "empty": False,
                "required": True,
                "schema": {
                    "isolate": {'type': 'boolean'},
                    "update": {'type': 'boolean'},
                    "reboot": {'type': 'boolean'}
                    }
                }
            }
        }
    }

notification_vnsfo_model = {
    "type":      {
        "type":     "string",
        "empty":    False,
        "required": True,
        "allowed": ["ns_instance"]
        },

    "data":      {
        "type":     "dict",
        "empty":    False,
        "required": True
    }
}


tenant_ip_association = {
    "tenant_id": {
        'type':     'string',
        "empty":    False,
        "required": True
        },
    "ip":        {
        "type":     "list",
        "schema":   {"type": "ipv4address"},
        "empty":    False,
        "required": True
        }
    }

tenant_vnsf_association = {
    'tenant_id':      {
        'type':     'string',
        'empty':    False,
        'required': True,
        },
    'vnsf_instances': {
        'type':     'list',
        'schema':   {'type': 'string'},
        'empty':    False,
        'required': True
        }
    }

ns_instance_update = {
    'ns_instance_id': {
        'type':     'string',
        'empty':    False,
        'required': True
        },
    'nfvo_version': {
        'type':     'string',
        'empty':    False,
        'required': True,
        }
    }

tm_attest_all = {

}

tm_attest_node = {
    'node_id': {
        'type': 'string',
        'empty': False,
        'required': True,
    }
}

#
# Defines the fee a Developer charges for the use of its vNSF.
# The fees represented here are monthly rates.
#
billing_vnsf = {

    # The Developer that this billing definition belongs to
    'user_id': {
        'type': 'string',
        'empty': False,
        'required': True
    },

    # ID, from the catalogue, assigned to a vNSF onboarded by the Developer.
    'vnsf_id': {
        'type': 'objectid',
        'empty': False,
        'required': True,
        'unique': True

    },

    # vNSF monthly rate charged by the Developer to the ISP.
    'fee': {
        'type': 'number',
        'empty': False,
        'required': False,
        'default': 0.0
    }
}

#
# Defines the fee of an NS.
# The fees represented here are monthly rates.
#
billing_ns = {
    # ID, from the Store catalogue, assigned to the NS available to a SecaaS Client.
    'ns_id': {
        'type': 'objectid',
        'empty': False,
        'required': True,
        'unique': True
    },

    'constituent_vnsfs': {
        'type': 'list',
        'empty': False,
        'required': True,
    },

    # Calculated inherited monthly rates from the constituent vNSFs (OpEx)
    'expense_fee': {
        'type': 'number',
        'empty': False,
        'required': True
    },

    # Custom fee to charge for the NS
    'fee': {
        'type': 'number',
        'empty': False,
        'required': False,
        'default': 0.0
    },
}



#
# Records the NS usage for a given SecaaS Client.
#
billing_ns_usage = {

    # Instance ID retrieved from the vNSFO upon successful instantiation
    'ns_instance_id': {
        'type': 'string',
        'empty': False,
        'required': True,
    },

    # ID, from the Store catalogue, assigned to the NS available to a SecaaS Client.
    'ns_id': {
        'type': 'string',
        'empty': False,
        'required': True
    },

    # Tenant ID using the NS.
    'tenant_id': {
        'type': 'string',
        'empty': False,
        'required': True
    },

    # Specifies if this usage is still counting, i.e. subject to be updated (open or closed)
    'usage_status': {
        'type': 'string',
        'empty': False,
        'required': True,
        'allowed': ['open', 'closed']
    },

    # # Specifies if the ns instance is terminated or running
    # 'instance_status': {
    #     'type': 'string',
    #     'empty': False,
    #     'required': True,
    #     'allowed':  ["running", "terminated"],
    # },

    # Month of billing. Format: YYYY-MM.
    'month': {
        'type': 'string',
        'empty': False,
        'required': True
    },

    # Date when the NS was instantiated by the SecaaS Client. Format: ISO 8601.
    'used_from': {
        # This field should be of type datetime. The problem here is that datetime isn't JSON serializable so a
        # string must be sent. The trick is to convert the string to a datetime instance in a hook function.
        # The string type caters for the serialization to JSON so the type must match or Cerberus won't validate it
        # and so it never gets to the hook function. Once it gets to the hook function it is converted to datetime
        # and stored. Storing as datetime doesn't seem to be a problem as pymongo doesn't check the instance type (
        # the assumption is that it was previously validated by Cerberus so it won't check it again).
        # This is not the most elegant hack but it seems the most adequate given the constraints.
        'type': 'string',
        'empty': False,
        'required': True
    },

    # Date when the NS was stopped by the SecaaS Client. Format: ISO 8601.
    'used_to': {
        # This field should be of type datetime. The problem here is that datetime isn't JSON serializable so a
        # string must be sent. The trick is to convert the string to a datetime instance in a hook function.
        # The string type caters for the serialization to JSON so the type must match or Cerberus won't validate it
        # and so it never gets to the hook function. Once it gets to the hook function it is converted to datetime
        # and stored. Storing as datetime doesn't seem to be a problem as pymongo doesn't check the instance type (
        # the assumption is that it was previously validated by Cerberus so it won't check it again).
        # This is not the most elegant hack but it seems the most adequate given the constraints.
        'type': 'string',
        'empty': False,
        'required': False
    },

    # Fee, applied at the time of instantiation, to charge for the NS usage.
    'fee': {
        'type': 'number',
        'empty': False,
        'required': True
    },

    # Reflects the monthly usage percentage which will be billable
    'billable_percentage': {
        'type': 'number',
        'empty': False,
        'required': True
    },

    # Calculated billable fee during the usage period of time of the month
    'billable_fee': {
        'type': 'number',
        'empty': False,
        'required': True
    },

}


#
# Records the vNSF usage for a given Developer.
# The amount of vNSF instances are not recorded. In contrast with Billing NS Usage,
# the Billing vNSF usage only records the periods that a particular vNSF was active/instantiated,
# regardless of the number of instances. In other words, if multiple instances of the same vNSF
# are running at the same time (period overlap) it only records the 'used_from' date of the first
# instantiation and the 'used_to' date of the last termination.
#

billing_vnsf_usage = {
    # vNSF ID, from the Store catalogue
    'vnsf_id': {
        'type': 'string',
        'empty': False,
        'required': True
    },

    # Developer that owns the vNSF
    'user_id': {
        'type': 'string',
        'empty': False,
        'required': True
    },

    # Associated 'billing_ns_usage_id' -> which ns usage this vnsf usage is refered to
    'associated_ns_usages': {
        'type': 'list',
        'empty': False,
        'required': True,
        'schema': {
            'ns_usage_id': {
                'type': 'objectid',
                'empty': False,
                'required': True,
                'data_relation': {
                     'resource': 'billing_ns_usage',
                     'field': '_id',
                     'embeddable': True
                 },
            }
        }
    },

    # Active status -> specifies if the vNSF instance is active or idle
    'usage_status': {
        'type': 'string',
        'empty': False,
        'required': True,
        'allowed':  ["active", "idle"],
    },

    # Month of billing. Format: YYYY-MM.
    'month': {
        'type': 'string',
        'empty': False,
        'required': True
    },

    # Date when the vNSF was instantiated by the SecaaS Client. Format: ISO 8601.
    'used_from': {
        # This field should be of type datetime. The problem here is that datetime isn't JSON serializable so a
        # string must be sent. The trick is to convert the string to a datetime instance in a hook function.
        # The string type caters for the serialization to JSON so the type must match or Cerberus won't validate it
        # and so it never gets to the hook function. Once it gets to the hook function it is converted to datetime
        # and stored. Storing as datetime doesn't seem to be a problem as pymongo doesn't check the instance type (
        # the assumption is that it was previously validated by Cerberus so it won't check it again).
        # This is not the most elegant hack but it seems the most adequate given the constraints.
        'type': 'string',
        'empty': False,
        'required': True
    },

    # Date when the vNSF was stopped by the SecaaS Client. Format: ISO 8601.
    'used_to': {
        # This field should be of type datetime. The problem here is that datetime isn't JSON serializable so a
        # string must be sent. The trick is to convert the string to a datetime instance in a hook function.
        # The string type caters for the serialization to JSON so the type must match or Cerberus won't validate it
        # and so it never gets to the hook function. Once it gets to the hook function it is converted to datetime
        # and stored. Storing as datetime doesn't seem to be a problem as pymongo doesn't check the instance type (
        # the assumption is that it was previously validated by Cerberus so it won't check it again).
        # This is not the most elegant hack but it seems the most adequate given the constraints.
        'type': 'string',
        'empty': False,
        'required': False
    },

    # Monthly fee, applied at the time of instantiation, to charge for the vNSF usage.
    'fee': {
        'type': 'number',
        'empty': False,
        'required': True
    },

    # Reflects the monthly usage percentage which will be billable
    'billable_percentage': {
        'type': 'number',
        'empty': False,
        'required': True
    },

    # Calculated billable fee during the usage period of time
    'billable_fee': {
        'type': 'number',
        'empty': False,
        'required': True
    },

}

#
# Defines the fee a SecaaS Client ows to the ISP for the use of a NS.
#
billing_ns_summary = {

    # Tenant ID using the NS.
    'tenant_id': {
        'type': 'string',
        'empty': False,
        'required': True,
    },

    # Month of billing. Format: YYYY-MM.
    'month': {
        'type': 'string',
        'empty': False,
        'required': True
    },

    # Number of NSs used during the month
    'number_nss': {
        'type': 'number',
        'empty': False,
        'required': True
    },

    # Number of Network Instances used during the month
    'number_ns_instances': {
        'type': 'number',
        'empty': False,
        'required': True
    },

    # Status of the billing summary (closed or open)
    'status': {
        'type': 'string',
        'empty': False,
        'required': True,
        'allowed':  ["closed", "open"],
    },

    # Fee to charge for the NS availability.
    'billable_fee': {
        'type': 'number',
        'empty': False,
        'required': True
    }
}

#
# Defines the fee the ISP ows to the Developer for the use of a vNSF.
#
billing_vnsf_summary = {

    # Developer that owns the vNSF
    'user_id': {
        'type': 'string',
        'empty': False,
        'required': True
    },

    # Month to charge. Format: YYYY-MM.
    'month': {
        'type': 'string',
        'empty': False,
        'required': True,
        'unique': True,
    },

    'number_vnsfs': {
        'type': 'number',
        'empty': False,
        'required': True,
    },

    # Specifies if this usage is still counting, i.e. subject to be updated (open or closed)
    'status': {
        'type': 'string',
        'empty': False,
        'required': True,
        'allowed': ['open', 'closed']
    },

    # Fee to charge for the vNSF availability.
    'billable_fee': {
        'type': 'number',
        'empty': False,
        'required': True
    }
}

billing_summary = {

    # Month. Format: YYYY-MM.
    'month': {
        'type': 'string',
        'empty': False,
        'required': True,
        'unique': True,
    },

    'number_tenants': {
        'type': 'number',
        'empty': False,
        'required': True,
    },

    'number_nss': {
        'type': 'number',
        'empty': False,
        'required': True,
    },

    'number_ns_instances': {
        'type': 'number',
        'empty': False,
        'required': True,
    },

    'number_vnsfs': {
        'type': 'number',
        'empty': False,
        'required': True,
    },

    'status': {
        'type': 'string',
        'empty': False,
        'required': True,
        'allowed': ['open', 'closed']
    },

    'profit_balance': {
        'type': 'number',
        'empty': False,
        'required': True,
    },
}

#
# Keeps information about billing updates which are
# typically called by the Billing Monitor Scheduler
#
billing_update = {}

#
# Keeps information about billing updates which are
# typically called for testing purposes
#
billing_clean = {
    'resources': {
        'type': 'list',
        'empty': False,
        'required': True,
    }
}

