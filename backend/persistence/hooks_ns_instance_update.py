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
import logging

import settings as cfg
from dashboard_polling.polling import CheckableQueue, Worker
from dashboard_polling.processor import VNSFONSInstanceProcessor



class NSInstanceHooks:
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.queue = CheckableQueue()
        self.worker = Worker(self.queue, VNSFONSInstanceProcessor(cfg.VNSFO_PROTOCOL, cfg.VNSFO_HOST, cfg.VNSFO_PORT,
                                                                  cfg.VNSFO_API).processor, workers=4)
        self.worker.start()

    def post_ns_instance(self, request, payload):

        data = json.loads(request.data)
        item = {
            "instance_id": data["ns_instance_id"],
            "nfvo_version": data['nfvo_version']
        }

        if self.queue.put(item):
            self.logger.debug(f"Add new item to the processing queue {data['ns_instance_id']}")
        else:
            self.logger.debug(f"Item, {data['ns_instance_id']} already on the processing queue")


