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
import logging

import requests
from dashboardutils import http_utils
from dashboardutils.error_utils import IssueHandling, IssueElement

from .vnsfo_adapter import VnsfOrchestratorAdapter


class OsmVnsfoAdapter(VnsfOrchestratorAdapter):
    """
    Open Source Mano Orchestrator adapter.
    """

    def __init__(self, protocol, server, port, api_basepath, logger=None):
        super().__init__(protocol, server, port, api_basepath, logger)
        self.logger = logger or logging.getLogger(__name__)
        self.issue = IssueHandling(self.logger)

    def apply_policy(self, target_id, policy):
        """
        Sends a security policy through the Orchestrator REST interface.

        :param target_id: The target to apply the policy to.
        :param policy: The security policy data.
        """

        sec_policy = dict()
        sec_policy['vnsf_id'] = target_id
        sec_policy['action'] = 'set-policies'
        sec_policy['params'] = dict()
        sec_policy['params']['policies'] = policy['recommendation']

        self.logger.debug('Policy for Orchestrator: %r', json.dumps(sec_policy))

        url_r2 = '{}/{}'.format(self.basepath, 'vnsf/r2/action')
        url_r4 = '{}/{}'.format(self.basepath, 'vnsf/r4/action')

        headers = {'Content-Type': 'application/json'}

        # self.logger.debug("-> Send policy data to '%s'", url)

        try:
            r = requests.post(url_r4, headers=headers, json=sec_policy, verify=False)
            if not (r.status_code == http_utils.HTTP_200_OK or r.status_code == http_utils.HTTP_201_CREATED or
                    r.status_code == http_utils.HTTP_202_ACCEPTED):

                r = requests.post(url_r2, headers=headers, json=sec_policy, verify=False)
                if not (r.status_code == http_utils.HTTP_200_OK or r.status_code == http_utils.HTTP_201_CREATED or
                        r.status_code == http_utils.HTTP_202_ACCEPTED):
                    self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['POLICY_ISSUE'],
                                        [[url_r4, r.status_code]])

            if r.text:
                self.logger.debug(r.text)


        except requests.exceptions.ConnectionError:
            self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['VNSFO_UNREACHABLE'],
                                [[url_r4]])

    def instantiate_ns(self, ns_name, target, osm_version):
        """
        Instantiates a Network Service using the Orchestrator REST interface (vNSFO API).
        :param ns_id: Network Service ID
        :return:
        """

        inst_body = {
            "instance_name": ns_name,
            "ns_name": ns_name,
            "virt_type": target
        }

        url = '{}/{}/{}/{}'.format(self.basepath, 'ns', osm_version, 'instantiate')
        headers = {'Content-Type': 'application/json'}
        self.logger.debug("Instantiating Network Service '%s'", ns_name)

        try:
            self.logger.debug("Connecting to vNSFO: {}".format(url))

            r = requests.post(url, headers=headers, json=inst_body, verify=False)

            if not r.status_code == http_utils.HTTP_200_OK:
                self.logger.error("Couldn't instantiate network service '%s'", ns_name)
                return r

            self.logger.debug("Network service '{}' instantiated successfully."
                              "\nGot response:\n{}".format(ns_name, r.json()))
            return r

        except requests.exceptions.ConnectionError:
            self.logger.error("Couldn't connect to vNSFO")

    def terminate_ns(self, instance_id, osm_version):

        url = '{}/{}/{}/{}/{}'.format(self.basepath, 'ns', osm_version, 'running', instance_id)
        headers = {'Content-Type': 'application/json'}

        try:
            self.logger.debug("Connecting to vNSFO: {}".format(url))
            r = requests.delete(url, headers=headers, verify=False)

            if not r.status_code == http_utils.HTTP_200_OK:
                self.logger.error("Couldn't terminate network service with instance id '%s'", instance_id)

            self.logger.debug("Network service instance id '{}' terminated successfully.".format(instance_id))
            return r

        except requests.exceptions.ConnectionError:
            self.logger.error("Termination failed. Couldn't connect to vNSFO")

    def apply_remediation(self, target_type, target_id, action):

        target_action = {
            'sdn': self.__sdn_remediation__,
            'hosts': self.__host_remediation__,
            'vnsf': self.__vnsf_remediation__
        }

        self.logger.debug(
            f'Received remediation request with type {target_type} for id {target_id} and action {action}')
        if target_type not in target_action.keys():
            self.issue.raise_ex(IssueElement.ERROR, self.errors['REMEDIATION']['INVALID_ACTION'],
                                [[action]])

        target_action[target_type](target_id, action)

    def __host_remediation__(self, target_id, action):

        if action == 'update':
            return

        action_map = {
            'isolate': 'isolated',
            'reboot': 'reboot',
            'terminate': 'terminated'
        }

        headers = {'Content-Type': 'application/json'}
        url = f'{self.basepath}/nfvi/node/{target_id}'
        remediation = {
            action_map[action]: True
        }

        self.logger.debug(f"Send remediation data {remediation} to {url}")

        try:
            r = requests.put(url, headers=headers, json=remediation, verify=False)

            if r.text:
                self.logger.debug(r.text)

            if r.status_code > 299:
                self.issue.raise_ex(IssueElement.ERROR, self.errors['REMEDIATION']['INVALID_RESPONSE'])

        except requests.exceptions.ConnectionError:
            self.issue.raise_ex(IssueElement.ERROR, self.errors['REMEDIATION']['VNSFO_UNREACHABLE'],
                                [[url]])

    def __sdn_remediation__(self, target_id, action):
        pass

    def __vnsf_remediation__(self, target_id, action):
        if action == 'update':
            return

        action_map = {
            'isolate': 'isolated',
            'reboot': 'reboot',
            'terminate': 'terminated'
        }

        headers = {'Content-Type': 'application/json'}
        url = f'{self.basepath}/vnsf/action'
        remediation = {
            'action': action_map[action],
            'vnsf_id': target_id
        }

        self.logger.debug(f"Send remediation data {remediation} to {url}")

        try:
            r = requests.post(url, headers=headers, json=remediation, verify=False)
            if r.text:
                self.logger.debug(r.text)

            if r.status_code > 299:
                self.issue.raise_ex(IssueElement.ERROR, self.errors['REMEDIATION']['INVALID_RESPONSE'])

        except requests.exceptions.ConnectionError:
            self.issue.raise_ex(IssueElement.ERROR, self.errors['REMEDIATION']['VNSFO_UNREACHABLE'],
                                [[url]])
