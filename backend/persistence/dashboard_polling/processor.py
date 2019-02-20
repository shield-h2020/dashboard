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
import time
from abc import abstractmethod, ABCMeta
import json
import requests
import yaml
from dashboardutils import http_utils


class Processor(metaclass=ABCMeta):
    logger = logging.getLogger(__name__)

    def __init__(self, protocol, server, port, api_basepath):
        self.basepath = f'{protocol}://{server}:{port}'
        if api_basepath:
            self.basepath += f'/{api_basepath}'

    @abstractmethod
    def processor(self, item, *args, **kwargs):
        pass


class VNSFONSInstanceProcessor(Processor):

    def processor(self, item, *args, **kwargs):
        instance_id = item['instance_id']
        vnfvo_version = item['nfvo_version']

        ns_name = ''
        data = {}
        running_status = ''
        vnsf_instances = list()
        while running_status not in ['running', 'failed']:
            time.sleep(3)
            url = f"{self.basepath}/ns/{vnfvo_version}/running/{instance_id }"
            print("Polling url: '{}'".format(url))

            self.logger.debug(f"Polling NS instance '{instance_id }'")

            response = requests.get(url, verify=False)
            if not response.status_code == http_utils.HTTP_200_OK:
                # TODO: raise exception
                self.logger.error(f"Couldn't retrieve running NS instance_id '{instance_id }' from vNSFO.")
                running_status = 'failed'
                break

            # vNSFO API may return a json with single quotes, which is not a json standard
            # This hack loads the json response with the yaml loader which is more permissive
            print(response.text)
            data = yaml.load(response.text)

            print(data)

            if data['ns']:
                ns_name = data['ns'][0]['ns_name']
                running_status = data['ns'][0]['operational_status']
                self.logger.debug(f"Continuing to poll NS instance '{instance_id }'. Current status: {running_status }")

        self.logger.debug(f"NS instance '{instance_id }' polling terminated. vNSFO replied status: '{running_status }'")

        if running_status == 'running':
            for vnf_instance in data['ns'][0]['constituent_vnf_instances']:
                vnfr_id = vnf_instance['vnfr_id']
                vnsf_instances.append(vnfr_id)

            # vnsf_instances = list([vnf['vnfr_id'] for vnf in data['ns'][0]['constituent_vnf_instances']])
            # print(data['ns'][0]['constituent_vnf_instances'])

            self.logger.debug("vNSF Instances running: {}".format(vnsf_instances))

        # if not vnsf_instances:
        #     # TODO: raise exception
        #     self.logger.error(
        #         f"Couldn't retrieve associated vNSF instances with NS instance_id '{instance_id }' from vNSFO")
        #     return False

        message = {
            "type": "ns_instance",
            "data": {
                "instance_id": instance_id,
                "operational_status": running_status,
                "vnsf_instances": vnsf_instances,
                "ns_name": ns_name
            }
        }

        self.logger.debug("About to submit message to Queue, topic: {}".format(item['routing_key']))

        item['producer'].submit_message(message, item['routing_key'])
        return True
