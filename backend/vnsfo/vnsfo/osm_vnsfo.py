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

import requests
import xmlschema as xmlschema

import settings as cfg
from .vnsfo_adapter import VnsfOrchestratorAdapter


class OsmVnsfoAdapter(VnsfOrchestratorAdapter):
    """
    Open Source Mano Orchestrator adapter.
    """

    def __init__(self, protocol, server, port, api_basepath, logger=None):
        super().__init__(protocol, server, port, api_basepath, logger)

    def apply_policy(self, tenant_id, policy):
        """
        Sends a security policy through the Orchestrator REST interface.

        :param tenant_id: The tenant to apply the policy to.
        :param policy: The security policy data.
        """

        sec_policy = dict()
        sec_policy['vnsf_id'] = self.get_vnsf_id_for_demo_hack(policy['recommendation'])
        sec_policy['action'] = 'set-policies'
        sec_policy['params'] = dict()
        sec_policy['params']['policy'] = policy['recommendation']

        self.logger.debug('Policy for Orchestrator: %r', json.dumps(sec_policy))

        url = '{}/{}'.format(self.basepath, 'vnsf/action')

        headers = {'Content-Type': 'application/json'}

        self.logger.debug("Send policy data to '%s'", url)

        try:
            r = requests.post(url, headers=headers, json=sec_policy, verify=False)

            if len(r.text) > 0:
                self.logger.debug(r.text)

            if not r.status_code == 200:
                self.logger.error('vNFSO policy at {}. Status: {}'.format(url, r.status_code))
                raise self._policy_issue

        except requests.exceptions.ConnectionError:
            self.logger.error('Error conveying policy at %s', url)
            raise self._unreachable

    def get_vnsf_id_for_demo_hack(self, policy_data):
        policy_schema = xmlschema.XMLSchema(cfg.POLICYSCHEMA_FILE)
        policy = policy_schema.to_dict(policy_data, './tns:mspl-set/tns:it-resource')

        return policy['@id']
