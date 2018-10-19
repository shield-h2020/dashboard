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
import logging
from pprint import pprint
from threading import Thread
import requests

import settings as cfg
from dashboardutils import http_utils
from dashboardutils.pipe import PipeProducer
from dashboardutils.rabbit_client import RabbitAsyncConsumer

from .vnsfo_notification_persistence import VnsfoNotificationPersistence

config = {
    'persist_url_notification_vnsfo': cfg.VNSFO_NOTIFICATION_API_PERSIST_HOST_URL,
    'persist_headers_notification_vnsfo': cfg.VNSFO_NOTIFICATION_API_PERSIST_HOST_HEADERS
}


class VNSFONotification(PipeProducer):
    """
    Handles the AMQP server to receive the NS Instance notifications and acts as an events producer for such notifications.

    How an AMQP server gets up and running is the responsibility of this class. When it does this is up to a pipe
    manager provided upon instantiation. All this class needs to do for the manager is to present itself as an events
    producer.
    """

    def __init__(self, settings, pipe, boot=True):
        """
        :param settings: The AMQP queue settings.
        :param pipe: The pipe manager where this instance is to be identified as an events producer.
        """

        super().__init__()

        self.logger = logging.getLogger(__name__)

        self.pipe = pipe
        self._consumer = RabbitAsyncConsumer(config=settings, msg_callback=self.persist_notification)

        if boot:
            # Setup the instance as the events producer for the managed pipe.
            self.pipe.boot_in_sink(self)

    def setup(self):
        """
        The logic is provided by the RabbitMQ client hence nothing to do here.
        """
        pass

    def bootup(self):
        """
        Gets the AMQP server up and running.
        """
        thread = Thread(target=self._consumer.run)
        thread.start()

    def persist_notification(self, body):
        """
        Persists the vNSFO notification and notifies the observers about the new notification.
        TODO: For now, this notification should be triggered by the polling thread that is watching vNSFO ns/running instances
        NOTE: exceptions should be caught by the caller.
        :param body: the actual notification.
        """

        self.logger.info('vNSFO Notification: %r', body)

        notifications = json.loads(body)

        notification_persistence = VnsfoNotificationPersistence(config)

        if 'type' not in notifications or 'data' not in notifications or not notifications['type'] == 'ns_instance':
            self.logger.error("Received invalid notification: {}".format(notifications))
            return

        data = notifications['data']
        ns_instance_id = data['instance_id']
        op_status = data['operational_status']
        vnsf_instances = data['vnsf_instances']
        ns_name = data['ns_name']

        if not op_status == "running":
            self.logger.error("Notification for NS instance_id '{}' has an invalid running status '{}'"
                              .format(ns_instance_id, op_status))
            return

        # 1. Retrieve the tenant associated with this instance_id in nss inventory
        self.logger.debug("-> Retrieving tenant associated with NS instance_id '{}'".format(ns_instance_id))
        url = '{}?where={{\"instance_id\": \"{}\"}}'.format(cfg.VNSFO_NOTIFICATION_API_INVENTORY_NSS_URL, ns_instance_id)
        self.logger.debug("\n\nRequesting URL: {}\n\n".format(url))
        r = requests.get(url)
        if not r.status_code == http_utils.HTTP_200_OK:
            # TODO: raise exception
            self.logger.error("Couldn't retrieve the tenant associated with NS instance_id '{}'".format(ns_instance_id))
            return
        r = r.json()
        tenant_id = r['_items'][0]['tenant_id']
        ns_id = r['_items'][0]['ns_id']
        inventory_nss_id = r['_items'][0]['_id']
        inventory_nss_etag = r['_items'][0]['_etag']
        self.logger.debug("NS instance_id '{}' is associated with tenant_id '{}'".format(ns_instance_id, tenant_id))

        # 2. Update tenant associations with vNSF instances running under this ns_instance_id
        self.logger.debug('Updating tenant <-> vNSF instances association')
        headers = cfg.TENANT_VNSF_INSTANCE_ASSOCIATION_HEADERS

        url = '{}/{}'.format(cfg.TENANT_VNSF_INSTANCE_ASSOCIATION_URL, tenant_id)

        r = requests.get(url, headers=headers)

        # if this tenant doesn't have any record of association -> create it
        if r.status_code == http_utils.HTTP_404_NOT_FOUND:
            self.logger.debug("The tenant_id '{}' doesn't have any association record of vNSF Instances. Creating it."
                              .format(tenant_id))
            url = '{}'.format(cfg.TENANT_VNSF_INSTANCE_ASSOCIATION_URL)
            post_json = {
	            "tenant_id": tenant_id,
	            "vnsf_instances": vnsf_instances
            }
            r = requests.post(url, json=post_json, headers=headers, verify=False)
            if not r.status_code == http_utils.HTTP_201_CREATED:
                self.logger.debug("Couldn't create tenant <-> vNSF instances association: {}".format(post_json))
                return

        # if this tenant already has a record of association -> patch it and removing old vnsf instances
        elif r.status_code == 200:
            r = r.json()
            etag = r['_etag']
            headers['If-Match'] = etag

            patch_json = {
                "vnsf_instances": vnsf_instances
            }

            r = requests.patch(url, headers=headers, json=patch_json, verify=False)
            if not r.status_code == http_utils.HTTP_200_OK:
                self.logger.debug("Couldn't update tenant_id {} <-> vNSF instances association: {}".format(tenant_id, patch_json))
                return

        # Persist the notification
        notification_persistence.persist_ns_instance(ns_instance_id, op_status)

        # Everything went ok, update status of NS instance to 'running'

        url = '{}/{}?where={{\"tenant_id\": \"{}\"}}'.format(cfg.VNSFO_NOTIFICATION_API_INVENTORY_NSS_URL,
                                                            inventory_nss_id, tenant_id)
        self.logger.debug("Updating NS instance_id '{}' status to 'running'".format(ns_instance_id))
        headers = cfg.VNSFO_NOTIFICATION_API_INVENTORY_NSS_HEADERS
        headers['If-Match'] = inventory_nss_etag
        update_json = {
            "status": "running"
        }
        r = requests.patch(url, headers=headers, json=update_json, verify=False)
        if not r.status_code == http_utils.HTTP_200_OK:
            self.logger.debug("Couldn't update instance_id {} to 'running' status".format(ns_instance_id))
            return

        # Notify by tenant
        notification_json = {
            "type": "ns_instance",
            "instance_id": ns_instance_id,
            "ns_id": ns_id,
            "ns_name": ns_name,
            "result": 'success' if op_status == 'running' else 'failure'
        }
        self.logger.debug('Sending Notification: {}'.format(notification_json))
        self.notify_by_tenant(notification_json, tenant_id)
