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
from pprint import pprint
from threading import Thread

import settings as cfg
from dashboardutils.pipe import PipeProducer
from dashboardutils.rabbit_client import RabbitAsyncConsumer

from .mspl_notification_persistence import MsplPersistence

config = {
    'policy_schema':       cfg.POLICYSCHEMA_FILE,

    'persist_url':         cfg.POLICYAPI_PERSIST_URL,
    'persist_headers':     cfg.POLICYAPI_PERSIST_HEADERS,

    'association_url':     cfg.MSPL_ASSOCIATION_API_URL,
    'association_headers': cfg.MSPL_ASSOCIATION_API_HEADERS,
    }


class MsplNotification(PipeProducer):
    """
    Handles the AMQP server to receive the DARE policies and acts as an events producer for such policies.

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
        self._consumer = RabbitAsyncConsumer(config=settings, msg_callback=self.persist_policy)

        # Setup the instance as the events producer for the managed pipe.
        self.pipe.boot_in_sink(self)

    def setup(self):
        """
        The logic is provided by the RabbitMQ client hence nothing to do here.
        """
        pass

    def bootup(self):
        """
        Gets the AMQP server up and running. Also sets up the security recommendations queue to communicate with the
        DARE.
        """
        thread = Thread(target=self._consumer.run)
        thread.start()

    def persist_policy(self, body):
        """
        Persists the security policy and notifies the observers about the new policy.

        NOTE: exceptions should be caught be the caller.

        :param body: the actual security policy.
        """

        self.logger.info('Policy: %r', body)

        policy_persistence = MsplPersistence(config)

        tenant, policy = policy_persistence.persist(body)
        if tenant:
            self.logger.debug('Sending Notification: {}'.format(pprint(policy)))
            self.notify_by_tenant(policy, tenant)
