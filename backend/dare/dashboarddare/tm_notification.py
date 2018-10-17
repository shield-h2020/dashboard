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
from pprint import pprint
from threading import Thread

import settings as cfg
from dashboardutils.pipe import PipeProducer
from dashboardutils.rabbit_client import RabbitAsyncConsumer

from .tm_notification_persistence import TMNotificationPersistence

config = {
    'persist_url_hosts': cfg.TM_NOTIFICATION_API_PERSIST_HOST_URL,
    'persist_headers_hosts': cfg.TM_NOTIFICATION_API_PERSIST_HOST_HEADERS,

    'persist_url_vnsf': cfg.TM_NOTIFICATION_API_PERSIST_VNSF_URL,
    'persist_headers_vnsf': cfg.TM_NOTIFICATION_API_PERSIST_VNSF_HEADERS,

    'association_url': cfg.TM_ASSOCIATION_API_URL,
    'association_headers': cfg.TM_ASSOCIATION_API_HEADERS,

    'attestation_message': cfg.TM_ATTESTATION_MESSAGE

}


class TMNotification(PipeProducer):
    """
    Handles the AMQP server to receive the vNSF notifications and acts as an events producer for such notifications.

    How an AMQP server gets up and running is the responsibility of this class. When it does this is up to a pipe
    manager provided upon instantiation. All this class needs to do for the manager is to present itself as an events
    producer.
    """

    def __init__(self, settings, pipe, boot=True):
        """
        :param settings: The AMQP queue settings.
        :param pipe: The pipe manager where this instance is to be identified as an events producer.
        """

        super().__init__()

        self.logger = logging.getLogger(__name__)

        self.pipe = pipe
        self._consumer = RabbitAsyncConsumer(config=settings, msg_callback=self.persist_notification)

        if boot:
            # Setup the instance as the events producer for the managed pipe.
            self.pipe.boot_in_sink(self)

    def setup(self):
        """
        The logic is provided by the RabbitMQ client hence nothing to do here.
        """
        pass

    def bootup(self):
        """
        Gets the AMQP server up and running.
        """
        thread = Thread(target=self._consumer.run)
        thread.start()

    def persist_notification(self, body):
        """
        Persists the TM notification and notifies the observers about the new notification.

        NOTE: exceptions should be caught by the caller.

        :param body: the actual notification.
        """

        self.logger.info('TM Notification: %r', body)

        notifications = json.loads(body)
        # v = Validator(tm_notification)

        # Validate the received notification
        # TODO: Validate the schema by file
        '''
        if not v.validate(notifications):
            self.logger.error('Error validating notification {}'.format(pprint(v.errors)))
        '''
        # Persist the notification
        notification_persistence = TMNotificationPersistence(config)

        # Based on the message provide two operations
        tenant_vnsf_association = {}

        if 'hosts' in notifications:
            for host in notifications['hosts']:
                vnsfs = host.pop('vnsfs', [])

                for vnsf in vnsfs:
                    tenant = notification_persistence.__associate_vnsf_instance__(vnsf.get('vnsfd_name'))
                    if tenant not in tenant_vnsf_association:
                        tenant_vnsf_association[tenant] = {}
                        tenant_vnsf_association[tenant]['vnsfs'] = []
                        tenant_vnsf_association[tenant]['time'] = host.get('time')
                        tenant_vnsf_association[tenant]['tenant_id'] = tenant

                    tenant_vnsf_association[tenant]['vnsfs'].append(vnsf)

            notification_persistence.persist_host(notifications['hosts'], 'hosts')

        if 'sdn' in notifications:
            notification_persistence.persist_host(notifications['sdn'], 'sdn')

        for _tenant, _vnsf in tenant_vnsf_association.items():
            notification_persistence.persist_vnsf(_vnsf)
            _vnsf.pop('tenant_id', None)
            self.logger.debug(f'Sending Notification for tenant {_tenant}: {_vnsf}')
            self.notify_by_tenant(config['attestation_message'], _tenant)

        self.logger.debug(f'Sending Notification for tenant {tenant}: {vnsf}')

        self.logger.debug('Sending Notification to host: {}'.format(pprint(notifications)))
        self.notify_all(config['attestation_message'])
