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
from abc import ABCMeta, abstractmethod

from tornado.websocket import WebSocketHandler


class AbstractSocketHandler(WebSocketHandler, metaclass=ABCMeta):
    """
    Default behaviour for sockets.
    """

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.logger = logging.getLogger(__name__)

        self.controller = kwargs.get('controller')
        self.logger.debug('Initialize with controller: %r', self.controller)

    def initialize(self, **kwargs):
        """
        This method is called from within the super().__init__. To get the data provided in the usual place (
        __init__) this implementation only declares the user-defined variables here to avoid errors when assigning
        the intended values to them in the __init__.

        :param kwargs: the user-defined data.
        """

        # Socket controller instance (used for the subscriber pattern) to reference this socket instance.
        self.controller = None

    def open(self, **kwargs):
        self.logger.debug('New client connected - %r', self)
        self.controller.register_socket(self, **kwargs)

    def check_origin(self, origin):
        # Avoids CORS when using clients from localhost.
        return True

    def data_received(self, chunk):
        pass

    @abstractmethod
    def on_message(self, message):
        pass

    def on_close(self):
        self.logger.debug('Client disconnected - %r', self)
        self.controller.unroll_socket(self, **self.open_kwargs)
