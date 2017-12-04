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

from dashboardutils import exceptions


class VnsfOrchestratorPolicyIssue(exceptions.ExceptionMessage):
    """vNSFO policy operation failed."""


class VnsfOrchestratorOnboardingIssue(exceptions.ExceptionMessage):
    """vNSFO onboarding operation failed."""


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

    def __init__(self, protocol, server, port, api_basepath, logger=None):
        self.logger = logging.getLogger(__name__)

        # Maintenance friendly.
        self._policy_issue = VnsfOrchestratorPolicyIssue('Can not convey policy to the vNFSO')
        self._unreachable = VnsfOrchestratorOnboardingIssue('Can not reach the Orquestrator')

        if port is not None:
            server += ':' + port

        self.basepath = '{}://{}'.format(protocol, server)
        if len(api_basepath) > 0:
            self.basepath = '{}/{}'.format(self.basepath, api_basepath)

        self.logger.debug('vNSF Orchestrator API at: %s', self.basepath)

    @abstractmethod
    def apply_policy(self, tenant_id, policy):
        """
        Sends a security policy to the Orchestrator.

        :param tenant_id: The tenant to apply the policy to.
        :param policy: The security policy data.
        """

        pass
