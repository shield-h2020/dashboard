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


tm_notification = {
    'type': 'dict',
    'allow_unknown': True,
    'schema': {
        'hosts': {
            'type': 'list',
            'allow_unknown': True,
            'schema': {
                'node': 'string',
                'status': 'integer',
                'remediation': {
                    'type': 'dict',
                    'schema': {
                        'isolate': 'boolean',
                        'update': 'boolean',
                        'reboot': 'boolean'
                    }
                },
                'vnsfs': {
                    'type': 'list',
                    'allow_unknown': True,
                    'schema': {
                        'vnsf_id': 'string',
                        'vnsfd_name': 'string',
                        'remediation': {
                            'type': 'dict',
                            'schema': {
                                'isolate': 'boolean',
                                'update': 'boolean',
                                'reboot': 'boolean'
                            }
                        }
                    }
                },
                'trust': 'boolean'
            }
        },
        'sdn': {
            'type': 'list',
            'allow_unknown': True,
            'schema': {
            }
        },
        'trust': 'boolean'
    }
}
