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
from dashboardutils.tenant_ip_utils import get_tenant_by_ip, AssociationCodeError, MultipleAssociation


class VNSFNotificationNotPersisted(ExceptionMessage):
    """Error persisting the notification."""


class TenantAssociationError(ExceptionMessage):
    """Error associating tenant and IP"""


class VNSFNotificationPersistence:
    errors = {
        'NOTIFICATION': {
            'ERROR':         {
                IssueElement.EXCEPTION.name: TenantAssociationError('Invalid association with total results of: {}')
                },
            'NOT_PERSISTED': {
                IssueElement.ERROR.name:     ['vNSF notification not persisted. Association error for {}. Status: {}'],
                IssueElement.EXCEPTION.name: VNSFNotificationNotPersisted('Error persisting the vNSF notification.')
                }
            }
        }

    def __init__(self, settings):
        self.logger = logging.getLogger(__name__)
        self.issue = IssueHandling(self.logger)

        self.settings = settings

    def __associate_tenant_ip__(self, ip_address):
        """
        Associates a given IP address to a tenant interacting with the association service.
        :param ip_address: the address to be associated with a tenant
        :return String with the tenant name associated with the IP
        :raise TenantAssociationError when the IP is associated with more then one tenant or none association was found
        """

        self.logger.debug("Associating IP: {}".format(ip_address))
        url = self.settings.get('association_url')

        try:
            tenant = get_tenant_by_ip(url, ip_address)
            self.logger.debug("IP {} belongs to Tenant {}".format(ip_address, tenant))
            return tenant
        except MultipleAssociation as e:
            self.issue.raise_ex(IssueElement.ERROR, self.errors['NOTIFICATION']['ERROR'],
                                [[e.total_associations]])
        except AssociationCodeError as e:
            self.issue.raise_ex(IssueElement.ERROR, self.errors['NOTIFICATION']['NOT_PERSISTED'],
                                [[url, e.status_code]])

    def persist(self, notification):
        url = self.settings['persist_url']
        headers = self.settings['persist_headers']

        try:

            # Associate IP with tenants
            tenant = self.__associate_tenant_ip__(notification.get('event').get('destination-ip'))

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
