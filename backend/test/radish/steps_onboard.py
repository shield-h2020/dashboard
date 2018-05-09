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


from pprint import pformat

import re
from dashboardtestingutils.steps_utils import *
from radish import when


@when(re.compile(u'The Developer onboards a (.*)'))
def onboard_vnsf(step, vnsf_file):
    print('developer_info\n' + pformat(world.my_context['developer_info']))

    print('developer\n' + pformat(world.my_context['developer']))

    print('xpto')
    print('xpto')

    data = {'developer_id': world.my_context['developer']['token']['user']['id']}

    file = os.path.join(world.env['data']['input_data'], vnsf_file)
    files = {'package': open(file, 'rb')}

    http_post_file(step, url=world.endpoints['vnsfs'], files=files, data=data,
                   auth=(world.my_context['developer']['token']['id'], ''))
