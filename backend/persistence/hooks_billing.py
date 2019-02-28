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

import logging
import requests
from flask import current_app

class BillingActions:

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
        print(ns_json)
        expense_fee = 0.0
        for constituent_vnsf_id in ns_json['constituent_vnsfs']:

            #constituent_vnsf_id = BillingActions._get_vnsf_id_from_store(constituent_vnsf_record_id)

            logger.debug("Retrieved constituent vnsf {}".format(constituent_vnsf_id))
            # make and internal request to billing vnsfs to retrieve its fee
            # Returns a tuple: (response, last_modified, etag, status, headers)
            (billing_vnsf_data,  _, _, status, _) = get_internal('billing_vnsf', vnsf_id=constituent_vnsf_id)

            print(billing_vnsf_data)
            logger.debug("Retrieved constituent vnsf {} data: {}".format(constituent_vnsf_id, billing_vnsf_data))

            if not status == http_utils.HTTP_200_OK or billing_vnsf_data['_meta']['total'] == 0:
                abort(make_response(jsonify(**{"_status": "ERR", "_error": {"code": 404, "message":
                      "Failed retrieving billing for constituent vnsf '{}' of ns '{}'"
                                    .format(constituent_vnsf_id, json_data['ns_id'])}}), 404))

            expense_fee += billing_vnsf_data['_items'][0]['fee']

        # fulfill te 'expense_fee'
        json_data['expense_fee'] = expense_fee
        json_data['fee'] = 0.0

        # note: no need to mess with 'additional_fee' as is has a default value of 0.0 in the data model

    @staticmethod
    def set_ns_billing_fee(updates, original):
        """
        Updates the 'fee' of a particular NS Billing.
        Updating other parameters, such as 'expense_fee', 'instance_balance' or 'flatten_min_instances'
         is not allowed as they are calculated automatically.
        """
        logger = logging.getLogger(__name__)

        logger.debug("Setting Billing 'fee' of NS {}".format(original['ns_id']))

        # don't allow updates to fields other than 'fee'
        restricted_fields = ['ns_id', 'expense_fee', 'instance_balance', 'flatten_min_instances']

        for restricted_field in restricted_fields:
            if restricted_field in updates.keys():
                logger.error("Updates to fields other than 'fee' are not allowed.")
                abort(make_response(jsonify(**{"_status": "ERR", "_error": {"code": 409, "message":
                          "Updates to fields other than 'fee' are not allowed."}}), 409))

        if not original['expense_fee']:
            logger.debug("Expense fee of NS {} is not defined".format(updates['ns_id']))
            return

        if updates['fee'] == 0.0:
            updates['instance_balance'] = 0.0
            updates['flatten_min_instances'] = 0.0
            return

        updates['instance_balance'] = updates['fee'] - original['expense_fee']
        if updates['instance_balance'] >= 0:
            updates['flatten_min_instances'] = 1
        else:
            flat_ratio = 1 / (updates['fee'] / original['expense_fee'])
            updates['flatten_min_instances'] = math.trunc(flat_ratio if flat_ratio % 10 == 0.0 else flat_ratio + 1)

    @staticmethod
    def _get_billing_ns_usage(ns_instance_id, month):
        logger = logging.getLogger(__name__)
        logger.debug("Retrieving 'billing_ns_usage' of NS instance id={} for month={}"
                     .format(ns_instance_id, month))

        (ns_usage_data, _, _, status, _) = get_internal('billing_vnsf', ns_instance_id=ns_instance_id, month=month)

        if not status == http_utils.HTTP_200_OK or billing_vnsf_data['_meta']['total'] != 1:
            logger.debug("The 'billing_ns_usage' of NS instance id={} for month={} does not exist."
                         .format(ns_instance_id, month))
            return None

        return ns_usage_data['_items'][0]

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

        print(request.json.keys())

        if not list(request.json.keys()) == allowed_fields:
            logger.error("Specification of fields other than 'ns_instance_id' is not allowed.")
            abort(make_response(jsonify(**{"_status": "ERR", "_error": {"code": 409, "message":
                                        "Specification of fields other than 'ns_instance_id' is not allowed."}}), 409))

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
        fee = BillingActions._get_billing_ns_fee(ns_id)

        current_date = datetime.datetime.now()
        used_from = current_date.date()
        used_to = current_date.date()

        # Assign calculated fields to post request
        request.json['tenant_id'] = tenant_id
        request.json['ns_id'] = ns_id
        request.json['usage_status'] = 'open'
        request.json['instance_status'] = 'running'
        request.json['month'] = current_date.strftime('%Y-%m')
        request.json['used_from'] = used_from.isoformat()
        request.json['used_to'] = used_to.isoformat()
        request.json['fee'] = fee
        request.json['billable_percentage'] = BillingActions._get_ns_usage_billable_percentage(
            used_from, used_to
        )
        request.json['billable_fee'] = BillingActions._get_ns_usage_billable_fee(
            request.json['fee'], request.json['billable_percentage']
        )

    @staticmethod
    def _get_ns_usage_billable_percentage(used_from, used_to):
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
    def _get_ns_usage_billable_fee(monthly_fee, percentage):
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
        updates['instance_status'] = "terminated"
        updates['billable_percentage'] = BillingActions._get_ns_usage_billable_percentage(
            used_from, used_to
        )
        updates['billable_fee'] = BillingActions._get_ns_usage_billable_fee(
            original['fee'], updates['billable_percentage']
        )

    @staticmethod
    def get_billins_ns_usage(response):
        """
        Gets information about a the billing of a NS usage.
        On top of the database data it adds useful information, such as NS instance status
        """
        logger = logging.getLogger(__name__)
        logger.debug("Fetching NS Billing Usages")

        for item in response['_items']:
            item['instance_status'] = BillingActions._get_ns_instance_status(item['ns_instance_id'])

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
    def _get_ns_instance_status(ns_instance_id):
        # retrieve current billing ns usage data
        (nss_inventory_data, _, _, status, _) = get_internal('nss_inventory', instance_id=ns_instance_id)
        if not status == http_utils.HTTP_200_OK or nss_inventory_data['_meta']['total'] == 0:
            abort(make_response(jsonify(**{"_status": "ERR", "_error": {"code": 500, "message":
                                "Failed retrieving status of NS instance '{}'".format(ns_instance_id)}}), 500))

        return nss_inventory_data['_items'][0]['status']

    @staticmethod
    def _get_billing_ns_fee(ns_id):
        logger = logging.getLogger(__name__)
        logger.debug("Retrieving current Billing NS fee for ns id '{}'".format(ns_id))

        # retrieve current billing ns usage data
        (billing_ns_data, _, _, status, _) = get_internal('billing_ns', ns_id=ns_id)
        if not status == http_utils.HTTP_200_OK or billing_ns_data['_meta']['total'] == 0:
            abort(make_response(jsonify(**{"_status": "ERR", "_error": {"code": 500, "message":
                                "Failed retrieving billing for NS '{}'".format(ns_id)}}), 500))

        return billing_ns_data['_items'][0]['fee']


    @staticmethod
    def update_billing(request):
        """
        This hook triggers the update of all top-down billing information, such as
        billing_ns_usage, billing_vnsf_usage, billing_ns_summary and billing_vnsf_summary
        """
        logger = logging.getLogger(__name__)
        logger.info("Updating billing information data")

        # retrieve current billing ns usage data
        (ns_usage_data, _, _, status, _) = get_internal('billing_ns_usage')

        # process NS instances
        for item in ns_usage_data['_items']:
            logger.debug("Processing NS Instance '{}' of NS '{}' belonging to Tenant {}"
                         .format(item['ns_instance_id'], item['ns_id'], item['tenant_id']))

            instance_status = BillingActions._get_ns_instance_status(item['ns_instance_id'])

            if instance_status == 'terminated':
                logger.debug("NS Instance '{}' status is terminated. Skipping.".format(item['ns_instance_id']))
                return

            # get 'used_from' date
            used_from = dateutil.parser.parse(item['used_from']).date()

            # set 'used_to' date
            # a new 'billing_ns_usage' record needs to be created if the month has finished
            # (used_from month is lower than used_to month) and consequently define 'used_to' as the end of the
            # 'used_from' year-month
            current_date = datetime.datetime.now().date()

            if current_date.year > used_from.year or current_date.month > used_from.month:

                (_, year_month_last_day) = calendar.monthrange(used_from.year, used_from.month)
                used_to = datetime.datetime(used_from.year, used_from.month, year_month_last_day).date()
                billable_percentage = BillingActions._get_ns_usage_billable_percentage(used_from, used_to)
                billable_fee = BillingActions._get_ns_usage_billable_fee(item['fee'], billable_percentage)

                # close this 'billing_ns_usage' if isn't already closed
                if item['usage_status'] != 'closed':
                    logger.debug("Closing usage of NS instance={} month={}"
                                 .format(item['ns_instance_id'], item['month']))

                    with current_app.test_request_context():
                        payload = {
                            'used_to': used_to.isoformat(),
                            'billable_percentage': billable_percentage,
                            'billable_fee': billable_fee,
                            'usage_status': 'closed'
                        }
                        lookup = {"_id": item['_id']}
                        (result, _, etag, status) = patch_internal("billing_ns_usage", payload, **lookup)
                        if status != http_utils.HTTP_200_OK:
                            logger.debug("Failed to update 'billing_ns_usage' id '{}'".format(item['_id']))
                            return

                # for each month up to current month, get 'billing_ns_usage' if existent,
                # otherwise create new 'billing_ns_usage' record
                time_delta = relativedelta(used_to, used_from)
                months_delta = time_delta.months + time_delta.years*12 + (1 if time_delta.days else 0)

                print("Dealing with months delta = {}".format(months_delta))
                # TODO: check if this delta is correct!

                for i in range(months_delta):
                    used_from = (datetime.datetime(used_from.year, used_from.month, 1) +
                                 relativedelta(months=1)).date()

                    instance_status = BillingActions._get_ns_instance_status(item['ns_instance_id'])

                    if current_date.year == used_from.year and current_date.month == used_from.month:
                        used_to = current_date
                        usage_status = 'open' if instance_status == 'running' else 'closed'
                    else:
                        (_, year_month_last_day) = calendar.monthrange(used_from.year, used_from.month)
                        used_to = datetime.datetime(used_from.year, used_from.month, year_month_last_day).date()
                        usage_status = 'closed'

                    month = used_from.strftime('%Y-%m')
                    logger.debug("Creating usage of NS instance={}, month={}, used_from={}, used_to={}"
                                 .format(item['ns_instance_id'], month, used_from.isoformat(), used_to.isoformat()))

                    fee = BillingActions._get_billing_ns_fee(item['ns_id'])
                    billable_percentage = BillingActions._get_ns_usage_billable_percentage(used_from, used_to)
                    billable_fee = BillingActions._get_ns_usage_billable_fee(fee, billable_percentage)
                    with current_app.test_request_context():
                        payload = {
                            'ns_instance_id': item['ns_instance_id'],
                            'ns_id': item['ns_id'],
                            'tenant_id': item['tenant_id'],
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
                            logger.debug("Failed to create 'billing_ns_usage' for NS Instance '{}'"
                                         .format(item['ns_instance_id']))
                            return
            else:
                # update 'used_to' date, 'billable_percentage' and 'billable_fee'
                logger.debug("Updating usage of NS instance={} month={}"
                             .format(item['ns_instance_id'], item['month']))

                used_to = current_date
                billable_percentage = BillingActions._get_ns_usage_billable_percentage(used_from, used_to)
                billable_fee = BillingActions._get_ns_usage_billable_fee(item['fee'], billable_percentage)

                (_, year_month_last_day) = calendar.monthrange(used_from.year, used_from.month)
                if current_date.day == year_month_last_day:
                    logger.debug("Last day of the month {}: Closing usage of NS instance={}"
                                 .format(item['month'], item['ns_instance_id']))
                    usage_status = 'closed'
                else:
                    usage_status = 'open'

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
                        logger.debug("Failed to update 'billing_ns_usage' id '{}'".format(item['_id']))
                        return




        print(ns_usage_data)
