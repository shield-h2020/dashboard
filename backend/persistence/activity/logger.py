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


import requests
import logging
import time
from dashboardutils import http_utils
from keystone_adapter import KeystoneAuthzApi
import settings as cfg

class ActivityLogger:

    def __init__(self, backend_api_url):
        self.logger = logging.getLogger(__name__)
        self.backend_api_url = backend_api_url

    def _get_token_data(self, token):
        aaa = KeystoneAuthzApi(protocol=cfg.AAA_PROTOCOL,
                               host=cfg.AAA_HOST,
                               port=cfg.AAA_PORT,
                               username=cfg.AAA_SVC_ADMIN_USER,
                               password=cfg.AAA_SVC_ADMIN_PASS,
                               service_admin=cfg.AAA_SVC_ADMIN_SCOPE)
        return aaa.get_token_data(token)

    def log(self, message, auth_token):

        token_data = self._get_token_data(auth_token)

        url = f'{self.backend_api_url}/activity'
        headers = {'Content-Type': 'application/json'}

        try:
            payload = {
                'timestamp':   time.time(),
                'message':     message,
                'user_id':     token_data['token']['user']['id'],
                'user_name':   token_data['token']['user']['name'],
                'tenant_id':   token_data['token']['domain']['id'],
                'tenant_name': token_data['token']['domain']['name']
            }
            r = requests.post(url, headers=headers, json=payload, verify=False)
            if not r.status_code == http_utils.HTTP_201_CREATED:
                self.logger.error('Failed to create activity log for the payload:\n{}'
                                  .format(payload))
                return

        except requests.exceptions.ConnectionError as e:
            self.logger.error('Error connecting to the activity endpoint at {}.'.format(url), e)
            return
