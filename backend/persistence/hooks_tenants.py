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
from pprint import pformat

import flask
import settings as cfg
from dashboardutils import http_utils
from dashboardutils.error_utils import IssueHandling, IssueElement
from eve.methods.get import get_internal
from keystone_adapter import KeystoneAuthzApi
from werkzeug.exceptions import InternalServerError


class TenantHooks:
    """
    Handles the backstage operations required for the login part of the Dashboard API. These operations are mostly
    targeted at pre and post hooks associated with the API.
    """

    __logger = logging.getLogger(__name__)

    __issue = IssueHandling(__logger)

    __errors = {
        'TENANTS': {
            'SCOPE_GROUPS_ISSUE': {
                IssueElement.ERROR:     ["Can't find groups for scope '{}'. Scope ID: '{}'."],
                IssueElement.EXCEPTION: InternalServerError("Can't find groups for scope.")
                },
            'GROUPS_ISSUE':       {
                IssueElement.ERROR:     ["Can't find group information. Group ID: '{}'."],
                IssueElement.EXCEPTION: InternalServerError("Can't find group information.")
                },
            'GROUP_ROLES_ISSUE':  {
                IssueElement.ERROR:     ["Can't find roles for group. Group ID: '{}'."],
                IssueElement.EXCEPTION: InternalServerError("Can't create roles for group.")
                },
            'ROLE_ISSUE':         {
                IssueElement.ERROR:     ["Can't find the role. Role ID: '{}'."],
                IssueElement.EXCEPTION: InternalServerError("Can't find the role to assign to the group.")
                }
            }
        }

    @staticmethod
    def get_service_admin_authz():
        return KeystoneAuthzApi(protocol=cfg.AAA_PROTOCOL,
                                host=cfg.AAA_HOST,
                                port=cfg.AAA_PORT,
                                username=cfg.AAA_SVC_ADMIN_USER,
                                password=cfg.AAA_SVC_ADMIN_PASS,
                                service_admin=cfg.AAA_SVC_ADMIN_SCOPE)

    @staticmethod
    def create_tenant(items):
        """
        Create a tenant in the platform.

        The tenant creation comprises the creation of the tenant in the AAA system as well as in the API data model,
        the creation of the groups for the tenant (determined by the tenant scope), and the role(s) to assign to the
        group (based on the group definition).

        :param items: the data provided in the request.
        """

        authz = TenantHooks.get_service_admin_authz()
        tenant_data = items[0]

        # Create the tenant in the AAA system.
        created_tenant = authz.create_tenant(tenant_data['tenant_name'], tenant_data['description'])

        TenantHooks.__logger.debug('--tenant_data:\n' + pformat(tenant_data))

        # The tenant scope dictates which groups to create for a tenant.
        # Returns a tuple: (response, last_modified, etag, status, headers)
        (scope_data, _, _, status, _) = get_internal('tenant_scope_groups', scope_id=tenant_data['scope_id'])

        if not status == http_utils.HTTP_200_OK or scope_data['_meta']['total'] == 0:
            TenantHooks.__issue.raise_ex(IssueElement.ERROR, TenantHooks.__errors['TENANTS']['SCOPE_GROUPS_ISSUE'],
                                         [[tenant_data['tenant_name'], tenant_data['scope_id']]])

        TenantHooks.__logger.debug('scope data:\n' + pformat(scope_data))

        group_ids = scope_data['_items'][0]['groups']

        groups = []

        # Create the groups in the AAA system and record the required metadata along with the tenant.
        for group_id in group_ids:

            # Get the groups to create for a tenant.
            (group_data, _, _, status, _) = get_internal('tenant_groups', _id=group_id)

            if not status == http_utils.HTTP_200_OK or group_data['_meta']['total'] == 0:
                TenantHooks.__issue.raise_ex(IssueElement.ERROR, TenantHooks.__errors['TENANTS']['GROUPS_ISSUE'],
                                             [[group_id]])

            TenantHooks.__logger.debug('group data:\n' + pformat(group_data))

            # Find the role(s) associated with the group.
            (roles_data, _, _, status, _) = get_internal('tenant_group_roles', group_id=group_data['_items'][0]['_id'])

            if not status == http_utils.HTTP_200_OK or roles_data['_meta']['total'] == 0:
                TenantHooks.__issue.raise_ex(IssueElement.ERROR, TenantHooks.__errors['TENANTS']['GROUP_ROLES_ISSUE'],
                                             [[group_data['_items'][0]['_id']]])

            TenantHooks.__logger.debug('roles data:\n' + pformat(roles_data))

            roles_id = roles_data['_items'][0]['roles']

            # Create the actual group in the AAA system and assign it the proper role.
            for role_id in roles_id:

                (role, _, _, status, _) = get_internal('tenant_roles', _id=role_id)

                if not status == http_utils.HTTP_200_OK or role['_meta']['total'] == 0:
                    TenantHooks.__issue.raise_ex(IssueElement.ERROR,
                                                 TenantHooks.__errors['TENANTS']['ROLE_ISSUE'],
                                                 [[role_id]])

                TenantHooks.__logger.debug('role data:\n' + pformat(role))

                group = authz.create_group(tenant_id=created_tenant['domain']['id'],
                                           description=group_data['_items'][0]['description'],
                                           code=group_data['_items'][0]['code'], role_id=role['_items'][0]['aaa_id'])

                TenantHooks.__logger.debug('group:\n' + pformat(group))

                groups.append(group)

        # Set data which is only available once the tenant is created in the external authorization system.
        tenant_data['tenant_id'] = created_tenant['domain']['id']
        tenant_data['groups'] = groups

    @staticmethod
    def remove_tenant():
        authz = TenantHooks.get_service_admin_authz()
        authz.remove_tenant(flask.request.view_args['tenant_id'])

    @staticmethod
    def create_tenant_user(items):
        authz = TenantHooks.get_service_admin_authz()
        user_data = items[0]

        # TODO: If more than one "where" lookup there's an error in the URL query parameters.
        lookup = json.loads(flask.request.args.getlist('where')[0])
        print('lookup: ' + pformat(lookup))

        created_user = authz.create_tenant_user(lookup['tenant_id'], user_data)

        # Set data which is only available once the tenant user is created in the external authorization system.
        user_data['tenant_id'] = created_user['user']['tenant_id']
        user_data['user_id'] = created_user['user']['id']

    @staticmethod
    def update_tenant_user(updates, original):
        authz = TenantHooks.get_service_admin_authz()
        user_data = updates

        updated_user = authz.update_tenant_user(updates['tenant_id'], user_data)

        # Set data which is only available once the tenant user is created in the external authorization system.
        user_data['tenant_id'] = updated_user['user']['tenant_id']
        user_data['user_id'] = updated_user['user']['id']

    @staticmethod
    def create_role(items):
        authz = TenantHooks.get_service_admin_authz()

        role_data = items[0]
        print('role data:\n' + pformat(role_data))
        aaa_role = authz.create_role(role_data['code'], role_data['description'])

        # Set data which is only available once the role is created in the external authorization system.
        print('AAA role:\n' + pformat(aaa_role))
        role_data['aaa_id'] = aaa_role['role']['id']
