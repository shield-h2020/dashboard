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


import time
import settings as cfg
import requests
from eve.methods.get import get_internal
from eve.methods.post import post_internal
from dashboardutils import http_utils
import logging

logger = logging.getLogger(__name__)


class AttackHooks:

    @staticmethod
    def post_statistics_set_timestamp(request):
        """
        Upon creation of a new attack statistic a timestamp of the current time is applied.
        """
        logger.debug("Setting timestamp on attack statistics post")

        current_time = time.time()

        # Check if statistics already exist. If not create an time instance with 0 active and 0 blocked
        # The tenant scope dictates which groups to create for a tenant.
        # Returns a tuple: (response, last_modified, etag, status, headers)
        (statistics_data, _, _, status, _) = get_internal('attack_statistics')
        if status == http_utils.HTTP_200_OK and statistics_data['_meta']['total'] == 0:
            logger.debug("Creating statistics !zero! for attack statistics")
            payload = {
                'timestamp': current_time - 1.0,  # decrease one second from current time
                'active': 0,
                'blocked': 0,
                'cumulative': 0
            }
            (result, _, etag, status, _) = post_internal("attack_statistics", payload)
            if not status == http_utils.HTTP_201_CREATED:
                logger.error("Failed to create statistics zero in attack statistics")

        # set timestamp to current time
        request.json['timestamp'] = current_time

    @staticmethod
    def post_registry_set_status(request):
        """
        Upon creation of a new attack record the status must be always set to 'active'
        """
        request.json['status'] = 'active'
        request.json['detection_timestamp'] = time.time()

    @staticmethod
    def patch_registry_set_closure(updates, original):
        """
        Upon patch of an existing attack record, check if status is being set to blocked. In that case, set the
        closure timestamp to current time
        """
        if updates['status'] == 'blocked':
            updates['closure_timestamp'] = time.time()


    @staticmethod
    def statistics_add_active(items):
        """
        After inserting attack on registry, add a new statistic by incrementing the number of active attacks
        """
        # Get last attack statistics
        last_statistic = AttackHooks._get_last_attack_statistics()
        if not last_statistic:
            # First statistic
            num_active = 1
            num_blocked = 0
            num_cumulative = 1
        else:
            # Create a new updated statistic
            num_active = last_statistic['active'] + 1
            num_blocked = last_statistic['blocked']
            num_cumulative = last_statistic['cumulative'] + 1

        if not AttackHooks._post_attack_statistics(num_active, num_blocked, num_cumulative):
            return

    @staticmethod
    def statistics_add_blocked(updates, original):
        """
        After updating attack on registry to status 'blocked', add a new statistic by decrementing the number
        of active attacks and incrementing the number of blocked attacks.
        """
        if not updates['status'] == 'blocked':
            return

        # Get last attack statistics
        last_statistic = AttackHooks._get_last_attack_statistics()
        if not last_statistic:
            return

        # Create a new updated statistic
        num_active = last_statistic['active'] - 1
        num_blocked = last_statistic['blocked'] + 1
        num_cumulative = last_statistic['cumulative']
        if not AttackHooks._post_attack_statistics(num_active, num_blocked, num_cumulative):
            return


    @staticmethod
    def _get_last_attack_statistics():
        url = f'{cfg.BACKENDAPI}/attack/statistics?sort=[{{"timestamp", -1}}]'
        headers = {'Content-Type': 'application/json'}
        try:
            r = requests.get(url, headers=headers, verify=False)
            if not r.status_code == http_utils.HTTP_200_OK:
                logger.error('Failed to retrieve the attack statistics: {}'.format(r.text))
                return

        except requests.exceptions.ConnectionError as e:
            logger.error('Error connecting to the attack statistics at {}.'.format(url), e)
            return

        last_statistic = r.json()
        return last_statistic['_items'][0] if last_statistic['_meta']['total'] > 0 else None

    @staticmethod
    def _post_attack_statistics(num_active, num_blocked, num_cumulative):
        url = f'{cfg.BACKENDAPI}/attack/statistics'
        headers = {'Content-Type': 'application/json'}
        try:
            payload = {
                'active':     num_active,
                'blocked':    num_blocked,
                'cumulative': num_cumulative
            }
            r = requests.post(url, headers=headers, json=payload, verify=False)
            if not r.status_code == http_utils.HTTP_201_CREATED:
                logger.error('Failed to create the attack statistics {}: {}'.format(payload, r.text))
                return

        except requests.exceptions.ConnectionError as e:
            logger.error('Error connecting to the attack statistics at {}.'.format(url), e)
            return

        return r.json()