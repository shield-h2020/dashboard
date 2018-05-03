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
import re
import websocket
from dashboardtestingutils.socket_client import ReceiveOnlySocketClient
from dashboardtestingutils.steps_utils import *
from dashboardutils import http_utils
from radish import given, when, then, world
from radish.stepmodel import Step
from shutil import copyfile


@when(re.compile(u'I receive a security recommendation (.*)'))
def security_policy(step, policy):
    if world.my_context['msgq_channel'] is None:
        raise EnvironmentError('Recommendations Queue must be up and running!!!')

    with open(os.path.join(world.env['data']['input_data'], policy), 'r') as msg:
        world.my_context['msgq_channel'].basic_publish(exchange=world.env['hosts']['msg_q']['exchange'],
                                                       routing_key=world.env['hosts']['msg_q']['topic'],
                                                       body=msg.read())


@then(re.compile(u'The security recommendation must be persisted (.*)'))
def is_policy_persisted(step, policy):
    # Ensure that the system under test has time to persist the recommendation.
    sleep(1)

    http_get(step, world.endpoints['policies_latest'])
    matches_json_file(step, policy)


@then(re.compile(u'The security recommendation notification must be received (.*)'))
def check_policy_notification(step, expected_notification):
    if world.my_context['socket'] is None:
        raise EnvironmentError('Recommendations Socket must be up and running!!!')

    # Ensure that the system under test has enough time to send the notification.
    sleep(1)

    with open(world.my_context['socket_output_file'], 'r') as f:
        actual_data = json.load(f)

    with open(os.path.join(world.env['data']['expected_output'], expected_notification), 'r') as f:
        expected_data = json.load(f)

    matches_json(actual_data, expected_data)


@given(re.compile(u'I mock the latest security recommendation (.*)'))
def persist_policy(step, policy):
    with open(os.path.join(world.env['data']['input_data'], policy), 'r') as mspl:
        # set_http_headers(step, {'Content-Type': 'application/json'})
        http_post_json(step, world.endpoints['policies_admin'], json.load(mspl))
        expected_status_code(step, http_utils.HTTP_201_CREATED)

        # Ensure that the system under test has enough time to send the notification.
        sleep(1)


@when(u'I want to apply the latest security recommendation')
def apply_latest_policy(step):
    #
    #  Set the proper vNSFO response.
    #
    dest_file = os.path.join(world.env['mock']['vnsfo_folder'], world.mock_vnsfo_endpoints['apply_policy'],
                             'index.post.json')
    dest_path = os.path.dirname(dest_file)
    if not os.path.exists(dest_path):
        os.makedirs(dest_path, exist_ok=True)

    src_file = os.path.join(world.env['mock']['vnsfo_data'], step.context.mock_vnsfo['response_file'])
    assert os.path.isfile(src_file)
    copyfile(src_file, dest_file)

    #
    #  Get latest policy data.
    #
    http_get(step, world.endpoints['policies_latest'])
    expected_status_code(step, http_utils.HTTP_200_OK)

    #
    # Apply the latest policy.
    #
    url = '{}/{}'.format(world.endpoints['policies_apply'], step.context.api['response']['json']['_items'][0]['_id'])
    set_http_headers(step, {'If-Match': step.context.api['response']['json']['_items'][0]['_etag']})
    http_patch_json(step, url, {'status': 'Applied'})


@when(u'I check the Recommendations Queue')
def recommendations_queue_check(step):
    connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=world.env['hosts']['msg_q']['host'],
                                      port=world.env['hosts']['msg_q']['port']))
    channel = connection.channel()

    channel.exchange_declare(exchange=world.env['hosts']['msg_q']['exchange'],
                             exchange_type=world.env['hosts']['msg_q']['exchange_type'])

    # TODO Need to check whether the exchange exists and is ready. What about the queue?
    step.state = Step.State.PENDING

    connection.close()


@given(u'The Recommendations Queue is ready')
def recommendations_queue_ready(step):
    if world.my_context['msgq_channel'] is not None:
        return

    world.my_context['msgq_connection'] = pika.BlockingConnection(
            pika.ConnectionParameters(host=world.env['hosts']['msg_q']['host'],
                                      port=world.env['hosts']['msg_q']['port']))

    world.my_context['msgq_channel'] = world.my_context['msgq_connection'].channel()

    world.my_context['msgq_channel'].exchange_declare(exchange=world.env['hosts']['msg_q']['exchange'],
                                                      exchange_type=world.env['hosts']['msg_q']['exchange_type'])


@when(u'I check the Recommendations Socket')
def recommendations_socket_check(step):
    """
    Connecting to a socket that isn't available yields the 'WebSocketBadStatusException: Handshake status 404'
    exception so no further checks are needed for the step purpose.
    """

    ws = websocket.create_connection(world.env['hosts']['socket']['host'])
    ws.close()


@given(u'The Recommendations Socket is ready')
def recommendations_socket_ready(step):
    """
    Connecting to a socket that isn't available yields the 'WebSocketBadStatusException: Handshake status 404'
    exception so no further checks are needed for the step purpose.
    """

    if world.my_context['socket'] is not None:
        return

    world.my_context['socket'] = ReceiveOnlySocketClient(url=world.env['hosts']['socket']['host'],
                                                         callback=recommendations_socket_msg,
                                                         output=world.my_context['socket_output_file'])


def recommendations_socket_msg(message, output_file):
    """
    Callback function for when a security recommendation is received on the socket. Every new recommendation
    overwrites the output file.

    :param message: The security recommendation.
    :param output_file: The file path where to store the recommendation received in the socket.
    """

    # Any exception will cause a test failure which is the intended behaviour.
    with open(output_file, 'w') as f:
        json.dump(json.loads(message), f)
