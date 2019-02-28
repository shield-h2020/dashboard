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

import uuid
import time
import logging
import requests
import settings as cfg
from queue import Queue
from dashboardutils import http_utils
from dashboardutils.rabbit_client import RabbitProducer
from apscheduler.schedulers.background import BackgroundScheduler



class BillingMonitor:

    def __init__(self, update_interval=1):
        self._id = uuid.uuid4()
        self._working = False
        self._update_interval = update_interval
        self._scheduler = BackgroundScheduler()
        self._job = None
        print("Created Billing Monitor")

    def start(self):
        print("Starting Billing Monitor Scheduler")
        self._job = self._scheduler.add_job(self.work, 'interval', minutes=self._update_interval)

        # TODO: enable scheduler after testing phase
        # self._scheduler.start()

    def stop(self):
        self._working = False
        self._job.remove()
        self._scheduler.shutdown()
        print("Billing Monitor Scheduler stopped")

    def work(self):
        print("Triggering update to billing information data")

        # Trigger NS Instance polling
        url = "{}/billing/update".format(cfg.BACKENDAPI)
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, json={}, headers=headers, verify=False)

        if not r.status_code == http_utils.HTTP_201_CREATED:
            print("Failed to trigger update. Got error code: {}".format(r.status_code))
