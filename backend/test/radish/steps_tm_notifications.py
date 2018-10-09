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

import os
import re
from time import sleep

from dashboardtestingutils.steps_rmsq import *
from dashboardtestingutils.steps_sockets import *
from dashboardtestingutils.steps_utils import *
from radish import given, when, then, world


@given(re.compile(u'A TM notification socket is ready'))
def set_host_socket(step):
    pass


@given(re.compile(u'A TM VNSF notification socket is ready for (.*)'))
def set_vnsf_socket(step, tenant):
    set_socket_client(world.sockets_endpoints['tm_vnsf_notification'].format(tenant), tenant)


@when(re.compile(u'I receive a TM notification with (.*)'))
def tm_notification(step, notification):
    send_notification(
        os.path.join(world.env['data']['input_data']),
        world.my_context['msgq_channel'], world.env['hosts']['tm_msg_q']['exchange'],
        world.env['hosts']['tm_msg_q']['topic'], notification)


@then(re.compile(u'The TM host notification must be persisted (.*)'))
def is_tm_host_notification_persisted(step, notification):
    # Ensure that the system under test has time to persist the recommendation.
    sleep(3)

    http_get(step, world.endpoints['tm_host_notifications_latest'])
    matches_json_file(step, notification)


@then(re.compile(u'The TM sdn notification must be persisted (.*)'))
def is_tm_host_notification_persisted(step, notification):
    # Ensure that the system under test has time to persist the recommendation.
    sleep(3)

    http_get(step, world.endpoints['tm_sdn_notifications_latest'])
    matches_json_file(step, notification)


@then(re.compile(u'The TM VNSF notification must be persisted (.*)'))
def is_tm_vnsf_notification_persisted(step, notification):
    sleep(3)

    http_get(step, world.endpoints['tm_vnsf_notifications_latest'])
    matches_json_file(step, notification)


@then(re.compile(u'The TM notification must be received (.*)'))
def check_tm_notification(step, expected_notification):
    check_socket_message(step, expected_notification)


@then(re.compile(u'The TM VNSF notification must be received (.*)'))
def check_tm_notification(step, expected_notification):
    check_socket_message(step, expected_notification)