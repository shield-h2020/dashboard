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
import xmlschema
from xmlschema import XMLSchemaValidationError

from dashboardutils import exceptions, http_codes
from . import dashboard_errors as err


class SecurityPolicyNotComplaint(exceptions.ExceptionMessage):
    """Policy not compliant with the schema defined."""


class SecurityPolicyNotPersisted(exceptions.ExceptionMessage):
    """Error persisting the security policy."""


class SecurityPolicyPersistence:
    def __init__(self, settings):
        self.logger = logging.getLogger(__name__)

        # Maintenance friendly.
        self._wrong_policy_format = SecurityPolicyNotComplaint(err.SECPOLICY_NOT_COMPLIANT)
        self._policy_not_persisted = SecurityPolicyNotPersisted(err.SECPOLICY_NOT_PERSISTED)

        self.settings = settings

    def persist(self, policy):
        try:
            # Check MSPL schema compliance.
            policy_schema = xmlschema.XMLSchema(self.settings['policy_schema'])
            policy_context = policy_schema.to_dict(policy, './tns:mspl-set/tns:context')

            # Extract metadata.
            policy_info = dict()
            policy_info['tenant_id'] = self.settings['tenant_id']
            policy_info['detection'] = policy_context['tns:timestamp']
            policy_info['severity'] = policy_context['tns:severity']
            policy_info['status'] = 'Not applied'
            policy_info['attack'] = policy_context['tns:type']
            policy_info['recommendation'] = policy.decode('utf-8')

            policy_json = json.dumps(policy_info)

            self.logger.debug('policy from XML\n%r', policy_info['recommendation'])

            # Persist policy.
            url = self.settings['persist_url']
            headers = self.settings['persist_headers']

            r = requests.post(url, headers=headers, data=policy_json)

            if len(r.text) > 0:
                self.logger.debug(r.text)

            if not r.status_code == http_codes.HTTP_201_CREATED:
                self.logger.error('Persistence error for {}. Status: {}'.format(url, r.status_code))
                raise self._policy_not_persisted

            # Include identification data for the policy just persisted.
            response_data = r.json()
            policy_info['_id'] = response_data['_id']
            policy_info['_etag'] = response_data['_etag']

            return policy_info

        except XMLSchemaValidationError:
            raise self._wrong_policy_format

        except requests.exceptions.ConnectionError as e:
            self.logger.error('Error persisting the policy at {}.'.format(url), e)
            raise Exception
