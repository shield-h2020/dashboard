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


import datetime
import logging
from pprint import pprint

import settings as cfg
from vnsfo.vnsfo import VnsfoFactory, VnsfoNotSupported
from vnsfo.vnsfo_adapter import VnsfOrchestratorPolicyIssue


class DashboardPersistence:
    """
    Handles the backstage operations required for the Dashboard Persistence API. These operations are mostly targeted
    at pre and post hooks associated with the API.
    """

    @staticmethod
    def convey_policy(updates, original):
        """
        Forwards the security policy to the vNSFO so it can be applied.

        As this method is an hook for an API update operation it ensures the new data replaces the original one
        before conveying the policy.

        :param updates: The data updated
        :param original: The original data
        """

        logger = logging.getLogger(__name__)

        policy = dict(original)
        for key, value in updates.items():
            policy[key] = value

        logger.info('updated policy: \n%s', pprint(policy))
        print('updated policy: \n%s', pprint(policy))

        try:
            vnsfo = VnsfoFactory.get_orchestrator('OSM', cfg.VNSFO_PROTOCOL, cfg.VNSFO_HOST, cfg.VNSFO_PORT,
                                                  cfg.VNSFO_API)
            vnsfo.apply_policy(policy['vnsf_id'], policy)
        except VnsfOrchestratorPolicyIssue:
            logger.error('VnsfOrchestratorPolicyIssue')
        except VnsfoNotSupported:
            logger.error('VnsfOrchestratorPolicyIssue')

    @staticmethod
    def convert_to_datetime(items):
        """
        Converts the detection date field to datetime as it is a string due to the JSON serialization operation.

        :param items: The json to store.
        """

        for item in items:
            item['detection'] = datetime.datetime.strptime(item['detection'], cfg.DATETIME_FIELDS_INPUT_FMT)
