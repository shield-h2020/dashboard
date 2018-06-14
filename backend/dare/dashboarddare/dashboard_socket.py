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

from dashboardutils.pipe import PipeConsumer
from tornado.websocket import WebSocketClosedError


class DashboardSocket(PipeConsumer):
    """
    Handles the web socket server to notify the Dashboard of new DARE policies acting as a consumer for such policies.

    How a web socket server gets up and running is the responsibility of this class. When it does this is up to a
    pipe manager provided upon instantiation. All this class needs to do for the manager is to present itself as an 
    events consumer.

    This class is to be used as an output sink for a pipe manager which consumes the policies and feeds them through
    a web socket. Thus it must implement two distinct behaviours: (i) act as a consumer and (ii) feed the socket. The
    first behaviour is already mentioned above and relates to the manager. The second behaviour needs a little hack
    as the web socket handler class has no direct relationship to this consumer class.

    When a producer notifies this class of a new policy it must convey it through the socket. The issue here is that
    this class doesn't play a part in instantiating the socket handler class and thus has no access to the socket
    itself. To make this all work together a hack is provided to the socket handler class whereas the socket
    'controller' class is supplied. This is only done with the purpose of allowing the socket handler class to
    register itself as a socket within the consumer class. This in turn allows the consumer class to convey the
    policy to the other party using the underlying socket.
    """

    # Clients connected to the socket.
    clients = set([])

    def __init__(self, pipe):
        """
        :param pipe: The pipe manager where this instance is to be identified as an events consumer.
        :param logger: Logger object.
        """

        super().__init__()
        self.logger = logging.getLogger(__name__)
        """
        self.application = Application([

            # Frontend Interface.
            (r'/policy', SecurityPolicySocketHandler, {'controller': self}),
        ])

        self._settings = settings
        """
        # Get the socket up and running.
        self.pipe = pipe
        self.pipe.boot_out_sink(self)

    def setup(self):
        """
        Sets up a web socket on a specific port.
        """
        """
        self.logger.debug('Setup')
        self.application.listen(port=self._settings['port'])
        """

    def bootup(self):
        """
        Gets the Web socket up and running to communicate with the dashboard.
        """
        """
        self.logger.info(
            'Starting web socket on port {}'.format(self._settings['port']))

        IOLoop.instance().start()
        """

    def register_socket(self, socket):
        """
        Register a socket handler instance as the underlying socket for communicating the policy.

        :param socket: The socket handler instance where to convey the policies.
        """
        self.logger.debug('Registered socket %r', socket)
        self.clients.add(socket)

    def unroll_socket(self, socket):
        """
        Register a socket handler instance as the underlying socket for communicating the policy.

        :param socket: The socket handler instance where to convey the policies.
        """
        self.logger.debug('Unrolled socket %r', socket)
        self.clients.discard(socket)

    def update(self, data, **kwargs):
        """
        Called when a new policy is received in the input pipe.

        :param data: The policy data provided.
        """

        for socket in self.clients:
            self.logger.debug('Socket %r | message - %r', socket, data)

            try:
                socket.write_message(data)
            except WebSocketClosedError:
                self.logger.debug('Socket not available %r', socket)
