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


import json
from pprint import pformat
import logging
from vnsfo.vnsfo import VnsfoFactory, VnsfoNotSupported
from vnsfo.vnsfo_adapter import VnsfOrchestratorPolicyIssue
import settings as cfg
import flask
from flask import abort, make_response, jsonify
import requests
from dashboardutils import http_utils

class NssInventoryHooks:
    """
    Handles the backstage operations required for the Network Services Inventory part of the Dashboard API. These
    operations are mostly targeted at pre and post hooks associated with the API.
    """

    @staticmethod
    def provision_network_service(items):
        user_data = items[0]

        # TODO: If more than one "where" lookup there's an error in the URL query parameters.
        lookup = json.loads(flask.request.args.getlist('where')[0])
        print('lookup: ' + pformat(lookup))

        # The tenant ID must be set according to the one provided in the URL (which has been properly authorized).
        user_data['tenant_id'] = lookup['tenant_id']

    @staticmethod
    def instantiate_network_service(updates, original):

        logger = logging.getLogger(__name__)

        # request instantiation only if current status is 'available'
        if not original['status'] == 'available':
            logger.error("Cannot instantiate network service '{}'. "
                         "Current status is '{}'".format(original['ns_id'], original['status']))
            abort(make_response(jsonify(**{"_status": "ERR", "_error":
                                        {"code": 418, "message":
                                            "Instantiation failed. Improper status of network service"}}), 418))
            return

        # get network service data from Store
        url = "http://{}:{}/nss/{}".format(cfg.STORE_HOST, cfg.STORE_PORT, original['ns_id'])
        logger.debug("Connecting to store: {}".format(url))

        try:
            r = requests.get(url)

            if not r.status_code == http_utils.HTTP_200_OK:
                # TODO: raise exception
                logger.error("Couldn't retrieve data of Network Service '%s'", original['ns_id'])
                abort(make_response(jsonify(**{"_status": "ERR", "_error":
                                    {"code": r.status_code, "message":
                                        "Instantiation failed. Store replied: {}".format(r.text())}}), r.status_code))

        except requests.exceptions.ConnectionError as e:
            #  TODO: raise exception
            logger.error("Couldn't connect to Store: {}".format(e))
            abort(make_response(jsonify(**{"_status": "ERR", "_error":
                                {"code": 404, "message":
                                    "Instantiation failed. Store is unavailable"}}), 404))
            return

        # Retrieve relevant network service parameters
        r = r.json()
        ns_id = r['ns_id']
        ns_name = r['ns_name']
        target = r['manifest']['manifest:ns']['target']
        print("\n\n\nRetrieved ns_id: '{}', ns_name: '{}' target: {}\n\n".format(ns_id, ns_name, target))

        try:
            vnsfo = VnsfoFactory.get_orchestrator('OSM', cfg.VNSFO_PROTOCOL, cfg.VNSFO_HOST, cfg.VNSFO_PORT,
                                                  cfg.VNSFO_API)
            r = vnsfo.instantiate_ns(ns_name, target)
            if not r:
                logger.error("FAILED instantiation of network service '{}'".format(ns_name))
                message = r.text if r.text else r.json() if r.json() else None
                abort(make_response(jsonify(**{"_status": "ERR", "_error":
                                    {"code": r.status_code, "message":
                                        "Instantiation failed. vNSFO replied: {}".format(message)}}), r.status_code))
                return

            r = r.json()
            updates['status'] = "configuring"
            updates['instance_id'] = r['instance_id']

        except VnsfOrchestratorPolicyIssue or VnsfoNotSupported:
            logger.error('VnsfOrchestratorPolicyIssue')
            abort(make_response(jsonify(**{"_status": "ERR", "_error":
                                {"code": 400, "message":
                                    "Instantiation failed. vNSFO Policy Issue not supported".format(r.text())}}), 400))

        # Trigger NS Instance polling
        url = "{}/ns_instance_update".format(cfg.BACKENDAPI)
        json_instance_update = {
            "ns_instance_id": updates['instance_id']
        }
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, json=json_instance_update, headers=headers, verify=False)
        if not r.status_code == http_utils.HTTP_201_CREATED:
            updates['status'] = "available"
            logger.error("Failed to trigger polling for NS instance_id '{}'".format(updates['instance_id']))
            abort(make_response(jsonify(**{"_status": "ERR", "_error":
                                {"code": 500, "message":
                                    "Instantiation failed. Failed to trigger polling for NS instance_id '{}'"
                                        .format(updates['instance_id'])}}), 500))

        logger.debug("NS instance_id '{}' instantiation cess was successful".format(updates['instance_id']))

    @staticmethod
    def terminate_network_service(updates, original):

        logger = logging.getLogger(__name__)

        # request termination only if current status is 'running'
        if not original['status'] == 'running':
            logger.error("Cannot terminate network service '{}'. "
                         "Current status is '{}'".format(original['ns_id'], original['status']))
            abort(make_response(jsonify(**{"_status": "ERR", "_error":
                                {"code": 418, "message":
                                    "Termination failed. Improper status of network service"}}), 418))
            return

        instance_id = original['instance_id']

        logger.debug("Terminating network service '{}'".format(original['ns_id']))

        try:
            vnsfo = VnsfoFactory.get_orchestrator('OSM', cfg.VNSFO_PROTOCOL, cfg.VNSFO_HOST, cfg.VNSFO_PORT,
                                                  cfg.VNSFO_API)
            r = vnsfo.terminate_ns(instance_id)
            if not r:
                logger.error("FAILED termination of network service instance id '{}'".format(instance_id))
                abort(make_response(jsonify(**{"_status": "ERR", "_error":
                                    {"code": r.status_code, "message":
                                        "Instantiation failed. vNSFO replied: {}".format(r.text())}}), r.status_code))
                return
            r = r.json()
            updates['status'] = "available"
            updates['instance_id'] = ''

        except VnsfOrchestratorPolicyIssue or VnsfoNotSupported:
            logger.error('VnsfOrchestratorPolicyIssue')
            abort(make_response(jsonify(**{"_status": "ERR", "_error":
                                {"code": 400, "message":
                                    "Instantiation failed. vNSFO Policy Issue not supported".format(r.text())}}), 400))
