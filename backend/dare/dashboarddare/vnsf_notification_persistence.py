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
from dashboardutils import exceptions, http_codes

from . import dashboard_errors as err


class VNSFNotificationNotPersisted(exceptions.ExceptionMessage):
    """Error persisting the notification."""


class TenantAssociationError(exceptions.ExceptionMessage):
    """Error associating tenant and IP"""


class VNSFNotificationPersistence:

    def __init__(self, settings):
        self.logger = logging.getLogger(__name__)

        # Maintenance friendly.
        self._notification_not_persisted = VNSFNotificationNotPersisted(err.VNSFNOT_NOT_PERSISTED)
        self._tenant_association_error = TenantAssociationError(err.ASSOCIATION_ERROR)

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
        headers = self.settings.get('association_headers')

        # Create the query string to search for the IP
        payload = dict(where='{{"ip":"{}"}}'.format(ip_address))

        try:

            r = requests.get(url, headers=headers, params=payload)

            if r.text:
                self.logger.debug(r.text)

            if not r.status_code == http_codes.HTTP_200_OK:
                self.logger.error('Association error for {}. Status: {}'.format(url, r.status_code))
                raise self._notification_not_persisted

            response_data = r.json()
            if response_data['_meta']['total'] != 1:
                self.logger.error(
                    'Invalid association with total results of: {}'.format(response_data['_meta']['total']))
                raise self._tenant_association_error

            tenant = response_data.get('_items')[0].get('tenant_id', None)
            self.logger.debug("IP {} belongs to Tenant {}".format(ip_address, tenant))
            return tenant

        except requests.exceptions.ConnectionError as e:
            self.logger.error('Error associating the IP at {}.'.format(url), e)
            raise Exception

    def persist(self, notification):
        url = self.settings['persist_url']
        headers = self.settings['persist_headers']

        try:

            # Associate IP with tenants
            tenant = self.__associate_tenant_ip__(notification.get('event').get('destination-ip'))

            notification_to_persist = dict()
            notification_to_persist['tenant'] = tenant
            notification_to_persist['type'] = self.settings['notification_type']
            notification_to_persist['data'] = json.dumps(notification)

            # Persist notification.
            r = requests.post(url, headers=headers, data=json.dumps(notification_to_persist))
            if r.text:
                self.logger.debug(r.text)

            if not r.status_code == http_codes.HTTP_201_CREATED:
                self.logger.error('Persistence error for {}. Status: {}'.format(url, r.status_code))
                raise self._notification_not_persisted

            return tenant

        except requests.exceptions.ConnectionError as e:
            self.logger.error('Error persisting the policy at {}.'.format(url), e)
            raise Exception

        except TenantAssociationError as e:
            # The exception only logs the error
            # There's no one to handle this
            self.logger.exception(e)
