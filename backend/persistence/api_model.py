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
    'tenant_id': {
        'description': 'Description of the user resource',
        'type': 'string',
        'empty': False,
        'required': True
    },

    # Time and date when the thread was detected. Format: ISO 8601.
    'detection': {
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

    # The severity assigned to the threat. Format: user-defined.
    'severity': {
        'type': 'integer',
        'empty': False,
        'required': True
    },

    # The applicability of the policy for the tenant in question. Format: user-defined.
    'status': {
        'type': 'string',
        'empty': False,
        'required': True
    },

    # The kind of network attack. Format: user-defined.
    'attack': {
        'type': 'string',
        'empty': False,
        'required': True
    },

    # The recommendation to counter the threat. Format: user-defined.
    'recommendation': {
        'type': 'string',
        'empty': False,
        'required': True
    }
}

tenant_ip_association = {
    "ip": {
        "type": "list",
        "schema": {"type": "ipv4address"},
        "empty": False,
        "required": True
    },
    "tenant_id": {
        'type': 'string',
        "empty": False,
        "required": True
    }
}
