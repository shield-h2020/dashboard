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


import requests
import logging
from dashboardutils import http_utils

class AttackLogger:

    def __init__(self, backend_api_url):
        self.logger = logging.getLogger(__name__)
        self.backend_api_url = backend_api_url

    def add(self, ip_address, attack_type):

        # Check if this combination of <ip_address, attack_type> already exists
        if self._get_attack_record(ip_address, attack_type):
            return

        # No record was found, post it
        if not self._post_attack_record(ip_address, attack_type):
            return

        return True

    def block(self, ip_address, attack_type):
        # Get the attack record
        attack_record = self._get_attack_record(ip_address, attack_type)
        if not attack_record:
            self.logger.error("Failed to block the attack <{},{}>".format(ip_address, attack_type))
            return

        # Check if the attack record current status is 'active', otherwise just ignore and quit
        if not attack_record['status'] == 'active':
            self.logger.debug("Failed to block the attack <{},{}>: status is not 'active'"
                              .format(ip_address, attack_type))
            return

        # Update the attack record to 'blocked'
        if not self._patch_attack_record(attack_record, 'blocked'):
            return

        return True


    ####################
    # Helper functions #
    ####################

    def _get_attack_record(self, ip_address, attack_type):
        url = f'{self.backend_api_url}/attack/registry?where={{"ip_address":"{ip_address}", "attack": "{attack_type}"}}'
        headers = {'Content-Type': 'application/json'}
        try:
            r = requests.get(url, headers=headers, verify=False)

            if not r.status_code == http_utils.HTTP_200_OK:
                self.logger.error('Invalid attack registry endpoint')
                return

            registry_data = r.json()
            if registry_data['_meta']['total'] > 1:
                self.logger.error('The registry has {} records of the <{},{}> association'
                                  .format(registry_data['_meta']['total'], ip_address, attack_type))
                return

        except requests.exceptions.ConnectionError as e:
            self.logger.error('Error connecting to the attack registry at {}.'.format(url), e)
            return

        return registry_data['_items'][0] if registry_data['_meta']['total'] == 1 else None

    def _post_attack_record(self, ip_address, attack_type):
        url = f'{self.backend_api_url}/attack/registry'
        headers = {'Content-Type': 'application/json'}
        try:
            payload = {
                'ip_address': ip_address,
                'attack':     attack_type
            }
            r = requests.post(url, headers=headers, json=payload, verify=False)
            if not r.status_code == http_utils.HTTP_201_CREATED:
                self.logger.error('Failed to create a record of the <{},{}> association: {}'
                                  .format(ip_address, attack_type, r.text))
                return

        except requests.exceptions.ConnectionError as e:
            self.logger.error('Error connecting to the attack registry at {}.'.format(url), e)
            return

        self.logger.debug('Created record for the <{},{}> association'.format(ip_address, attack_type))
        return r.json()

    def _patch_attack_record(self, attack_record, status):
        url = f'{self.backend_api_url}/attack/registry/{attack_record["_id"]}'
        headers = {'Content-Type': 'application/json'}
        try:
            headers['If-Match'] = attack_record['_etag']
            payload = {
                'status': status
            }
            r = requests.patch(url, headers=headers, json=payload, verify=False)
            if not r.status_code == http_utils.HTTP_200_OK:
                self.logger.error("Failed to update the record <{},{}> to status '{}'"
                                  .format(attack_record['ip_address'], attack_record['attack'], status))
                return

        except requests.exceptions.ConnectionError as e:
            self.logger.error('Error connecting to the attack registry at {}.'.format(url), e)
            return

        self.logger.debug("Updated record <{},{}> to status '{}'"
                          .format(attack_record['ip_address'], attack_record['attack'], status))
        return r.json()
