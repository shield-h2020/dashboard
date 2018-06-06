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


import json
from pprint import pformat

import flask


class NssInventoryHooks:
    """
    Handles the backstage operations required for the Network Services Inventory part of the Dashboard API. These
    operations are mostly targeted at pre and post hooks associated with the API.
    """

    @staticmethod
    def provision_network_service(items):
        user_data = items[0]

        # TODO: If more than one "where" lookup there's an error in the URL query parameters.
        lookup = json.loads(flask.request.args.getlist('where')[0])
        print('lookup: ' + pformat(lookup))

        # The tenant ID must be set according to the one provided in the URL (which has been properly authorized).
        user_data['tenant_id'] = lookup['tenant_id']
