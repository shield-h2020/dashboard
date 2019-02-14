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
import settings as cfg
import copy
import math
import datetime
import dateutil.parser
from dateutil.relativedelta import relativedelta
import calendar
from vnsfo.vnsfo import VnsfoFactory
from werkzeug.datastructures import ImmutableMultiDict
from flask import abort, make_response, jsonify
from eve.methods.get import get_internal, getitem_internal
from eve.methods.patch import patch_internal
from eve.methods.post import post_internal

from dashboardutils import http_utils
from keystone_adapter import KeystoneAuthzApi
import pprint
import logging
import requests
from flask import current_app


class BillingActions:

    @staticmethod
    def create_ns_billing_placeholder(request):
        """
        Creates the billing placeholder for a particular NS Billing.
        This should be invoked by the client/tenant admin immediately after the on-boarding of a new NS.
        The 'expense_fee' field is fulfilled automatically by gathering the fees of the NS constituent vNSFs.
        The 'fee' is left at its default value (0.0) - to later be fulfilled by the client/tenant admin.
        :param request: The user request containing a json object with only one field: 'ns_id'
        """

        logger = logging.getLogger(__name__)

        json_data = request.json

        if not 'ns_id' in json_data:
            logger.error("Failed to create billing placeholder for NS '{}': 'ns_id' value is required."
                         .format(json_data['ns_id']))
            abort(make_response(jsonify(**{"_status": "ERR", "_error": {"code": 422, "message":
                "Failed to create billing placeholder for NS '{}".format(json_data['ns_id'])}}), 422))

        logger.debug("Creating billing model for NS '{}'".format(json_data['ns_id']))

        # retrieve 'constituent_fee' by gathering the 'fee'
        # get network service data from Store
        url = "http://{}:{}/nss/{}".format(cfg.STORE_HOST, cfg.STORE_PORT, json_data['ns_id'])
        logger.debug("Connecting to store: {}".format(url))

        try:
            r = requests.get(url)

            if not r.status_code == http_utils.HTTP_200_OK:
                logger.error("Couldn't retrieve data of Network Service '%s'", json_data['ns_id'])
                abort(make_response(jsonify(**{"_status": "ERR", "_error": {"code": r.status_code, "message":
                    "Failed retrieving Network Service '{}'. Store replied: {}".format(json_data['ns_id'], r.text)}}),
                                    r.status_code))

        except requests.exceptions.ConnectionError as e:
            logger.error("Couldn't connect to Store: {}".format(e))
            abort(make_response(jsonify(**{"_status": "ERR", "_error":
                {"code": 404, "message":
                    "Failed retrieving Network Service '{}'. Store is unavailable".format(json_data['ns_id'])}}), 404))
            return

        # from retrieved ns, get constituent vnsf ids to retrive vnsfs billing in order to calculate NS expense
        ns_json = r.json()
        constituent_vnsfs = ns_json['constituent_vnsfs']
        expense_fee = BillingActions._calc_vnsfs_expense_fee(constituent_vnsfs)

        # fulfill te 'expense_fee'
        json_data['expense_fee'] = expense_fee
        json_data['constituent_vnsfs'] = constituent_vnsfs
        json_data['fee'] = 0.0

    @staticmethod
    def create_vnsf_billing_placeholder(request):
        """
        Creates the billing placeholder for a particular vNSF Billing.
        This should be invoked by the developer user immediately after the on-boarding of a new vNSF.
        The 'fee' is left with its default value (0.0) - later to be fulfilled by the developer.
        :param request: The user request containing a json object with only one field: 'vnsf_id'
        """

        logger = logging.getLogger(__name__)

        json_data = request.json

        if not 'vnsf_id' in json_data:
            logger.error("Failed to create billing placeholder for vNSF '{}': 'vnsf_id' value is required"
                         .format(json_data['vnsf_id']))
            abort(make_response(jsonify(**{"_status": "ERR", "_error": {"code": 422, "message":
                    "Failed to create billing placeholder for vNSF '{}".format(json_data['vnsf_id'])}}), 422))

        logger.debug("Creating billing model for vNSF {}".format(json_data['vnsf_id']))

        # retrieve 'user_id' based on the auth token
        token = current_app.auth.get_user_or_token()
        aaa = KeystoneAuthzApi(protocol=cfg.AAA_PROTOCOL,
                               host=cfg.AAA_HOST,
                               port=cfg.AAA_PORT,
                               username=cfg.AAA_SVC_ADMIN_USER,
                               password=cfg.AAA_SVC_ADMIN_PASS,
                               service_admin=cfg.AAA_SVC_ADMIN_SCOPE)
        token_data = aaa.get_token_data(token)
        json_data['user_id'] = token_data['token']['user']['id']
        json_data['fee'] = 0.0

        # note: no need to mess with 'fee' and 'support_fee' as they have a default value of 0.0 in the data model


    @staticmethod
    def _get_vnsf_id_from_store(vnsf_record_id):
        """
        Retrieves the vnsf_id from the Store based on the Store vnsf record id
        :param store_vnsf_record_id: the '_id' of the vNSF
        :return: vnsf_id
        """
        logger = logging.getLogger(__name__)

        url = "http://{}:{}/vnsfs/{}".format(cfg.STORE_HOST, cfg.STORE_PORT, vnsf_record_id)
        logger.debug("Connecting to store: {}".format(url))

        try:
            r = requests.get(url)
            if not r.status_code == http_utils.HTTP_200_OK:
                logger.error("Couldn't retrieve data of vNSF '%s' from the Store", vnsf_record_id)
                abort(make_response(jsonify(**{"_status": "ERR", "_error": {"code": r.status_code, "message":
                    "Failed retrieving vNSF '{}'. Store replied: {}".format(vnsf_record_id, r.text)}}), r.status_code))

        except requests.exceptions.ConnectionError as e:
            logger.error("Couldn't connect to Store: {}".format(e))
            abort(make_response(jsonify(**{"_status": "ERR", "_error": {"code": 404, "message":
                "Failed retrieving vNSF '{}'. Store is unavailable".format(vnsf_record_id)}}), 404))

        vnsf_json = r.json()
        return vnsf_json['vnsf_id']

    @staticmethod
    def _get_ns_id_from_store(ns_record_id):
        """
        Retrieves the ns_id from the Store based on the Store ns record id
        :param ns_record_id: the '_id' of the NS
        :return: ns_id
        """
        logger = logging.getLogger(__name__)

        url = "http://{}:{}/nss/{}".format(cfg.STORE_HOST, cfg.STORE_PORT, ns_record_id)
        logger.debug("Connecting to store: {}".format(url))

        try:
            r = requests.get(url)

            if not r.status_code == http_utils.HTTP_200_OK:
                logger.error("Couldn't retrieve data of NS '%s' from the Store", ns_record_id)
                abort(make_response(jsonify(**{"_status": "ERR", "_error": {"code": r.status_code, "message":
                    "Failed retrieving NS '{}'. Store replied: {}".format(ns_record_id, r.text)}}), r.status_code))

        except requests.exceptions.ConnectionError as e:
            logger.error("Couldn't connect to Store: {}".format(e))
            abort(make_response(jsonify(**{"_status": "ERR", "_error": {"code": 404, "message":
                "Failed retrieving NS '{}'. Store is unavailable".format(ns_record_id)}}), 404))

        ns_json = r.json()
        return ns_json['ns_id']

    @staticmethod
    def _calc_vnsfs_expense_fee(vnsf_ids):
        logger = logging.getLogger(__name__)
        logger.debug("Calculating expense fee for vnfs={}".format(vnsf_ids))

        # get constituent vNSFs for this ns_id
        expense_fee = 0.0

        # calculate expense fee
        for vnsf_id in vnsf_ids:
            # get vNSF Billing for this vnsf_id
            billing_vnsf = BillingActions._get_billing_vnsf(vnsf_id)
            expense_fee += billing_vnsf['fee']

        return expense_fee

    @staticmethod
    def set_billing_ns_fee(updates, original):
        """
        Updates the 'fee' of a particular NS Billing.
        Updating other parameters, such as 'expense_fee'
         is not allowed as they are calculated automatically.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Setting Billing 'fee' of NS {}".format(original['ns_id']))

        # don't allow updates to fields other than 'fee'
        restricted_fields = ['ns_id']

        for restricted_field in restricted_fields:
            if restricted_field in updates.keys():
                logger.error("Updates to fields other than 'fee' are not allowed.")
                abort(make_response(jsonify(**{"_status": "ERR", "_error": {"code": 409, "message":
                                    "Updates to fields other than 'fee' are not allowed."}}), 409))

        if not original['expense_fee']:
            logger.warning("Expense fee of NS {} is not defined".format(original['ns_id']))
            return

        # TODO: check the update of expense fee

    @staticmethod
    def set_billing_vnsf_fee(updates, original):
        """
        Updates fee of a particular vNSF Billing.
        Updating other parameters is not allowed as they are calculated automatically.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Setting vNSF Billing fee of vnsf_id={}".format(original['vnsf_id']))

        allowed_fields = ['fee', '_updated']
        print(sorted(list(updates.keys())))
        print(sorted(allowed_fields))
        if sorted(list(updates.keys())) != sorted(allowed_fields):
            logger.error("Specification of fields other than 'fee' is not allowed.")
            abort(make_response(jsonify(**{"_status": "ERR", "_error": {"code": 409, "message":
                                "Specification of fields other than 'fee' is not allowed."}}), 409))

        # TODO: Trigger NS Billing expense fees here or let it be done automatically in billing update?

    @staticmethod
    def _get_billing_ns_usage(ns_instance_id, month):
        logger = logging.getLogger(__name__)
        logger.debug("Retrieving 'billing_ns_usage' of NS instance id={} for month={}"
                     .format(ns_instance_id, month))

        with current_app.test_request_context():
            (ns_usage_data, _, _, status, _) = get_internal('billing_ns_usage', ns_instance_id=ns_instance_id, month=month)

            if not status == http_utils.HTTP_200_OK or ns_usage_data['_meta']['total'] != 1:
                logger.debug("The 'billing_ns_usage' of NS instance id={} for month={} does not exist."
                             .format(ns_instance_id, month))
                return None

            return ns_usage_data['_items'][0]

    @staticmethod
    def _get_billing_vnsf_usage(vnsf_id, month, fee):
        logger = logging.getLogger(__name__)
        logger.debug("Retrieving 'billing_vnsf_usage' of vnsf_id={} for month={} for fee={}"
                     .format(vnsf_id, month, fee))

        with current_app.test_request_context():
            (vnsf_usage_data, _, _, status, _) = get_internal('billing_vnsf_usage')
            if not status == http_utils.HTTP_200_OK or vnsf_usage_data['_meta']['total'] != 1:
                logger.debug("The 'billing_vnsf_usage' of vnsf_id={} for month={} for fee={} does not exist."
                             .format(vnsf_id, month, fee))
                return None

            for item in vnsf_usage_data['_items']:
                if item['vnsf_id'] == vnsf_id and item['month'] == month and item['fee'] == fee:
                    return item

    @staticmethod
    def start_billing_ns_usage(request):
        """
        Registers the start date on billing of particular NS instance.
        The only field allowed in the request is the 'ns_instance_id'.
        Remaining fields are calculated automatically.
        :param request:
            example:
            {
                "ns_instance_id": "instance_x",
            }
        """
        logger = logging.getLogger(__name__)

        # Ensure request form is in compliance
        allowed_fields = ['ns_instance_id']
        if not list(request.json.keys()) == allowed_fields:
            logger.error("Specification of fields other than 'ns_instance_id' is not allowed.")
            abort(make_response(jsonify(**{"_status": "ERR", "_error": {"code": 409, "message":
                                        "Specification of fields other than 'ns_instance_id' is not allowed."}}), 409))

        # Protect against inserting a new usage with the same ns_instance_id and month combination
        current_date = datetime.datetime.now()
        month = current_date.strftime('%Y-%m')
        ns_usage_item = BillingActions._get_billing_ns_usage(request.json['ns_instance_id'], month)
        if ns_usage_item:
            logger.error("NS Usage record for NS instance id={} and month={} already exists"
                         .format(request.json['ns_instance_id'], month))
            abort(make_response(jsonify(**{"_status": "ERR", "_error": {"code": 400, "message":
                                "NS Usage record for NS instance id={} and month={} already exists"
                                .format(request.json['ns_instance_id'], month)}}), 400))

        # Retrieve 'ns_id' and 'tenant_id' using the 'instance_id' from the nss_inventory
        logger.debug("Retrieving information about provided instance id {}".format(request.json['ns_instance_id']))
        # Returns a tuple: (response, last_modified, etag, status, headers)
        (instance_data, _, _, status, _) = get_internal('nss_inventory', instance_id=request.json['ns_instance_id'])

        if instance_data['_meta']['total'] == 0:
            logger.error("Couldn't retrieve information about provided NS instance id {}"
                         .format(request.json['ns_instance_id']))
            abort(make_response(jsonify(**{"_status": "ERR", "_error": {"code": 500, "message":
                                "Couldn't retrieve information about provided NS instance id '{}'"
                                        .format(request.json['ns_instance_id'])}}), 500))

        tenant_id = instance_data['_items'][0]['tenant_id']
        ns_id = instance_data['_items'][0]['ns_id']

        # Retrieve current fee from 'billing_ns' for this 'ns_id'
        fee = BillingActions._get_billing_ns(ns_id)['fee']
        used_from = current_date.date()
        used_to = current_date.date()

        # Assign calculated fields to post request
        request.json['tenant_id'] = tenant_id
        request.json['ns_id'] = ns_id
        request.json['usage_status'] = 'open'
        request.json['month'] = month
        request.json['used_from'] = used_from.isoformat()
        request.json['used_to'] = used_to.isoformat()
        request.json['fee'] = fee
        request.json['billable_percentage'] = BillingActions._get_usage_billable_percentage(
            used_from, used_to
        )
        request.json['billable_fee'] = BillingActions._get_usage_billable_fee(
            request.json['fee'], request.json['billable_percentage']
        )

        # Start Billing vNSF usage for constituent vNSFs
        constituent_vnsfs = BillingActions._get_billing_ns(ns_id)['constituent_vnsfs']
        logger.debug("Creating Billing vNSF Usages for vnsfs={}".format(constituent_vnsfs))
        for vnsf_id in constituent_vnsfs:
            BillingActions._start_billing_vnsf_usage(vnsf_id)

    @staticmethod
    def _start_billing_vnsf_usage(vnsf_id):
        logger = logging.getLogger(__name__)

        # Get current fee for this vnsf_id from 'billing_vnsf'
        billing_vnsf = BillingActions._get_billing_vnsf(vnsf_id)
        fee = billing_vnsf['fee']

        # Protect against inserting a new usage with the same [vnsf_id, month, fee] combination
        current_date = datetime.datetime.now()
        month = current_date.strftime('%Y-%m')
        billing_vnsf_usage = BillingActions._get_billing_vnsf_usage(vnsf_id, month, fee)
        if billing_vnsf_usage:
            logger.debug("vNSF Usage record for vnsf_id={} and month={} and fee={} already exists. Nothing to do."
                         .format(vnsf_id, month, fee))
            return

        used_from = current_date.date()
        used_to = current_date.date()
        billable_percentage = BillingActions._get_usage_billable_percentage(used_from, used_to)
        billable_fee = BillingActions._get_usage_billable_fee(fee, billable_percentage)

        with current_app.test_request_context():
            payload = {
                'vnsf_id': vnsf_id,
                'usage_status': 'active',
                'fee': fee,
                'user_id': billing_vnsf['user_id'],
                'used_from': used_from.isoformat(),
                'used_to': used_to.isoformat(),
                'month': month,
                'billable_percentage': billable_percentage,
                'billable_fee': billable_fee
            }
            logger.debug("Creating vNSF usage for vnsf_id={} and month={} and fee={}"
                         .format(vnsf_id, month, fee))
            (result, _, etag, status, _) = post_internal("billing_vnsf_usage", payload)
            if status != http_utils.HTTP_201_CREATED:
                logger.error("Failed to create 'billing_vnsf_usage' for vnsf_id={}".format(vnsf_id))
                return

    @staticmethod
    def _get_usage_billable_percentage(used_from, used_to):
        logger = logging.getLogger(__name__)
        if not used_from.year == used_to.year or not used_from.month == used_to.month:
            logger.error("Can't calculate billing percentage ranging different months")
            abort(make_response(jsonify(**{"_status": "ERR", "_error": {"code": 500, "message":
                                "Can't calculate billing percentage ranging different months '{}' and '{}'"
                                .format(used_from.isoformat(), used_to.isoformat())}}), 500))

        (_, year_month_days) = calendar.monthrange(used_from.year, used_from.month)
        billable_days = used_to.day - used_from.day + 1
        return round((billable_days*100) / year_month_days, 2)

    @staticmethod
    def _get_usage_billable_fee(monthly_fee, percentage):
        return round((percentage * monthly_fee) / 100, 2)

    @staticmethod
    def stop_billing_ns_usage(updates, original):
        """
        Registers the start date on billing of particular NS instance.
        Fields such as 'ns_id', 'tenant_id', 'used_from', 'fee', 'used_to' should not be sent in the request,
        they are fulfilled automatically.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Stopping Billing Usage of NS instance '{}'".format(original['ns_instance_id']))
        current_date = datetime.datetime.now()
        used_from = dateutil.parser.parse(original['used_from'])
        used_to = current_date.date()

        # Update calculated fields
        updates['used_to'] = used_to.isoformat()
        updates['usage_status'] = 'closed'
        updates['billable_percentage'] = BillingActions._get_usage_billable_percentage(
            used_from, used_to
        )
        updates['billable_fee'] = BillingActions._get_usage_billable_fee(
            original['fee'], updates['billable_percentage']
        )

    @staticmethod
    def get_billins_ns_usage(response):
        """
        Gets information about a the billing of a NS usage.
        On top of the database data it adds useful information, such as NS instance status and total billable fee
        """
        logger = logging.getLogger(__name__)
        logger.debug("Fetching NS Billing Usages")
        total_billable_fee = 0.0
        for item in response['_items']:
            item['instance_status'] = BillingActions._get_ns_instance_status(item['ns_instance_id'])
            total_billable_fee += item['billable_fee']

        response['total_billable_fee'] = round(total_billable_fee, 2)

    @staticmethod
    def get_billing_vnsf_usage(response):
        """
        Gets information about a the billing of a vNSF usage.
        On top of the database data it adds useful information, such as total billable fee
        """
        logger = logging.getLogger(__name__)
        logger.debug("Fetching vNSF Billing Usages")
        total_billable_fee = 0.0
        for item in response['_items']:
            total_billable_fee += item['billable_fee']

        response['total_billable_fee'] = round(total_billable_fee, 2)

    @staticmethod
    def get_billing_ns_usage_item(response):
        """
        Gets Billing NS usage for an item.
        On top of the database data it adds useful information, such as NS instance status.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Fetching NS Billing Item Usage")
        response['instance_status'] = BillingActions._get_ns_instance_status(response['ns_instance_id'])

    @staticmethod
    def _get_running_ns_instances(ns_id):
        logger = logging.getLogger(__name__)
        logger.debug("Fetching NS Instances of ns_id={}".format(ns_id))

        ns_instances = list()
        with current_app.test_request_context():
            (nss_inventory_data, _, _, status, _) = get_internal('nss_inventory')
            if not status == http_utils.HTTP_200_OK or nss_inventory_data['_meta']['total'] == 0:
                logger.debug("Couldn't find NS instances for ns_id={}".format(ns_id))
                return

            for item in nss_inventory_data['_items']:
                if item['ns_id'] == ns_id and item['status'] == 'running':
                    ns_instances.append(item['instance_id'])

            return ns_instances

    @staticmethod
    def _get_ns_instance_status(ns_instance_id):
        # retrieve current billing ns usage data
        with current_app.test_request_context():
            (nss_inventory_data, _, _, status, _) = get_internal('nss_inventory', instance_id=ns_instance_id)
            print("status: {}".format(status))
            print("nss_inventory_data: {}".format(nss_inventory_data))

            if not status == http_utils.HTTP_200_OK or nss_inventory_data['_meta']['total'] == 0:
                abort(make_response(jsonify(**{"_status": "ERR", "_error": {"code": 500, "message":
                                    "Failed retrieving status of NS instance '{}'".format(ns_instance_id)}}), 500))

            return 'terminated' if nss_inventory_data['_items'][0]['status'] != 'running' else 'running'

    @staticmethod
    def _get_billing_ns(ns_id):
        logger = logging.getLogger(__name__)
        logger.debug("Retrieving current Billing NS for NS id='{}'".format(ns_id))
        with current_app.test_request_context():
            # retrieve current billing ns usage data
            (billing_ns_data, _, _, status, _) = get_internal('billing_ns', ns_id=ns_id)
            if not status == http_utils.HTTP_200_OK or billing_ns_data['_meta']['total'] != 1:
                abort(make_response(jsonify(**{"_status": "ERR", "_error": {"code": 500, "message":
                      "Failed retrieving billing for NS '{}'".format(ns_id)}}), 500))

            return billing_ns_data['_items'][0]

    @staticmethod
    def _get_billing_vnsf(vnsf_id):
        logger = logging.getLogger(__name__)
        logger.debug("Retrieving current Billing vNSF for vnsf_id='{}'".format(vnsf_id))

        with current_app.test_request_context():
            # retrieve current billing ns usage data
            (billing_vnsf_data, _, _, status, _) = get_internal('billing_vnsf', vnsf_id=vnsf_id)
            if not status == http_utils.HTTP_200_OK or billing_vnsf_data['_meta']['total'] != 1:
                abort(make_response(jsonify(**{"_status": "ERR", "_error": {"code": 500, "message":
                      "Failed retrieving billing for vnsf_id={}".format(vnsf_id)}}), 500))

            return billing_vnsf_data['_items'][0]

    @staticmethod
    def update_billing(request):
        """
        This hook triggers the update of all top-down billing information, such as
        billing_ns_usage, billing_vnsf_usage, billing_ns_summary and billing_vnsf_summary
        """
        logger = logging.getLogger(__name__)
        logger.info("Updating Billing Information")

        BillingActions._update_billing_ns()
        BillingActions._update_billing_usage()
        BillingActions._update_billing_summary()




    @staticmethod
    def _update_billing_ns():
        logger = logging.getLogger(__name__)
        logger.debug("Updating Billing NS parameters, such as expense fees")

        # retrieve current billing ns data
        (billing_ns_data, _, _, status, _) = get_internal('billing_ns')

        for billing_ns in billing_ns_data['_items']:
            logger.debug("Processing Billing NS ns_id={}".format(billing_ns['ns_id']))
            expense_fee = BillingActions._calc_vnsfs_expense_fee(billing_ns['constituent_vnsfs'])

            with current_app.test_request_context():
                payload = {
                    'expense_fee': expense_fee
                }
                lookup = {"_id": billing_ns['_id']}
                (result, _, etag, status) = patch_internal("billing_ns", payload, **lookup)
                if status != http_utils.HTTP_200_OK:
                    logger.error("Failed to update 'billing_ns' ns_id={}".format(billing_ns['_id']))
                    return

    @staticmethod
    def _update_billing_usage():
        logger = logging.getLogger(__name__)
        logger.debug("Updating Billing NS Usage")

        # retrieve current billing ns usage data
        (ns_usage_data, _, _, status, _) = get_internal('billing_ns_usage')

        # process NS instances
        for item in ns_usage_data['_items']:
            logger.debug("Processing NS Instance '{}' of NS '{}' belonging to Tenant {}"
                         .format(item['ns_instance_id'], item['ns_id'], item['tenant_id']))

            instance_status = BillingActions._get_ns_instance_status(item['ns_instance_id'])

            # get current date
            current_date = datetime.datetime.now().date()

            if instance_status == 'terminated':
                logger.debug("NS Instance '{}' status is terminated. Skipping.".format(item['ns_instance_id']))

                # in case that 'usage_status' is still open -> close it
                if item['usage_status'] == 'open':
                    logger.debug("NS Instance '{}' status is terminated however the 'billing_ns_usage' "
                                 "status is still open. Closing it.".format(item['ns_instance_id']))
                    BillingActions._update_billing_ns_usage(current_date,
                                                            item,
                                                            dateutil.parser.parse(item['used_to']).date())
                continue

            # get 'used_from' date
            used_from = dateutil.parser.parse(item['used_from']).date()

            # current month no longer applies to this ns usage record
            if current_date.year > used_from.year or current_date.month > used_from.month:
                logger.debug("Current date month is higher in NS Usage instance id={} month={}"
                             .format(item['ns_instance_id'], item['ns_id']))

                # skip if this month's usage record is already closed
                if item['usage_status'] == 'closed':
                    continue

                # calculate 'used_to' for this month's usage record
                (_, year_month_last_day) = calendar.monthrange(used_from.year, used_from.month)
                used_to = datetime.datetime(used_from.year, used_from.month, year_month_last_day).date()

                # close this month's usage record
                logger.debug("Closing usage of NS instance={} month={}".format(item['ns_instance_id'], item['month']))

                BillingActions._update_billing_ns_usage(current_date, item, used_to)

                # for each month up to current month, get 'billing_ns_usage' if existent and update it,
                # otherwise create new 'billing_ns_usage' record
                time_delta = relativedelta(used_to, used_from)
                months_delta = time_delta.months + time_delta.years * 12 + (1 if time_delta.days else 0)

                print("Dealing with months delta = {}".format(months_delta))
                # TODO: check if this delta is correct!

                for i in range(months_delta):

                    # calculate 'used_from' for this month's record
                    used_from = (datetime.datetime(used_from.year, used_from.month, 1) + relativedelta(months=1)).date()

                    # determine 'used_to' based on the current year/month
                    if current_date.year == used_from.year and current_date.month == used_from.month:
                        used_to = current_date
                    else:
                        (_, year_month_last_day) = calendar.monthrange(used_from.year, used_from.month)
                        used_to = datetime.datetime(used_from.year, used_from.month, year_month_last_day).date()

                    # get month's usage record
                    month = used_from.strftime('%Y-%m')
                    ns_usage_item = BillingActions._get_billing_ns_usage(item['ns_instance_id'], month)

                    # 'ns_billing_usage' does not exist for this ns_instance_id and month -> create it
                    if not ns_usage_item:
                        logger.debug("The 'billing_ns_usage' for NS instance id={} of month={} does not exist. "
                                     "Creating it.")
                        BillingActions._create_billing_ns_usage(
                            current_date,
                            item['ns_instance_id'],
                            item['tenant_id'],
                            item['ns_id'],
                            month,
                            used_from,
                            used_to,
                        )

                    # 'ns_billing_usage' already exists for this ns_instance_id and month
                    else:
                        # check if it is closed
                        if ns_usage_item['usage_status'] == 'closed':
                            # do nothing. silently ignore
                            continue

                        logger.debug("Updating NS Usage of instance_id={} and month={}"
                                     .format(item['ns_instance_id'], item['month']))

                        # update 'billing_ns_usage' of this month's record
                        BillingActions._update_billing_ns_usage(current_date, item, used_to)

            # current month applies to this ns usage record
            else:
                logger.debug("Current date month is within the NS Usage instance id={} month={}"
                             .format(item['ns_instance_id'], item['ns_id']))
                logger.debug("Updating NS Usage of instance_id={} and month={} to current date."
                             .format(item['ns_instance_id'], item['month']))

                if current_date < used_from:
                    logger.error("The system datetime clock was set ahead of time at some point. Skipping update.")
                    continue

                # update 'billing_ns_usage' of current month's record
                BillingActions._update_billing_ns_usage(current_date, item, current_date)

    @staticmethod
    def _create_billing_ns_usage(current_date, ns_instance_id, tenant_id, ns_id, month, used_from, used_to):
        logger = logging.getLogger(__name__)
        logger.debug("Creating usage of NS instance={}, month={}, used_from={}, used_to={}"
                     .format(ns_instance_id, month, used_from.isoformat(), used_to.isoformat()))

        fee = BillingActions._get_billing_ns(ns_id)['fee']
        billable_percentage = BillingActions._get_usage_billable_percentage(used_from, used_to)
        billable_fee = BillingActions._get_usage_billable_fee(fee, billable_percentage)
        instance_status = BillingActions._get_ns_instance_status(ns_instance_id)
        (_, year_month_last_day) = calendar.monthrange(used_from.year, used_from.month)
        if current_date.day == year_month_last_day:
            logger.debug("Last day of the month {}: Closing usage of NS instance={}"
                         .format(month, ns_instance_id))
            usage_status = 'closed'
        else:
            usage_status = 'open' if instance_status == 'running' else 'closed'

        with current_app.test_request_context():
            payload = {
                'ns_instance_id': ns_instance_id,
                'ns_id': ns_id,
                'tenant_id': tenant_id,
                'usage_status': usage_status,
                'month': month,
                'used_from': used_from.isoformat(),
                'used_to': used_to.isoformat(),
                'fee': fee,
                'billable_percentage': billable_percentage,
                'billable_fee': billable_fee
            }
            (result, _, etag, status, _) = post_internal("billing_ns_usage", payload)
            print("-------> creation status: {}, result: {}".format(status, result))
            if status != http_utils.HTTP_201_CREATED:
                logger.error("Failed to create 'billing_ns_usage' for NS Instance '{}'"
                             .format(item['ns_instance_id']))
                return

    @staticmethod
    def _update_billing_ns_usage(current_date, item, used_to):
        logger = logging.getLogger(__name__)
        logger.debug("Updating usage of NS instance={} month={}".format(item['ns_instance_id'], item['month']))

        used_from = dateutil.parser.parse(item['used_from']).date()
        billable_percentage = BillingActions._get_usage_billable_percentage(used_from, used_to)
        billable_fee = BillingActions._get_usage_billable_fee(item['fee'], billable_percentage)
        instance_status = BillingActions._get_ns_instance_status(item['ns_instance_id'])

        if current_date.month > used_to.month:
            logger.debug("NS Instance={} used up to last day of the month={}. Closing usage record."
                         .format(item['ns_instance_id'], item['month']))
            usage_status = 'closed'
        else:
            usage_status = 'open' if instance_status == 'running' else 'closed'

        with current_app.test_request_context():
            payload = {
                'used_to': used_to.isoformat(),
                'billable_percentage': billable_percentage,
                'billable_fee': billable_fee,
                'usage_status': usage_status
            }
            lookup = {"_id": item['_id']}
            (result, _, etag, status) = patch_internal("billing_ns_usage", payload, **lookup)
            if status != http_utils.HTTP_200_OK:
                logger.error("Failed to update 'billing_ns_usage' id '{}'".format(item['_id']))
                return

    @staticmethod
    def _add_item_control_ns_summary(ns_summary, item):

        # add tenant dict
        if item['tenant_id'] not in ns_summary.keys():
            ns_summary[item['tenant_id']] = dict()
        tenant = ns_summary[item['tenant_id']]

        # add tenant->month dict
        if item['month'] not in tenant.keys():
            tenant[item['month']] = dict()
        month = tenant[item['month']]

        # add tenant->month->ns_instances list
        if 'ns_instances' not in month:
            month['ns_instances'] = list()
        ns_instances = month['ns_instances']

        # add tenant->month->nss list
        if 'nss' not in month:
            month['nss'] = list()
        nss = month['nss']

        # append item ns_instance_id if not existent
        if item['ns_instance_id'] not in ns_instances:
            ns_instances.append(item['ns_instance_id'])

        # append item ns_id to tenant->month->nss and create it if not existent
        if item['ns_id'] not in nss:
            nss.append(item['ns_id'])

        # add tenant->month->billable_fee if not existent
        if 'billable_fee' not in month.keys():
            month['billable_fee'] = 0

        #  add tenant->month->status if not existent
        if 'status' not in month.keys():
            month['status'] = 'closed'

        # increase tenant->month->billable_fee of item billable_fee
        month['billable_fee'] += item['billable_fee']

        # set tenant->month->status to open if item is open
        if item['usage_status'] == 'open':
            month['status'] = 'open'

    @staticmethod
    def _add_item_control_vnsf_summary(vnsf_summary, item):

        # add user_id dict
        if item['user_id'] not in vnsf_summary.keys():
            vnsf_summary[item['user_id']] = dict()
        user = vnsf_summary[item['user_id']]

        # add month dict
        if item['month'] not in user.keys():
            user[item['month']] = dict()
        month = user[item['month']]

        # add month->vnsfs list if not existent
        if 'vnsfs' not in month.keys():
            month['vnsfs'] = list()
        vnsfs = month['vnsfs']

        # add month->status if not existent
        if 'status' not in month.keys():
            month['status'] = 'closed'

        # add month->billable_fee if not existent
        if 'billable_fee' not in month.keys():
            month['billable_fee'] = 0

        #  add month->status if not existent
        if 'status' not in month.keys():
            month['status'] = 'closed'

        # add vnsf to month->vnsfs if still not there
        if item['vnsf_id'] not in vnsfs:
            vnsfs.append(item['vnsf_id'])

        # increase month->billable_fee of item billable_fee
        month['billable_fee'] += item['billable_fee']
        month['number_vnsfs'] = len(vnsfs)

        # set tenant->month->status to open if item is open
        if item['usage_status'] == 'active':
            month['status'] = 'open'

    @staticmethod
    def _update_billing_summary():
        logger = logging.getLogger(__name__)
        logger.debug("Updating Billing NS Summary")

        ns_summary = dict()

        # crawl trough current billing ns usage data to populate ns_summary
        (ns_usage_data, _, _, status, _) = get_internal('billing_ns_usage')
        for item in ns_usage_data['_items']:
            logger.debug("Processing NS Instance '{}' of NS '{}' belonging to Tenant {}"
                         .format(item['ns_instance_id'], item['ns_id'], item['tenant_id']))

            BillingActions._add_item_control_ns_summary(ns_summary, item)

        logger.debug("Retrieved the following Billing NS Summary:\n {}".format(pprint.pformat(ns_summary)))

        # cycle through ns_summary tenants->months and retrieve its billing ns summary
        for tenant, months in ns_summary.items():
            for month, item in ns_summary[tenant].items():
                (ns_summary_data, _, _, status, _) = get_internal('billing_ns_summary',
                                                                  tenant_id=tenant,
                                                                  month=month)

                # if summary for this tenant->month doesn't exist > create it (post)
                if not status == http_utils.HTTP_200_OK or ns_summary_data['_meta']['total'] == 0:
                    logger.debug("Billing NS Summary of tenant id={} and month={} does not exist. Creating it."
                                 .format(tenant, month))

                    with current_app.test_request_context():
                        payload = {
                            'tenant_id': tenant,
                            'month': month,
                            'number_nss': len(item['nss']),
                            'number_ns_instances': len(item['ns_instances']),
                            'status': item['status'],
                            'billable_fee': item['billable_fee']
                        }
                        (result, _, etag, status, _) = post_internal("billing_ns_summary", payload)
                        logger.debug("Created NS Summary for tenant id={} and month={}".format(tenant, month))
                        if status != http_utils.HTTP_201_CREATED:
                            logger.error("Failed to create 'billing_ns_summary' for tenant id={} and month={}"
                                         .format(tenant, month))
                            continue  # or return?

                # if summary for this tenant->month exist -> update it (patch)
                else:
                    billing_ns_summary_id = ns_summary_data['_items'][0]['_id']
                    with current_app.test_request_context():
                        payload = {
                            'number_nss': len(item['nss']),
                            'number_ns_instances': len(item['ns_instances']),
                            'status': item['status'],
                            'billable_fee': item['billable_fee']
                        }
                        lookup = {"_id": billing_ns_summary_id}
                        (result, _, etag, status) = patch_internal("billing_ns_summary", payload, **lookup)
                        if status != http_utils.HTTP_200_OK:
                            logger.error("Failed to update 'billing_ns_summary' for tenant id={} and month={}"
                                         .format(tenant, month))
                            continue  # or return?

        vnsf_summary = dict()

        # crawl trough current billing ns usage data to populate ns_summary
        (vnsf_usage_data, _, _, status, _) = get_internal('billing_vnsf_usage')
        for item in vnsf_usage_data['_items']:
            logger.debug("Processing vnsf_id={} of month={} belonging to user_id={}"
                         .format(item['vnsf_id'], item['month'], item['user_id']))

            BillingActions._add_item_control_vnsf_summary(vnsf_summary, item)

        logger.debug("Retrieved the following Billing vNSF Summary:\n {}".format(pprint.pformat(vnsf_summary)))

        # cycle through vnsf_summary months and retrieve its billing ns summary to update it
        for user, months in vnsf_summary.items():
            for month, item in vnsf_summary[user].items():

                (vnsf_summary_data, _, _, status, _) = get_internal('billing_vnsf_summary', user_id=user, month=month)

                # if summary for this user->month doesn't exist > create it (post)
                if not status == http_utils.HTTP_200_OK or vnsf_summary_data['_meta']['total'] == 0:
                    logger.debug("Billing vNSF Summary of user_id={} and month={} does not exist. Creating it."
                                 .format(user, month))

                    with current_app.test_request_context():
                        payload = {
                            'user_id': user,
                            'month': month,
                            'number_vnsfs': item['number_vnsfs'],
                            'status': item['status'],
                            'billable_fee': item['billable_fee']
                        }
                        logger.debug("Creating vNSF Summary for user_id={} and month={}".format(user, month))
                        (result, _, etag, status, _) = post_internal("billing_vnsf_summary", payload)
                        if status != http_utils.HTTP_201_CREATED:
                            logger.error("Failed to create 'billing_vnsf_summary' for user_id={} and month={}"
                                         .format(user, month))
                            continue  # or return?

                # if summary for this month exist -> update it (patch)
                else:
                    billing_vnsf_summary_id = vnsf_summary_data['_items'][0]['_id']
                    with current_app.test_request_context():
                        payload = {
                            'number_vnsfs': item['number_vnsfs'],
                            'status': item['status'],
                            'billable_fee': item['billable_fee']
                        }
                        lookup = {"_id": billing_vnsf_summary_id}
                        (result, _, etag, status) = patch_internal("billing_vnsf_summary", payload, **lookup)
                        if status != http_utils.HTTP_200_OK:
                            logger.error("Failed to update 'billing_vnsf_summary' for user_id={} and month={}"
                                         .format(user, month))
                            continue  # or return?


    @staticmethod
    def billing_ns_simulate(request, payload):
        logger = logging.getLogger(__name__)
        logger.debug("Simulating Billing NS")

        allowed_fields = ['ns_id', 'fee']
        if not sorted(list(request.json.keys())) == sorted(allowed_fields):
            logger.error("Specification of fields other than {} is not allowed.".format(allowed_fields))
            abort(make_response(jsonify(**{"_status": "ERR", "_error": {"code": 409, "message":
                  "Specification of fields other than {} is not allowed.".format(allowed_fields)}}), 409))

        # Get expense fee for this ns_id
        ns_id = request.json['ns_id']
        fee = request.json['fee']
        expense_fee = BillingActions._get_billing_ns(ns_id)['expense_fee']

        instance_balance = fee - expense_fee
        running_instances = BillingActions._get_running_ns_instances(ns_id)
        if not running_instances:
            running_instances = list()

        if instance_balance >= 0:
            flatten_min_instances = 1
        else:
            if expense_fee <= 0 or fee <= 0:
                flatten_min_instances = 0
            else:
                flat_ratio = 1 / (fee / expense_fee)
                flatten_min_instances = math.trunc(flat_ratio if flat_ratio % 10 == 0.0 else flat_ratio + 1)

        request.json['instance_balance'] = [1, instance_balance]

        request.json['running_instances'] = [len(running_instances), len(running_instances)*fee]
        request.json['flatten_min_instances'] = [flatten_min_instances, flatten_min_instances*fee]
        request.json['total_balance'] = instance_balance + len(running_instances)*fee + flatten_min_instances*fee

        # Don't actually store this simulation, just return it
        abort(make_response(jsonify(**request.json), 200))

    @staticmethod
    def get_billing_usage(request, lookup):
        logger = logging.getLogger(__name__)
        logger.debug("Getting general billing usage")

        # with current_app.test_request_context():
        #     (ns_usage_data, _, _, status, _) = get_internal('billing_ns_usage')
        # 
        #     if not status == http_utils.HTTP_200_OK or ns_usage_data['_meta']['total'] != 1:
        #         logger.debug("The 'billing_ns_usage' of NS instance id={} for month={} does not exist."
        #                      .format(ns_instance_id, month))
        #         return None
        #
        #     return ns_usage_data['_items'][0]




    @staticmethod
    def get_billing_summary():
        logger = logging.getLogger(__name__)
        logger.debug("Getting general billing summary")
