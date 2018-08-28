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
from datetime import datetime, timezone
from threading import Thread

from dashboardutils.pipe import PipeProducer
from dashboardutils.rabbit_client import RabbitAsyncConsumer
from dashboardutils.tenant_ip_utils import get_tenant_by_ip, AssociationCodeError, MultipleAssociation
from influxdb import InfluxDBClient
from settings import ASSOCIATION_API_URL, INFLUXDB_HOST, INFLUXDB_PORT, INFLUXDB_USER, INFLUXDB_USER_PASSWORD, \
    INFLUXDB_DB


class AttackProcessor(PipeProducer):
    __INTERNAL_IP_CACHE__ = {}
    INTERNAL_CACHE_SIZE = 50000

    #
    # Line Format:
    # csv_id, severity, attack_type, timereceived, Year, Month, Day, hour, minutes, seconds, duration, src_ip, dst_ip,
    # s_port, d_port, protocol, in_pkt, in_bytes, out_pkts, out_bytes, score
    #
    # Tags: ['src_ip', 'dst_ip', 's_port', 'd_port', 'protocol']
    # Fields: ['duration', 'in_pkt', 'in_bytes', 'out_pkts', 'out_bytes', 'score']
    __csv__ = {
        "header": [
            "csv_id", "severity", "attack_type", "timereceived", "Year", "Month", "Day", "hour", "minutes",
            "seconds", "duration", "src_ip", "dst_ip", "s_port", "d_port", "protocol", "in_pkt", "in_bytes",
            "out_pkts", "out_bytes", "score"
        ],
        "tag_indexes": [2, 12],
        "field_indexes": [0, 1, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20],
        "time_index": 3,
        "tenant_index": 12
    }

    logger = logging.getLogger(__name__)

    SPLIT_CHAR = '\t'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    MEASUREMENT = 'attack'

    def __init__(self, settings, pipe):
        """
        :param settings: The AMQP queue settings.
        :param pipe: The pipe manager where this instance is to be identified as an events producer.
        """

        super().__init__()

        self.logger = logging.getLogger(__name__)

        self.influx_client = None

        self.pipe = pipe
        self._consumer = RabbitAsyncConsumer(config=settings, msg_callback=self.process_message)

        # Setup the instance as the events producer for the managed pipe.
        self.pipe.boot_in_sink(self)

    def setup(self):
        self.influx_client = InfluxDBClient(
            INFLUXDB_HOST, INFLUXDB_PORT, INFLUXDB_USER, INFLUXDB_USER_PASSWORD, INFLUXDB_DB
        )

    def bootup(self):
        thread = Thread(target=self._consumer.run)
        thread.start()

    def process_message(self, body):
        body = body.decode() if isinstance(body, (bytes, bytearray)) else body
        message = body.split(self.SPLIT_CHAR)

        # Validate message length
        if len(message) != 21:
            self.logger.error("Invalid incoming message")
            return

        # Get tenant
        tenant = self.parse_tenant(message[self.__csv__['tenant_index']])
        if not tenant:
            return

        # Build tag str
        tag_dict = {self.__csv__['header'][index]: message[index] for index in self.__csv__['tag_indexes']}
        tag_dict["tenant"] = tenant

        # Build field dict
        field_dict = {self.__csv__['header'][index]: message[index] for index in self.__csv__['field_indexes']}

        json_body = [{
            "measurement": "attack",
            "time": self.__build_timestamp__(message[self.__csv__['time_index']]),
            "tags": tag_dict,
            "fields": field_dict
        }]

        self.influx_client.write_points(json_body)

    def parse_tenant(self, ip):
        """
        Given the destination IP address find the related tenant.
        The association is found by means of a dictionary or by requesting the association IP directly
        """

        # search the IP on the Internal Cache
        if ip in self.__INTERNAL_IP_CACHE__:
            return self.__INTERNAL_IP_CACHE__[ip]

        try:
            _tenant = get_tenant_by_ip(ASSOCIATION_API_URL, ip)

            # Clears the IP cache
            if len(self.__INTERNAL_IP_CACHE__) > self.INTERNAL_CACHE_SIZE:
                self.__INTERNAL_IP_CACHE__ = {}

            self.__INTERNAL_IP_CACHE__[ip] = _tenant  # Store the association on the dictionary

            return _tenant
        except MultipleAssociation:
            self.logger.error(f"The given IP: {ip} has none or multiple associations")
        except AssociationCodeError as e:
            self.logger.error(f"There was an error making the IP association {e.status_code}")
        return None

    def __build_timestamp__(self, datestring):
        new_date = datetime.strptime(datestring, self.DATE_FORMAT)
        timestamp = int(new_date.replace(tzinfo=timezone.utc).timestamp())  # Return POSIX UTC timestamp
        return timestamp * 1000 * 1000 * 1000  # ms us ns
