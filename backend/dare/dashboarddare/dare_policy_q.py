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


import pika
from os import abort

import settings as cfg
from dashboardutils import http_codes
from dashboardutils.pipe import PipeProducer
from .secpolicy_persistence import SecurityPolicyPersistence, SecurityPolicyNotComplaint, SecurityPolicyNotPersisted

config = {
    'tenant_id': cfg.VNSFO_TENANT_ID,
    'policy_schema': cfg.POLICYSCHEMA_FILE,
    'persist_url': cfg.POLICYAPI_PERSIST_URL,
    'persist_headers': cfg.POLICYAPI_PERSIST_HEADERS
}


class DarePolicyQ(PipeProducer):
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
        :param logger: Logger object.
        """

        super().__init__()

        self._settings = settings
        self.pipe = pipe
        self._channel = None

        # Setup the instance as the events producer for the managed pipe.
        self.pipe.boot_in_sink(self)

    def setup(self):
        """
        Gets the AMQP server up and running. Also sets up the security recommendations queue to communicate with the
        DARE.
        """

        self.logger.info(
            '[DAREQ] Starting AMQP server at {} with exchange {}, queue {} and topic {}'.format(self._settings['host'],
                                                                                                self._settings[
                                                                                                    'exchange'],
                                                                                                self._settings[
                                                                                                    'dare_queue'],
                                                                                                self._settings[
                                                                                                    'dare_topic']))

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._settings['host']))
        self._channel = connection.channel()

        self._channel.exchange_declare(exchange=self._settings['exchange'],
                                       exchange_type=self._settings['exchange_type'])
        self._channel.queue_declare(queue=self._settings['dare_queue'])

        self._channel.queue_bind(exchange=self._settings['exchange'],
                                 queue=self._settings['dare_queue'],
                                 routing_key=self._settings['dare_topic'])

    def bootup(self):
        """
        Starts to listen for DARE messages in the queue.
        """

        self._channel.basic_consume(self.persist_dare_policy,
                                    queue=self._settings['dare_queue'],
                                    no_ack=not self._settings['dare_queue_ack'])

        self.logger.info('[DAREQ] [*] Waiting for messages. To exit press CTRL+C')
        self._channel.start_consuming()

    def persist_dare_policy(self, channel, basic_deliver, properties, body):
        """
        Persists the policy message. Also notifies the consumers about the new policy.

        :param channel: The channel where the message was received. Passed for your convenience.
        :param basic_deliver: Object that is passed in carries the exchange, routing key, delivery tag and a
        redelivered flag for the message.
        :param properties: The message properties. An instance of BasicProperties.
        :param body: The message received.
        """

        self.logger.info('[DARE POLICY] %r', body)

        try:
            policy_persistence = SecurityPolicyPersistence(config)
            policy = policy_persistence.persist(body)

            # Notify consumers about the new policy.
            self.notify_all(policy)

        except SecurityPolicyNotComplaint as e:
            abort(http_codes.HTTP_412_PRECONDITION_FAILED, e.message)

        except SecurityPolicyNotPersisted as e:
            abort(http_codes.HTTP_406_NOT_ACCEPTABLE, e.message)
