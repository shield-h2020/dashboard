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


from api_endpoints_def import Endpoint

swagger_info = {
    'title':          'Dashboard API',
    'version':        '0.1.0',
    'description':    """
                   This API handles the security recommendations CRUD operations.


                   _Please note that consumers are not allowed to edit (`PATCH`), update (`PUT`) or delete (`DELETE`) 
                   a resource unless they provide an up-to-date `ETag` for the resource they are attempting to modify. 
                   This value, taken from the details (`GET`) request, is mandatory and should be provided in the 
                   `If-Match` header_.


                   API version numbering as per http://semver.org/
                   """,
    'termsOfService': 'my terms of service',
    'contact':        {
        'name': 'Filipe Ferreira',
        'url':  'https://github.com/betakoder'
        },
    'license':        {
        'name': 'Apache License, Version 2.0',
        'url':  'http://www.apache.org/licenses/LICENSE-2.0',
        },
    'schemes':        ['http', 'https'],
    }

"""
The documentation is built from the endpoints definition by overwriting the keys the Eve Swagger automatically builds 
from the code.

To hack the item endpoints properly, one must first generate the documentation as is to know which variable names to 
use for the item endpoints (the {var_name} part of the endpoint).
"""


def _get_methods(endpoint_data):
    methods = {}
    for method in endpoint_data.keys():
        methods[method.lower()] = endpoint_data[method][Endpoint.__DOCS__]

    return methods


paths = {}
for name, member in Endpoint.__members__.items():
    endpoint_data = member.value

    paths['/' + endpoint_data[Endpoint.__URL__]] = _get_methods(endpoint_data[Endpoint.__RESOURCE__])

    if Endpoint.__DOC_ID_VAR__ in endpoint_data:
        paths['/{}/{{{}}}'.format(endpoint_data[Endpoint.__URL__],
                                  endpoint_data[Endpoint.__DOC_ID_VAR__])] = _get_methods(
                endpoint_data[Endpoint.__ITEM__])
