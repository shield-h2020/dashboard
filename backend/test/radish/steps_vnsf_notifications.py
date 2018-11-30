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
import re
from dashboardtestingutils.steps_rmsq import *
from dashboardtestingutils.steps_sockets import *
from dashboardtestingutils.steps_utils import *
from radish import given, when, then, world


@given(re.compile(u'A vnsf notification socket is ready for (.*)'))
def set_vnsf_socket(step, tenant):
    set_socket_client(world.sockets_endpoints['vnsf_notification'].format(tenant), tenant)


@when(re.compile(u'I receive a VNSF notification with (.*)'))
def vnsf_notification(step, notification):
    send_notification(
            os.path.join(world.env['data']['input_data']),
            world.my_context['msgq_channel'], world.env['hosts']['vnsf_msg_q']['exchange'],
            world.env['hosts']['vnsf_msg_q']['topic'], notification)


@then(re.compile(u'The vNSF notification must be persisted (.*)'))
def is_vnsf_notification_persisted(step, notification):
    # Ensure that the system under test has time to persist the recommendation.
    sleep(3)

    http_get(step, world.endpoints['vnsf_notifications_latest'])
    matches_json_file(step, notification)


@then(re.compile(u'The vNSF notification must be received (.*)'))
def check_vnsf_notification(step, expected_notification):
    check_socket_message(step, expected_notification)
