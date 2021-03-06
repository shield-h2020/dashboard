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

import logging

from abc import abstractmethod, ABCMeta
from dashboardutils import http_utils
from dashboardutils.error_utils import ExceptionMessage, IssueHandling, IssueElement


class VnsfOrchestratorPolicyIssue(ExceptionMessage):
    """vNSFO policy operation failed."""


class VnsfOrchestratorOnboardingIssue(ExceptionMessage):
    """vNSFO onboarding operation failed."""


class VnsfOrchestratorRemediationIssue(ExceptionMessage):
    """vNSFO remediation operation failed"""


class VnsfOrchestratorAdapter(metaclass=ABCMeta):
    """
    Interface with the vNSF Orchestrator through it's Service Orquestrator REST API.

    The documentation available at the time of coding this is for OSM Release One (March 1, 2017) and can be found at
    https://osm.etsi.org/wikipub/images/2/24/Osm-r1-so-rest-api-guide.pdf. Despite the apparently straight forward
    way for onboarding vNSF & NS referred by the documentation the endpoints mentioned are not available outside
    localhost. Thus a workaround is required to get this to work.

    Such workaround consist in using the REST interface provided by the composer available at
    OSM/UI/skyquake/plugins/composer/routes.js and which implementation is at
    OSM/UI/skyquake/plugins/composer/api/composer.js. From these two files one can actually find the Service
    Orquestrator REST API endpoints being called to perform the required operation. From there it's just a matter of
    calling the proper composer endpoint so it can carry out the intended operation. Ain't life great?!
    """

    errors = {
        'POLICY': {
            'POLICY_ISSUE':      {
                IssueElement.ERROR:     ['vNFSO policy at {}. Status: {}'],
                IssueElement.EXCEPTION: VnsfOrchestratorPolicyIssue('Can not convey policy to the vNFSO')
                },
            'VNSFO_UNREACHABLE': {
                IssueElement.ERROR:     ['Error conveying policy at {}'],
                IssueElement.EXCEPTION: VnsfOrchestratorOnboardingIssue('Can not reach the Orchestrator')
                }
            },
        'REMEDIATION':          {
            'VNSFO_UNREACHABLE': {
                IssueElement.ERROR:    ['Error conveying policy at {}'],
                IssueElement.EXCEPTION: VnsfOrchestratorOnboardingIssue('Can not reach the Orchestrator')
                },
            'INVALID_ACTION': {
                IssueElement.ERROR:    ['Error validating action {}'],
                IssueElement.EXCEPTION: VnsfOrchestratorRemediationIssue("Provided action is invalid")
                },
            'INVALID_RESPONSE': {
                IssueElement.ERROR:    ['Error applying action'],
                IssueElement.EXCEPTION: VnsfOrchestratorRemediationIssue("Can't apply the provided action")
                }
            }
        }

    def __init__(self, protocol, server, port, api_basepath, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.issue = IssueHandling(self.logger)

        self.basepath = http_utils.build_url(server, port, api_basepath, protocol)

        self.logger.debug('vNSF Orchestrator API at: %s', self.basepath)

    @abstractmethod
    def apply_policy(self, target_id, policy):
        """
        Sends a security policy to the Orchestrator.

        :param target_id: The target to apply the policy to.
        :param policy: The security policy data.
        """

        pass

    @abstractmethod
    def instantiate_ns(self, ns_id, target, nfvo_version):
        """
        :param ns_id:
        :param target:
        :return: Response from vNSFO
        """
        pass

    @abstractmethod
    def terminate_ns(self, instance_id, nfvo_version):
        """
        :param instance_id: Instance ID of Network Service
        :return: Response from vNSFO
        """
        pass
