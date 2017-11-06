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
import threading

from abc import abstractmethod, ABCMeta


class PipeManager:
    """
    Connects a input sink with one or more output sinks. It is agnostic to the type of sink.

    The input and output sinks must comply with the observer pattern. The manager relinquishes control for input and
    output sinks instantiation and simply connects the sinks. The only 'clever' thing it does is to ensure that the
    output sink consumes the events produced by the input sink.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.in_sink = None
        self.out_sink = None

    def boot_in_sink(self, in_sink):
        """
        Configures and boots up the input sink. Once set no other sink is allowed as input.

        :param in_sink: The input sink object, compliant with the PipeProducer interface.
        """

        if self.in_sink is None:
            self.in_sink = in_sink
            self.in_sink.setup()
            threading.Thread(target=self.in_sink.bootup).start()

    def boot_out_sink(self, out_sink):
        """
        Configures and boots up the output sink. It also does the pumbling to associate the (new) output sink with
        the input sink so the events are properly conveyed. There can be as many output sinks as desired.

        :param out_sink: The output sink object, compliant with the PipeConsumer interface.
        """

        self.out_sink = out_sink
        self.out_sink.setup()

        # The output sink needs to know about the events on the input sink.
        self.in_sink.subscribe(self.out_sink)

        threading.Thread(target=self.out_sink.bootup).start()

    def shutdown(self):
        pass


class PipeProducer(metaclass=ABCMeta):
    """
    Generic events producer to attach to a 'pipe'. It follows the producer part of the observer pattern.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.subscribers = set([])

    def subscribe(self, subscriber):
        if subscriber not in self.subscribers:
            self.subscribers.add(subscriber)
            self.logger.debug('New subscriber: {}'.format(type(subscriber).__name__))

    def unroll(self, subscriber):
        self.subscribers.discard(subscriber)
        self.logger.debug('Subscriber removed: {}'.format(type(subscriber).__name__))

    def notify_all(self, data):
        for subscriber in self.subscribers:
            self.logger.debug('Notify {}'.format(type(subscriber).__name__))
            subscriber.update(data)

    @abstractmethod
    def setup(self):
        """
        Sets up the producer configuration. The implementation details are extended-class specific.
        """
        pass

    @abstractmethod
    def bootup(self):
        """
        Boots up the producer according to the configuration defined previously. The implementation details are
        extended-class specific.
        """
        pass


class PipeConsumer(metaclass=ABCMeta):
    """
    Generic events consumer to attach to a 'pipe'. It follows the consumer part of the observer pattern.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def setup(self):
        """
        Sets up the producer configuration. The implementation details are extended-class specific.
        """
        pass

    @abstractmethod
    def bootup(self):
        """
        Boots up the producer according to the configuration defined previously. The implementation details are
        extended-class specific.
        """
        pass

    @abstractmethod
    def update(self, data):
        """
        Defines the method to use as a notification by the producer (to the consumer) whenever a new event is
        available.The implementation details are extended-class specific.

        :param data: The data provided by the producer.
        """
        pass
