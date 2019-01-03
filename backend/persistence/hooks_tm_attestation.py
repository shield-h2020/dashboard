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

import settings as cfg
import requests
from vnsfo.vnsfo import VnsfoFactory
from dashboardutils import http_utils
import threading
import logging

logger = logging.getLogger(__name__)


class TMAttestation:

    def __init__(self):
        self._node_id = None


    @staticmethod
    def tm_attest_all(items):

        url = "https://{}/nfvi_attestation_info".format(cfg.TM_HOST)

        t = threading.Thread(
            target=TMAttestation.tm_attest_async_request,
            args=[url])
        t.start()


    @staticmethod
    def tm_attest_node(items):

        if not items[0]['node_id']:
            logger.error("A node identifier is required to trigger the attestation")
            return

        node_id = items[0]['node_id']

        url = "https://{}/nfvi_pop_attestation_info?node_id={}" \
              .format(cfg.TM_HOST, node_id)

        t = threading.Thread(
            target=TMAttestation.tm_attest_async_request,
            args=[url])
        t.start()


    @staticmethod
    def tm_attest_async_request(url):

        # trigger attestation in trust monitor
        logger.debug("Connecting to Trust Monitor: {}".format(url))

        try:
            r = requests.get(url, verify=False)

            if not r.status_code == http_utils.HTTP_200_OK:
                logger.error("Trust Monitor replied with a failed attestation: {}"
                             .format(url))

            logger.debug("Got reply from Trust Monitor attest request: {}\n{}"
                         .format(url, r.json()))

        except requests.exceptions.ConnectionError as e:
            logger.error("Couldn't connect to Trust Monitor: {}".format(e))
