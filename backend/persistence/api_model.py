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
    # The vNSF developer.
    'user_id': {
        'description': 'TBD',
        'type':        'string'
        },
    }

nss_catalogue_model = {
    # The tenant to whom the NS is for.
    'tenant_id': {
        'description': 'Description of the user resource',
        'type':        'string',
        'empty':       False,
        'required':    True
        }
    }

nss_inventory_model = {
    # The tenant to whom the NS is for.
    'tenant_id': {
        'description': 'Description of the user resource',
        'type':        'string',
        'empty':       False,
        'required':    True
        }
    }
