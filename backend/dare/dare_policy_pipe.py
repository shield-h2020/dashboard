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


import logging

import settings as cfg
from dashboarddare.dare_policy_q import DarePolicyQ
from dashboarddare.dashboard_socket import DashboardSocket
from dashboardutils import log
from dashboardutils.pipe import PipeManager

dare_queue_settings = {
    'host': cfg.MSGQ_HOST,
    'port': cfg.MSGQ_PORT,
    'user': 'guest',
    'pass': 'guest',
    'exchange': cfg.MSGQ_EXCHANGE_DASHBOARD,
    'exchange_type': cfg.MSGQ_EXCHANGE_TYPE,
    'queue': cfg.MSGQ_DARE,
    'queue_ack': cfg.MSGQ_DARE_ACK,
    'topic': cfg.MSGQ_DARE_TOPIC
}

dashboard_socket_settings = {
    'port': cfg.SKT_PORT
}

if __name__ == '__main__':
    log.setup_logging()
    logger = logging.getLogger(__name__)

    #                             1. pipe
    #   +-----------+           +------------+           +-----------+
    #   | DARE      | 2. input  | Pipe       | 3. output | Dashboard |
    #   | Queue     | +-------> | Manager    | <-------+ | Socket    |
    #   +-----------+           +------------+           +-----------+
    #         |                                                ^
    #         |                                                |
    #         +------------------------------------------------+
    #                         4. convey policies
    #
    # The DARE policies are conveyed to the Dashboard through a pipe which connects the DARE input queue with the
    # socket output. This process requires the following steps:
    #
    #   1. Create the DARE->Dashboard connection pipe
    #   2. Setup a queue and bolt it to the pipe as an events producer.
    #   3. Setup a web socket and bolt it to the pipe as an events consumer.
    #   4. The pipe plumbing is done and the policies are auto-magically received in the DARE queue and conveyed to
    #      the socket.

    manager = PipeManager()
    DarePolicyQ(dare_queue_settings, manager)
    DashboardSocket(dashboard_socket_settings, manager)