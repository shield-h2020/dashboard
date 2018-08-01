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


class TMNotificationNotPersisted(ExceptionMessage):
    """Error persisting the notification."""


class TenantAssociationError(ExceptionMessage):
    """Error associating tenant and vNSF Instance ID"""


class TMNotificationPersistence:
    errors = {
        'NOTIFICATION': {
            'ERROR':         {
                IssueElement.EXCEPTION.name: TenantAssociationError('Invalid association with total results of: {}')
                },
            'NOT_PERSISTED': {
                IssueElement.ERROR.name:     ['TM notification not persisted. Association error for {}. Status: {}'],
                IssueElement.EXCEPTION.name: TMNotificationNotPersisted('Error persisting the TM notification.')
                }
            }
        }

    def __init__(self, settings):
        self.logger = logging.getLogger(__name__)
        self.issue = IssueHandling(self.logger)

        self.settings = settings

    def __associate_vnsf_instance__(self, instance_id):
        """
        Associates a given vNSF Instance to a tenant interacting with the association service.
        :param instance_id: the vNSF instance ID to be associated with a tenant
        :return String with the tenant name associated with the vNSF instance ID
        :raise TenantAssociationError when the instance ID is associated with more then one tenant or none association was found
        """

        self.logger.debug("Associating vNSF Instance ID: {}".format(instance_id))
        url = self.settings.get('association_url')
        headers = self.settings.get('association_headers')

        # Create the query string to search for the vNSF instance
        payload = dict(where='{{"vnsf_instances":"{}"}}'.format(instance_id))

        try:
            r = requests.get(url, headers=headers, params=payload)

            if r.text:
                self.logger.debug(r.text)

            if not r.status_code == http_utils.HTTP_200_OK:
                self.issue.raise_ex(IssueElement.ERROR, self.errors['NOTIFICATION']['NOT_PERSISTED'],
                                    [[url, r.status_code]])

            response_data = r.json()
            if response_data['_meta']['total'] != 1:
                self.issue.raise_ex(IssueElement.ERROR, self.errors['NOTIFICATION']['ERROR'],
                                    [[response_data['_meta']['total']]])

            tenant = response_data.get('_items')[0].get('tenant_id', None)
            self.logger.debug("vNSF Instance ID {} belongs to Tenant {}".format(instance_id, tenant))
            return tenant

        except requests.exceptions.ConnectionError as e:
            self.logger.error('Error associating the vNSF Instance at {}.'.format(url), e)
            raise Exception

    def persist(self, notification):
        url = self.settings['persist_url']
        headers = self.settings['persist_headers']

        try:
            # Associate IP with tenants
            tenant = self.__associate_vnsf_instance__(notification.get('event').get('vnsf_instance_id'))

            notification_to_persist = dict()
            notification_to_persist['tenant_id'] = tenant
            notification_to_persist['type'] = self.settings['notification_type']
            notification_to_persist['data'] = json.dumps(notification)

            # Persist notification.
            r = requests.post(url, headers=headers, data=json.dumps(notification_to_persist))
            if r.text:
                self.logger.debug(r.text)

            if not r.status_code == http_utils.HTTP_201_CREATED:
                self.issue.raise_ex(IssueElement.ERROR, self.errors['NOTIFICATION']['NOT_PERSISTED'],
                                    [[url, r.status_code]])

            return tenant

        except requests.exceptions.ConnectionError as e:
            self.logger.error('Error persisting the policy at {}.'.format(url), e)
            raise Exception

        except TenantAssociationError as e:
            # The exception only logs the error
            # There's no one to handle this
            self.logger.exception(e)
