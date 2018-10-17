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
from dashboardutils.error_utils import ExceptionMessage, IssueHandling, IssueElement


class VnsfoNotificationNotPersisted(ExceptionMessage):
    """Error persisting the notification."""


# class TenantAssociationError(ExceptionMessage):
#     """Error associating tenant and vNSF Instance ID"""
#

class VnsfoNotificationPersistence:
    NOT_APPLIED_STATUS = 'Not Applied'

    errors = {
        'NOTIFICATION': {
            'NOT_PERSISTED': {
                IssueElement.ERROR: ['vNSFO notification not persisted. Association error for {}. Status: {}'],
                IssueElement.EXCEPTION: VnsfoNotificationNotPersisted('Error persisting the vNSFO notification.')
            }
        }
    }

    def __init__(self, settings):
        self.logger = logging.getLogger(__name__)
        self.issue = IssueHandling(self.logger)
        self.settings = settings

    def persist_ns_instance(self, instance_id, op_status):
        url = self.settings['persist_url_notification_vnsfo']
        headers = self.settings['persist_headers_notification_vnsfo']

        try:
            # Persist notification
            notification_to_persist = {
                "type": 'ns_instance',
                "data": {
                    "instance_id": instance_id,
                    "status": op_status
                }
            }

            r = requests.post(url, headers=headers, data=json.dumps(notification_to_persist))
            if not r.status_code == http_utils.HTTP_201_CREATED:
                self.issue.raise_ex(IssueElement.ERROR, self.errors['NOTIFICATION']['NOT_PERSISTED'],
                                    [[url, r.status_code]])

        except requests.exceptions.ConnectionError as e:
            self.logger.error('Error persisting the vNSFO notification at {}.'.format(url), e)
            raise Exception
