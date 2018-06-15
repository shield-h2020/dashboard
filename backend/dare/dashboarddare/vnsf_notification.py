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
from cerberus import Validator
from dashboardutils.pipe import PipeProducer
from dashboardutils.rabbit_client import RabbitAsyncConsumer
from schema.vnsf_notification import vnsf_notification

from .vnsf_notification_persistence import VNSFNotificationPersistence

config = {
    'tenant_id': cfg.VNSFO_TENANT_ID,

    'persist_url': cfg.NOTIFICATION_API_PERSIST_URL,
    'persist_headers': cfg.NOTIFICATION_API_PERSIST_HEADERS,

    'association_url': cfg.ASSOCIATION_API_URL,
    'association_headers': cfg.ASSOCIATION_API_HEADERS,

    'notification_type': 'VNSF'
}


class VNSFNotification(PipeProducer):
    """
    Handles the AMQP server to receive the vNSF notifications and acts as an events producer for such notifications.

    How an AMQP server gets up and running is the responsibility of this class. When it does this is up to a pipe
    manager provided upon instantiation. All this class needs to do for the manager is to present itself as an events
    producer.
    """

    def __init__(self, settings, pipe):
        """
        :param settings: The AMQP queue settings.
        :param pipe: The pipe manager where this instance is to be identified as an events producer.
        """

        super().__init__()

        self.logger = logging.getLogger(__name__)

        self.pipe = pipe
        self._consumer = RabbitAsyncConsumer(config=settings, msg_callback=self.persist_notification)

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
        Persists the vNSF notification and notifies the observers about the new notification.

        NOTE: exceptions should be caught by the caller.

        :param body: the actual notification.
        """

        self.logger.info('vNSF Notification: %r', body)

        notification_persistence = VNSFNotificationPersistence(config)

        notifications = json.loads(body)
        v = Validator(vnsf_notification)

        for notification in notifications:
            if not v.validate(notification):
                self.logger.error('Error validating notification {}'.format(pprint(v.errors)))
            tenant = notification_persistence.persist(notification)
            if tenant:
                self.logger.debug('Sending Notification: {}'.format(pprint(notification)))
                self.notify_by_tenant(notification, tenant)
