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

import threading

import websocket


class SendOnlySocketClient:
    """
    Creates a receive-only socket which conveys the data received to a callback function.

    The callback function is responsible for handling the data as it sees fit and do whatever it requires with the
    output provided in the instantiation.
    """

    def __init__(self, url, callback, output=None):
        self._callback = callback
        self._output = output

        # websocket.enableTrace(True)
        self._ws = websocket.WebSocketApp(url,
                                          on_message=self.on_message,
                                          on_error=self.on_error)

        def run(*args):
            self._ws.run_forever()

        threading.Thread(target=run).start()

    def on_message(self, ws, message):
        self._callback(message, self._output)

    @staticmethod
    def on_error(ws, error):
        print('Socker Error: ' + str(error))

    def close(self):
        self._ws.close()
