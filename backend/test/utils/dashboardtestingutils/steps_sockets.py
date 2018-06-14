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
import os
from time import sleep

from dashboardtestingutils.socket_client import ReceiveOnlySocketClient
from dashboardtestingutils.steps_rmsq import *
from dashboardtestingutils.steps_utils import *
from radish import world


# TODO: Documentation
# TODO: Refactor policy tests to use this class


def msg_handler(message, output_file):
    """
    Callback function for when a message is received on the socket. Every new message
    overwrites the output file.

    :param message: The socket message.
    :param output_file: The file path where to store the received message.
    """

    # Any exception will cause a test failure which is the intended behaviour.
    with open(output_file, 'w') as f:
        json.dump(json.loads(message), f)


def check_socket_message(step, expected_notification):
    """
    Using the output file the function compares the message receive with what is expected.
    """
    if world.my_context['socket'] is None:
        raise EnvironmentError('vNSF notification Socket must be up and running!!!')

    # Ensure that the system under test has enough time to send the notification.
    sleep(1)
    with open(world.my_context['socket_output_file'], 'r') as f:
        actual_data = json.load(f)

    with open(os.path.join(world.env['data']['expected_output'], expected_notification), 'r') as f:
        expected_data = json.load(f)

    matches_json(actual_data, expected_data)


def set_socket_client(url, callback=msg_handler):
    """
    Creates a new socket client in the given URL
    :param url: The endpoint to connect the client
    :param callback: Function to handle the received message
    """
    if world.my_context['socket'] is not None:
        return
    world.my_context['socket'] = ReceiveOnlySocketClient(url=url, callback=callback,
                                                         output=world.my_context['socket_output_file'])
