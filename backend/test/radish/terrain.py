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
import tempfile
from radish import before, after, world
from shutil import rmtree


@before.all
def setup(features, marker):
    world.my_context = dict()
    world.my_context['msgq_connection'] = None
    world.my_context['msgq_channel'] = None
    world.my_context['socket'] = dict()
    world.my_context['socket_output_file'] = tempfile.NamedTemporaryFile(delete=False).name


@before.each_scenario
def setup_scenario(step):
    # Avoid poisoning mocked responses for the vNSFO.
    if os.path.exists(world.env['mock']['vnsfo_folder']):
        rmtree(world.env['mock']['vnsfo_folder'])

    # Mock vNSFO context.
    step.context.mock_vnsfo = dict()

    # API context.
    step.context.api = dict()
    step.context.api['response'] = dict()


@after.all
def cleanup(features, marker):
    if world.my_context['msgq_connection'] is not None:
        world.my_context['msgq_connection'].close()

    if world.my_context['socket'] is not None:
        for tenant in world.my_context['socket'].keys():
            world.my_context['socket'][tenant].close()

    if os.path.isfile(world.my_context['socket_output_file']):
        os.remove(world.my_context['socket_output_file'])
