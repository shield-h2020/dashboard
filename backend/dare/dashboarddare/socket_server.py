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

from tornado.ioloop import IOLoop
from tornado.web import Application

from .sendonly_socket_handler import SendOnlySocketHandler


class TornadoSocketServer:
    """
    Creates the socket server. Gathers all websocket endpoints and initialize the IO loop instance once avoiding
    thread problems.
    """

    def __init__(self, settings, **controllers):
        """
        :param settings: The socket settings.
        :param controllers: kwargs with pipe controller objects. Each controller is an instance of a pipe receiver.
                            policy: Policy pipe receiver
                            vnsf:   vNSF notifications pipe receiver
                            tm:     Trust Monitor pipe receiver
        """
        self.logger = logging.getLogger(__name__)

        self.logger.debug('Starting Tornado Server')

        self.application = Application([

            # Frontend Interface.
            (r'/policy/(?P<tenant>\w+)$', SendOnlySocketHandler, {'controller': controllers.get('mspl')}),
            (r'/vnsf/notifications/(?P<tenant>\w+)$', SendOnlySocketHandler,
             {'controller': controllers.get('vnsf')}),
            (r'/tm/notifications/(?P<tenant>\w+)$', SendOnlySocketHandler,
             {'controller': controllers.get('tm')}),
            ])

        self._settings = settings
        self.setup()
        self.bootup()

    def setup(self):
        """
        Sets up a web socket on a specific port.
        """

        self.logger.debug('Setup')
        self.application.listen(port=self._settings['port'])

    def bootup(self):
        """
        Gets the Web socket up and running to communicate with the dashboard.
        """

        self.logger.info(
                'Starting web socket on port {}'.format(self._settings['port']))

        IOLoop.instance().start()
