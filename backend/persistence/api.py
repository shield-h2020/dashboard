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

import api_docs
import settings as cfg
from dashboardpersistence.persistence import DashboardPersistence
from dashboardutils import log
from eve import Eve
from eve_swagger import swagger, add_documentation
from flask_cors import CORS
from hooks_login import LoginHooks
from hooks_ns_instance_update import NSInstanceHooks
from hooks_nss_inventory import NssInventoryHooks
from hooks_tenants import TenantHooks
from hooks_tm_notifications import TMNotifications
from hooks_tm_attestation import TMAttestation
from hooks_billing import BillingActions
from security import TokenAuthzOslo
from validators import NetworkValidator
from billing.monitor import BillingMonitor
from hooks_policies import PolicyHooks

# Start Billing Update Monitor
# BillingMonitor().start()

app = Eve(auth=TokenAuthzOslo, validator=NetworkValidator)
CORS(app)

app.on_post_POST_ns_instance_update += NSInstanceHooks().post_ns_instance

app.on_update_policies += DashboardPersistence.convey_policy
app.on_insert_policies_admin += DashboardPersistence.convert_to_datetime
app.on_fetched_resource_distinct_policies += PolicyHooks.get_distinct_vnsf_policies

app.on_post_POST_login += LoginHooks.post_login
app.on_post_POST_login_user += LoginHooks.post_login

app.on_insert_tenant_roles += TenantHooks.create_role

app.on_insert_tenants_catalogue += TenantHooks.create_tenant
app.on_delete_resource_tenants_catalogue_delete += TenantHooks.remove_tenant

app.on_insert_tenant_users_catalogue += TenantHooks.create_tenant_user
app.on_replace_tenant_user += TenantHooks.update_tenant_user

app.on_insert_nss_inventory += NssInventoryHooks.provision_network_service

app.on_update_ns_instantiate += NssInventoryHooks.instantiate_network_service
app.on_update_ns_terminate += NssInventoryHooks.terminate_network_service


app.on_update_notifications_tm_vnsf += TMNotifications.apply_vnsf_remediation
app.on_update_notifications_tm_host += TMNotifications.apply_host_remediation

app.on_fetched_resource_distinct_notifications_tm_vnsf += TMNotifications.get_distinct_tm_vnsf_notifications
app.on_fetched_resource_distinct_notifications_tm_host += TMNotifications.get_distinct_tm_notifications

app.on_insert_tm_attest_node += TMAttestation.tm_attest_node
app.on_insert_tm_attest_all += TMAttestation.tm_attest_all

# Billing hooks
app.on_pre_POST_billing_vnsf += BillingActions.create_vnsf_billing_placeholder
app.on_pre_POST_billing_ns += BillingActions.create_ns_billing_placeholder
app.on_update_billing_ns += BillingActions.set_billing_ns_fee
app.on_update_billing_vnsf += BillingActions.set_billing_vnsf_fee
app.on_pre_POST_billing_ns_start_usage += BillingActions.start_billing_ns_usage
app.on_inserted_billing_ns_start_usage += BillingActions.after_start_billing_ns_usage
#app.on_updated_ns_terminate += BillingActions.stop_billing_ns_usage
app.on_fetched_resource_billing_ns_usage += BillingActions.get_billing_ns_usage
app.on_fetched_resource_billing_vnsf_usage += BillingActions.get_billing_vnsf_usage
app.on_fetched_item_billing_ns_usage += BillingActions.get_billing_ns_usage_item
app.on_pre_POST_billing_update += BillingActions.update_billing
app.on_pre_POST_billing_clean += BillingActions.clean_billing
app.on_post_POST_billing_ns_simulate += BillingActions.billing_ns_simulate
#app.on_post_GET_billing_usage += BillingActions.get_billing_usage
# app.on_fetched_resource_billing_summary += BillingActions.get_billing_summary

app.register_blueprint(swagger)

app.config['SWAGGER_INFO'] = api_docs.swagger_info

add_documentation({'paths': api_docs.paths})

if __name__ == '__main__':
    log.setup_logging()
    logger = logging.getLogger(__name__)

    # use '0.0.0.0' to ensure your REST API is reachable from all your
    # network (and not only your computer).
    app.run(host='0.0.0.0', port=cfg.BACKENDAPI_PORT, debug=True, threaded=True)
