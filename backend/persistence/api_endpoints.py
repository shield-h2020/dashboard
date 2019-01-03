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

"""
(NOTE: this information is based on Eve v0.7.4.)

The endpoints are crafted resorting to the definitions in the file api_endpoints_def.py.
Any endpoint that is bound to a tenant must be defined as described next. Otherwise, the checks for the Role-Based 
Access Control (RBAC) policies won't work properly.


---------------------
TL;DR

+ Define the URL to use regular expressions where the variable name to look for is defined (e.g. tenant_id instead of 
_id).

+ Define the endpoint a first time (the actual collection) with only the resource_methods and allowed_roles settings. 
The item_methods setting is an empty list.

+ Define the endpoint a second time (the document instances) with only the item_methods and allowed_item_roles. The 
resource_methods setting is an empty list. Additionally the item_lookup_field setting is defined to state the variable
name to look for, the URL changes are defined as per the first time, and the schema and datasource settings are 
defined to use the same ones as the first resource definition.  
---------------------


An endpoint definition requires some tweaks to have things working properly when the (RBAC) comes into play to 
determine whether a user is allowed to invoke the endpoint. When an invocation to an endpoint takes place, 
an authorization check is carried out. This authorization employs data present in the request such as the user ID, 
the endpoint resource ID (the /endpoint/{resource_id} path parameter), role, etc. Such data is conveyed to the 
policy check library to determine whether the endpoint is allowed for the caller.

This API delegates the authentication to an external AAA system where the tenants, groups, roles, and users are 
created. Therefore, any authentication must be done on the IDs known to the AAA system. Since such elements must also 
live in the API data model, they get created in the AAA system and its ID stored in the data model for proper lookup 
on the AAA system. This leads to having two IDs for an element which need to be used properly.

Given that pretty much all the requests to the API are associated with a tenant, the authorization check is dependent 
on inspecting the user role and usually whether it has permissions to perform the operation on the tenant it belongs 
to. Thus, all requests need to provide the AAA-system-defined tenant ID, user ID, group ID, etc. in the URL, 
even for sub-resources. This is when problems start with Eve and some tweaks are required.

Eve is hardwired to seek authorization for IDs it knows about. It does this also for sub-resources. Having an 
endpoint like /endpoint/{tenant_id}/users/{user_id} will trigger Eve to associate the tenant_id and user_id with the 
internal _id field it uses for lookups on the data model. Since the lookup needs to be on tenant_id and user_id fields 
the first tweak is done to the URL part, introducing regular expressions and variable naming (
http://python-eve.org/features.html#sub-resources) so it can provide the proper data for the authorization check. Even 
though this should work, when using sub-resources the user_id isn't retrieved by the code so proper authorization 
can't take place.

Since only one (regex) ID works, and the tenant_id is very much mandatory for authorization checks, the other option 
is to rework the endpoints. Instead of having /endpoint/{tenant_id}/users/{user_id} one now has /users/{
user_id}?where={"tenant_id": "<tenant ID>"}. This caters for the retrieval of the user_id (through URL regex) and 
also for the tenant_id. Since the lookup needs to be on the user_id field (and not on the _id one) the item_lookup_field
setting must be defined for the endpoint (http://python-eve.org/config.html#resource-item-endpoints).

Authorization checks are based on policies (https://docs.openstack.org/oslo.policy/latest) where each endpoint method 
has its associated policy. Eve provides settings to define roles, namely the resource_methods and allowed_roles for 
endpoints, and item_methods and allowed_item_roles for items. However, these settings are based on lists and don't 
provide a fine-grained control over the methods (e.g. it doesn't differentiate a PUT from a PATCH). As such, an 
additional tweak is employed where the roles have a dictionary stating the policy for each method.

All these tweaks overcome Eve limitations on using IDs from an external AAA system to check for authentication and 
having RBAC policies for authorization. Nonetheless a new issue arises, resulting from the use of different variables 
names for lookup fields and having Eve do authorization on IDs it doesn't know about. The users/{user_id} doesn't work 
properly when Eve tries to do authorization checks. Therefore a final tweak is needed.
One must define the endpoint twice. The first time is for the resource part, where the variable names change get 
defined and the resource_methods and allowed_roles settings are defined; the item methods are purposefully stated as 
unavailable. The second time is the definition for the item methods, where only the settings for the item_methods and 
allowed_item_roles are defined; the resource methods are purposefully stated as unavailable. Additionally the 
item_lookup_field setting is defined to state the variable name to look for, the URL changes are defined as per the 
first resource, and the schema and datasource settings are defined to use the same ones as the first resource 
definition.  
"""

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
    'item_title':          'policies',
    'description':         'Security recommendations',
    'schema':              api_model.policy_model,
    'resource_methods':    ['POST', 'GET'],
    'item_methods':        ['GET', 'PATCH'],

    # TODO remove once inter-component authentication is in place.
    'public_methods':      ['GET'],
    'public_item_methods': ['GET', 'PATCH']
    }

policies_admin = {
    'item_title':       'admin policies',
    'url':              'admin/policies',
    'schema':           api_model.policy_model,
    'datasource':       {
        'source': 'policies'
        },
    'resource_methods': ['POST'],
    'item_methods':     [],

    # TODO remove once inter-component authentication is in place.
    'public_methods':   ['POST']
    }



###
#  NS Instances
###

ns_instance_update = {
    'item_title': 'ns_instance_update',
    'description': 'Ns Instance Update',
    'schema': api_model.ns_instance_update,
    'resource_methods': ['POST', 'GET'],
    'item_methods': ['GET'],

    # TODO remove once inter-component authentication is in place.
    'public_methods': ['GET', 'POST'],
    'public_item_methods': ['GET']
     }


# ###
#  Notification persistence
###

notifications = {
    'item_title':          'notifications',
    'description':         'Notifications',
    'schema':              api_model.notification_model,
    'resource_methods':    ['POST', 'GET'],
    'item_methods':        ['GET', 'PATCH'],

    # TODO remove once inter-component authentication is in place.
    'public_methods':      ['GET'],
    'public_item_methods': ['GET', 'PATCH']
    }

notifications_admin = {
    'item_title':       'admin notifications',
    'url':              'admin/notifications',
    'schema':           api_model.notification_model,
    'datasource':       {
        'source': 'notifications'
        },
    'resource_methods': ['POST'],
    'item_methods':     [],

    # TODO remove once inter-component authentication is in place.
    'public_methods':   ['POST']
    }


notifications_tm_host = {
    'item_title':       'tm host notifications',
    'url':              'tm/notifications',
    'schema':              api_model.notification_tm_host_model,
    'resource_methods':    ['POST', 'GET'],
    'item_methods':        ['GET', 'PATCH'],
    'allow_unknown':    True,

    # TODO remove once inter-component authentication is in place.
    'public_methods':      ['GET'],
    'public_item_methods': ['GET', 'PATCH']
    }

distinct_notifications_tm_host = {
    'item_title':       'distinct tm host notifications',
    'url':              'tm/notifications/distinct',
    'schema':           api_model.notification_tm_host_model,
    'resource_methods': ['GET'],
    'allow_unknown':    True,
    'datasource':       {
        'source': 'notifications_tm_host',
        'default_sort': [('time', -1)],
    },

    # TODO remove once inter-component authentication is in place.
    'public_methods':   ['GET'],

}


notifications_tm_host_admin = {
    'item_title':       'admin tm host notifications',
    'url':              'admin/tm/notifications',
    'schema':           api_model.notification_tm_host_model,
    'allow_unknown':    True,
    'datasource':       {
        'source': 'notifications_tm_host'
        },
    'resource_methods': ['POST'],
    'item_methods':     [],

    # TODO remove once inter-component authentication is in place.
    'public_methods':   ['POST']
    }

notifications_tm_vnsf = {
    'item_title':           'tm vnsf notifications',
    'url':                  'tm/vnsf/notifications',
    'schema':               api_model.notification_tm_vnsf_model,
    'item_lookup_field':    EndpointVar.__TENANT_ID__,
    'item_url':             EndpointVar.__TENANT_ID_FMT__,
    'resource_methods':    ['POST', 'GET'],
    'item_methods':        ['GET', 'PATCH'],
    'allow_unknown':    True,

    # TODO remove once inter-component authentication is in place.
    'public_methods':      ['GET'],
    'public_item_methods': ['GET', 'PATCH']
    }

distinct_notifications_tm_vnsf = {
    'item_title':       'distinct tm host notifications',
    'url':              'tm/vnsf/notifications/distinct',
    'schema':           api_model.notification_tm_vnsf_model,
    'resource_methods': ['GET'],
    'allow_unknown':    True,
    'datasource':       {
        'source': 'notifications_tm_vnsf',
        'default_sort': [('time', -1)],
    },

    # TODO remove once inter-component authentication is in place.
    'public_methods':   ['GET'],
}


notifications_tm_vnsf_admin = {
    'item_title':       'admin tm vnsf notifications',
    'url':              'admin/tm/vnsf/notifications',
    'schema':           api_model.notification_tm_vnsf_model,
    'allow_unknown':    True,
    'datasource':       {
        'source': 'notifications_tm_vnsf'
        },
    'resource_methods': ['POST'],
    'item_methods':     [],

    # TODO remove once inter-component authentication is in place.
    'public_methods':   ['POST']
    }

notifications_vnsfo_admin = {
    'item_title':       'admin vnsfo notifications',
    'url':              'admin/vnsfo/notifications',
    'schema':           api_model.notification_vnsfo_model,
    'allow_unknown':    True,
    'datasource':       {
        'source': 'notifications_vnsfo'
        },
    'resource_methods': ['POST'],
    'item_methods':     [],

    # TODO remove once inter-component authentication is in place.
    'public_methods':   ['POST']
    }


tenant_ip_association = {
    'item_title':          'tenant ip association',
    'description':         "Allows the association between tenant and it's assigned IPs",
    'url':                 'tenant_ips',
    'item_lookup_field':   EndpointVar.__TENANT_ID__,
    'item_url':            EndpointVar.__TENANT_ID_FMT__,
    'schema':              api_model.tenant_ip_association,
    'resource_methods':    ['POST', 'GET'],
    'item_methods':        ['GET', 'PATCH', 'DELETE'],

    # TODO remove once inter-component authentication is in place.
    'public_methods':      ['POST', 'GET'],
    'public_item_methods': ['GET', 'PATCH', 'DELETE']
    }

tenant_vnsf_association = {
    'item_title':          'tenant vnsf association',
    'description':         "Allows the association between tenant and it's vNSFs",
    'url':                 'tenant_vnsfs',
    'item_lookup_field':   EndpointVar.__TENANT_ID__,
    'item_url':            EndpointVar.__TENANT_ID_FMT__,
    'schema':              api_model.tenant_vnsf_association,
    'resource_methods':    ['POST', 'GET'],
    'item_methods':        ['GET', 'PATCH', 'DELETE'],
    'public_methods':      ['POST', 'GET'],
    'public_item_methods': ['GET', 'PATCH', 'DELETE']
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
        },
    # TODO remove once inter-component authentication is in place.
    'public_item_methods': ['GET']
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
    'item_title':            EndpointHelper.get_name(Endpoint.VNSFS_CATALOGUE),
    'url':                   EndpointHelper.get_url(Endpoint.VNSFS_CATALOGUE),
    'extra_response_fields': [EndpointVar.__TENANT_ID__],
    'resource_methods':      EndpointHelper.get_resource_methods(Endpoint.VNSFS_CATALOGUE),
    'allowed_roles':         [EndpointHelper.get_resource_policies(Endpoint.VNSFS_CATALOGUE)],
    'item_methods':          [],
    'schema':                EndpointHelper.get_schema(Endpoint.VNSFS_CATALOGUE)
    }

vnsf = {
    'item_title':            EndpointHelper.get_name(Endpoint.VNSFS_CATALOGUE),
    'url':                   EndpointHelper.get_url(Endpoint.VNSFS_CATALOGUE),
    'item_lookup_field':     EndpointVar.__TENANT_ID__,
    'item_url':              EndpointVar.__TENANT_ID_FMT__,
    'extra_response_fields': [EndpointVar.__TENANT_ID__],
    'resource_methods':      [],
    'item_methods':          EndpointHelper.get_item_methods(Endpoint.VNSFS_CATALOGUE),
    'allowed_item_roles':    [EndpointHelper.get_item_policies(Endpoint.VNSFS_CATALOGUE)],
    'schema':                vnsfs_catalogue['schema'],
    'datasource':            {
        'source': 'vnsfs_catalogue'
        }
    }

nss_catalogue = {
    'item_title':         EndpointHelper.get_name(Endpoint.NSS_CATALOGUE),
    'url':                EndpointHelper.get_url(Endpoint.NSS_CATALOGUE),
    'resource_methods':   EndpointHelper.get_resource_methods(Endpoint.NSS_CATALOGUE),
    'allowed_roles':      [EndpointHelper.get_resource_policies(Endpoint.NSS_CATALOGUE)],
    'item_methods':       EndpointHelper.get_item_methods(Endpoint.NSS_CATALOGUE),
    'allowed_item_roles': [EndpointHelper.get_item_policies(Endpoint.NSS_CATALOGUE)],
    'schema':             EndpointHelper.get_schema(Endpoint.NSS_CATALOGUE)
    }

nss_inventory = {
    'item_title':       EndpointHelper.get_name(Endpoint.NSS_INVENTORY),
    'url':              EndpointHelper.get_url(Endpoint.NSS_INVENTORY),
    'resource_methods': EndpointHelper.get_resource_methods(Endpoint.NSS_INVENTORY),
    'allowed_roles':    [EndpointHelper.get_resource_policies(Endpoint.NSS_INVENTORY)],
    'item_methods':     [],
    'schema':           EndpointHelper.get_schema(Endpoint.NSS_INVENTORY),

     # TODO remove once inter-component authentication is in place.
    'public_methods':      ['GET'],
    }

ns_instance = {
    'item_title':         EndpointHelper.get_name(Endpoint.NSS_INVENTORY),
    'url':                EndpointHelper.get_url(Endpoint.NSS_INVENTORY),
    'resource_methods':   [],
    'item_methods':       EndpointHelper.get_item_methods(Endpoint.NSS_INVENTORY),
    'allowed_item_roles': [EndpointHelper.get_item_policies(Endpoint.NSS_INVENTORY)],
    'schema':             nss_inventory['schema'],
    'datasource':         {
        'source': 'nss_inventory'
        },
    'public_item_methods': ['PATCH']
    }

ns_instantiate = {
    'item_title':         EndpointHelper.get_name(Endpoint.NSS_INSTANTIATE),
    'url':                EndpointHelper.get_url(Endpoint.NSS_INSTANTIATE),
    'resource_methods':   [],
    'item_methods':       EndpointHelper.get_item_methods(Endpoint.NSS_INSTANTIATE),
    'allowed_item_roles': [EndpointHelper.get_item_policies(Endpoint.NSS_INSTANTIATE)],
    'schema':             nss_inventory['schema'],
    'datasource':         {
        'source': 'nss_inventory'
        }
    }

ns_terminate = {
    'item_title':         EndpointHelper.get_name(Endpoint.NSS_TERMINATE),
    'url':                EndpointHelper.get_url(Endpoint.NSS_TERMINATE),
    'resource_methods':   [],
    'item_methods':       EndpointHelper.get_item_methods(Endpoint.NSS_TERMINATE),
    'allowed_item_roles': [EndpointHelper.get_item_policies(Endpoint.NSS_TERMINATE)],
    'schema':             nss_inventory['schema'],
    'datasource':         {
        'source': 'nss_inventory'
        }
    }

validations = {
    'item_title':         EndpointHelper.get_name(Endpoint.VALIDATION),
    'url':                EndpointHelper.get_url(Endpoint.VALIDATION),
    'resource_methods':   EndpointHelper.get_resource_methods(Endpoint.VALIDATION),
    'allowed_roles':      [EndpointHelper.get_resource_policies(Endpoint.VALIDATION)],
    'item_methods':       EndpointHelper.get_item_methods(Endpoint.VALIDATION),
    'allowed_item_roles': [EndpointHelper.get_item_policies(Endpoint.VALIDATION)],
    'schema':             EndpointHelper.get_schema(Endpoint.VALIDATION)
    }

###
#   Trigger on-demand Trust Monitor attestation
###
tm_attest_all = {
    'item_title':       EndpointHelper.get_name(Endpoint.TM_ATTEST_ALL),
    'url':              EndpointHelper.get_url(Endpoint.TM_ATTEST_ALL),
    'resource_methods': EndpointHelper.get_resource_methods(Endpoint.TM_ATTEST_ALL),
    'allowed_roles':    [EndpointHelper.get_resource_policies(Endpoint.TM_ATTEST_ALL)],
    'schema':           EndpointHelper.get_schema(Endpoint.TM_ATTEST_ALL),

    # TODO remove once inter-component authentication is in place.
    'public_methods': ['POST']
}

tm_attest_node = {
    'item_title':       EndpointHelper.get_name(Endpoint.TM_ATTEST),
    'url':              EndpointHelper.get_url(Endpoint.TM_ATTEST),
    'resource_methods': EndpointHelper.get_resource_methods(Endpoint.TM_ATTEST),
    'allowed_roles':    [EndpointHelper.get_resource_policies(Endpoint.TM_ATTEST)],
    'schema':           EndpointHelper.get_schema(Endpoint.TM_ATTEST),

    # TODO remove once inter-component authentication is in place.
    'public_methods':      ['POST']
}
