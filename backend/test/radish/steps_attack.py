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
import time

from dashboardtestingutils.steps_rmsq import *
from dashboardtestingutils.steps_utils import http_get, matches_json_file, http_post_json
from radish import when, world, then, given
from requests.auth import HTTPBasicAuth


@given(re.compile(u'A clean influx (.*)'))
def given_clean_db(step, measurement):
    clean_influx_db(step, measurement)


@then(re.compile(u'A clean influx (.*)'))
def then_clean_db(step, measurement):
    clean_influx_db(step, measurement)


def clean_influx_db(step, measurement):
    auth = HTTPBasicAuth(world.env['hosts']['influxdb']['admin_username'],
                         world.env['hosts']['influxdb']['admin_password'])
    params = {
        'db': 'cyberattack',
        'q': f'DROP MEASUREMENT {measurement}'
    }

    http_post_json(step, world.endpoints['influx_query'], auth=auth, params=params)


@when(re.compile(u'I receive an attack message with (.*)'))
def csv_attack_request(step, attack_message):
    # This function uses hardcoded rmq sender because it uses tests with multiple lines
    # and within the steps_rmsq.py the lines are not being read correctly.
    with open(os.path.join(os.path.join(world.env['data']['input_data']), attack_message), 'r') as file:
        for msg in file:
            world.my_context['msgq_channel'].basic_publish(exchange=world.env['hosts']['attack_msg_q']['exchange'],
                                                           routing_key=world.env['hosts']['attack_msg_q']['topic'],
                                                           body=msg)
            time.sleep(3)


@then(re.compile(u'The attack message must be stored (.*)'))
def csv_attack_influx_data(step, persisted_data):
    """
    Check the data is stored on the database
    """
    auth = HTTPBasicAuth(world.env['hosts']['influxdb']['username'], world.env['hosts']['influxdb']['password'])
    params = {
        'db': 'cyberattack',
        'q': 'SELECT Count("duration") FROM "attack" WHERE time > \'2018-01-01T00:00:00.000Z\''
             'AND time < \'2018-12-31T00:00:00.000Z\'',
        'pretty': 'true'
    }

    http_get(step, world.endpoints['influx_query'], auth=auth, params=params)

    matches_json_file(step, persisted_data)
