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


class MsplSocket(PipeConsumer):
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
    # the dictionary will store the tenant as the key
    clients = dict()

    def __init__(self, pipe):
        """
        :param pipe: The pipe manager where this instance is to be identified as an events consumer.
        """

        super().__init__()
        self.logger = logging.getLogger(__name__)

        # Get the socket up and running.
        self.pipe = pipe
        self.pipe.boot_out_sink(self)

    def setup(self):
        """
        The method currently is doing nothing since the setup is the server socket responsibility
        """
        pass

    def bootup(self):
        """
        The method currently is doing nothing since the bootup is the server socket responsibility
        """
        pass

    def register_socket(self, socket, **kwargs):
        """
        Register a socket handler instance as the underlying socket for communicating the policy.

        :param socket: The socket handler instance where to convey the notifications.
        :param kwargs: A tenant is given as keyword argument to be associated with the client
        """
        tenant = kwargs.get('tenant', None)
        self.logger.debug('Registered socket {} for tenant {}'.format(socket, tenant))
        if tenant and tenant in self.clients:
            self.clients[tenant].append(socket)
        elif tenant:
            self.clients[tenant] = [socket]
        else:
            # Discard the client since no tenant was provided
            self.logger.debug('Socket not registered as no tenant was provided')
            return

    def unroll_socket(self, socket, **kwargs):
        """
        Register a socket handler instance as the underlying socket for communicating the policy.

        :param socket: The socket handler instance where to convey the notifications.
        :param kwargs: A tenant is given as keyword argument to ease the search for the client
        """
        tenant = kwargs.get('tenant', None)
        self.logger.debug('Unrolled socket {} for tenant {}'.format(socket, tenant))
        if tenant and self.clients.get(tenant):
            self.clients.get(tenant).remove(socket)

    def update(self, data, **kwargs):
        """
        Called when a new policy is received in the input pipe.

        :param data: The policy data provided.
        :param kwargs: A tenant is given as keyword argument so the notification is sent only to the clients connected
        to the same tenant

        """
        tenant = kwargs.get('tenant', None)
        if not tenant:
            self.logger.debug('No tenant provided')
            return
        for socket in self.clients.get(tenant, []):
            self.logger.debug('Socket {} | tenant {} | message - {}'.format(socket, tenant, data))

            try:
                socket.write_message(data)
            except WebSocketClosedError:
                self.logger.debug('Socket not available %r', socket)
