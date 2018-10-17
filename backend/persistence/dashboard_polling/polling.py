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
import logging
import threading
from queue import Queue


class CheckableQueue(Queue):

    logger = logging.getLogger(__name__)

    def __init__(self, maxsize=0):
        super().__init__(maxsize)
        self._id = uuid.uuid4()
        self.logger.info(f"Generating queue {self._id}")

    def put(self, item, block=True, timeout=None):
        if item is None or item not in self.queue:
            super().put(item, block, timeout)
            return True
        return False

    def __contains__(self, item):
        with self.mutex:
            return item in self.queue


class Worker:
    logger = logging.getLogger(__name__)

    def __init__(self, polling_queue, processor, workers=5):
        self._id = uuid.uuid4()
        self.queue = polling_queue
        self.processor = processor
        self.threads = []
        self.workers = workers
        self.logger.info(f"Created Worker with id {self._id}")

    def start(self):
        self.logger.info(f"Starting Worker {self._id}")
        for i in range(self.workers):
            t = threading.Thread(target=self.work)
            t.start()
            self.threads.append(t)

    def stop(self):
        self.queue.join()

        # stop workers
        for i in range(self.workers):
            self.queue.put(None)
        for t in self.threads:
            t.join(1)
        self.logger.info(f"Worker {self._id} stopped")

    def work(self):
        while True:
            item = self.queue.get()
            if item is None:
                self.logger.debug(f"Exiting worker on worker {self._id}")
                break
            self.processor(item)
            self.queue.task_done()
