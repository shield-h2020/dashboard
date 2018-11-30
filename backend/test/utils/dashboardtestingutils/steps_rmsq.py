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

from time import sleep

import os
import pika
from radish import given, world


@given(u'The Recommendations Queue is ready')
def recommendations_queue_ready(step):
    if world.my_context['msgq_channel'] is not None:
        return

    world.my_context['msgq_connection'] = pika.BlockingConnection(
            pika.ConnectionParameters(host=world.env['hosts']['mspl_msg_q']['host'],
                                      port=world.env['hosts']['mspl_msg_q']['port']))

    world.my_context['msgq_channel'] = world.my_context['msgq_connection'].channel()

    world.my_context['msgq_channel'].exchange_declare(exchange=world.env['hosts']['mspl_msg_q']['exchange'],
                                                      exchange_type=world.env['hosts']['mspl_msg_q']['exchange_type'])


def send_notification(input_data, channel, exchange, topic, data):
    if channel is None:
        raise EnvironmentError('Recommendations Queue must be up and running!!!')
    with open(os.path.join(input_data, data), 'r') as msg:
        channel.basic_publish(exchange=exchange, routing_key=topic,
                              body=msg.read())
    sleep(3)
