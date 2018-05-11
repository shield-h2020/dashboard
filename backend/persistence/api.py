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

import api_docs
import flask
import settings as cfg
from dashboardpersistence.persistence import DashboardPersistence
from dashboardutils import http_utils
from dashboardutils import log
from eve import Eve
from eve.methods.get import get_internal
from eve_swagger import swagger, add_documentation
from flask import current_app
from keystone_adapter import KeystoneAuthzApi
from security import TokenAuthzOslo


def post_login(request, payload):
    logger.debug('login done')
    logger.debug(current_app.auth.get_request_auth_value())

    logger.debug('token')
    logger.debug(flask.g.get('token', 'xpto'))
    payload.headers['Vary'] = 'Shield-Authz-Token'
    payload.set_data(json.dumps(flask.g.get('token', None)))
    flask.g.token = None


def post_user_login(request, payload):
    logger.debug('user login done')
    logger.debug(current_app.auth.get_request_auth_value())

    logger.debug('token')
    logger.debug(flask.g.get('token', 'xpto'))
    payload.headers['Vary'] = 'Shield-Authz-Token'
    payload.set_data(json.dumps(flask.g.get('token', None)))
    flask.g.token = None


# def vnsfs_catalogue(items):
#     for item in items:
#         item['tenant_id'] = flask.request.view_args['tenant_id']


def get_service_admin_authz():
    return KeystoneAuthzApi(protocol=cfg.AAA_PROTOCOL,
                            host=cfg.AAA_HOST,
                            port=cfg.AAA_PORT,
                            username=cfg.AAA_SVC_ADMIN_USER,
                            password=cfg.AAA_SVC_ADMIN_PASS,
                            service_admin=cfg.AAA_SVC_ADMIN_SCOPE)


def create_tenant(items):
    authz = get_service_admin_authz()
    tenant_data = items[0]

    # Create the tenant in the AAA system.
    created_tenant = authz.create_tenant(tenant_data['tenant_name'], tenant_data['description'])

    logger.debug('--tenant_data:\n' + pformat(tenant_data))

    # The tenant scope dictates which groups to create for a tenant.
    # Returns a tuple: (response, last_modified, etag, status, headers)
    (scope_data, _, _, status, _) = get_internal('tenant_scope_groups', scope_id=tenant_data['scope_id'])

    if not status == http_utils.HTTP_200_OK:
        # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['POLICY_ISSUE'],
        #                     [[url, r.status_code]])
        raise FileNotFoundError

    logger.debug('scope data:\n' + pformat(scope_data))

    group_ids = scope_data['_items'][0]['groups']

    groups = []

    # Create the groups in the AAA system and record the required metadata along with the tenant.
    for group_id in group_ids:

        (group_data, _, _, status, _) = get_internal('tenant_groups', _id=group_id)

        if not status == http_utils.HTTP_200_OK:
            # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['POLICY_ISSUE'],
            #                     [[url, r.status_code]])
            raise FileNotFoundError

        logger.debug('group data:\n' + pformat(group_data))

        # Find the role(s) associated with the group.
        (roles_data, _, _, status, _) = get_internal('tenant_group_roles', group_id=group_data['_items'][0]['_id'])

        if not status == http_utils.HTTP_200_OK:
            # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['POLICY_ISSUE'],
            #                     [[url, r.status_code]])
            raise FileNotFoundError

        logger.debug('roles data:\n' + pformat(roles_data))

        roles_id = roles_data['_items'][0]['roles']

        # Create the actual group in the AAA system and assign it the proper role.
        for role_id in roles_id:

            (role, _, _, status, _) = get_internal('tenant_roles', _id=role_id)

            if not status == http_utils.HTTP_200_OK:
                # self.issue.raise_ex(IssueElement.ERROR, self.errors['POLICY']['POLICY_ISSUE'],
                #                     [[url, r.status_code]])
                raise FileNotFoundError

            logger.debug('role data:\n' + pformat(role))

            group = authz.create_group(tenant_id=created_tenant['domain']['id'],
                                       description=group_data['_items'][0]['description'],
                                       code=group_data['_items'][0]['code'], role_id=role['_items'][0]['aaa_id'])

            logger.debug('group:\n' + pformat(group))

            groups.append(group)

    # Set data which is only available once the tenant is created in the external authorization system.
    tenant_data['tenant_id'] = created_tenant['domain']['id']
    tenant_data['groups'] = groups


def remove_tenant():
    authz = get_service_admin_authz()
    authz.remove_tenant(flask.request.view_args['tenant_id'])


def create_tenant_user(items):
    authz = get_service_admin_authz()
    user_data = items[0]

    # TODO: If more than one "where" lookup there's an error in the URL query parameters.
    lookup = json.loads(flask.request.args.getlist('where')[0])
    print('lookup: ' + pformat(lookup))

    created_user = authz.create_tenant_user(lookup['tenant_id'], user_data)

    # Set data which is only available once the tenant user is created in the external authorization system.
    user_data['tenant_id'] = created_user['user']['tenant_id']
    user_data['user_id'] = created_user['user']['id']


def create_role(items):
    authz = get_service_admin_authz()

    role_data = items[0]
    print('role data:\n' + pformat(role_data))
    aaa_role = authz.create_role(role_data['code'], role_data['description'])

    # Set data which is only available once the role is created in the external authorization system.
    print('AAA role:\n' + pformat(aaa_role))
    role_data['aaa_id'] = aaa_role['role']['id']


# def enroll_ns(items):
#     user_data = items[0]
#
#     # TODO: If more than one "where" lookup there's an error in the URL query parameters.
#     lookup = json.loads(flask.request.args.getlist('where')[0])
#     print('lookup: ' + pformat(lookup))
#
#     # Set data which is only available once the tenant user is created in the external authorization system.
#     user_data['tenant_id'] = lookup['tenant_id']


app = Eve(auth=TokenAuthzOslo)

# app.on_insert_vnsfs_catalogue += vnsfs_catalogue

app.on_update_policies += DashboardPersistence.convey_policy
app.on_insert_policies_admin += DashboardPersistence.convert_to_datetime

app.on_post_POST_login += post_login
app.on_post_POST_login_user += post_login

app.on_insert_tenant_roles += create_role

app.on_insert_tenants_catalogue += create_tenant
app.on_delete_resource_tenants_catalogue_delete += remove_tenant

app.on_insert_tenant_users_catalogue += create_tenant_user

# app.on_insert_nss_catalogue += enroll_ns

app.register_blueprint(swagger)

app.config['SWAGGER_INFO'] = api_docs.swagger_info

add_documentation({'paths': api_docs.paths})

if __name__ == '__main__':
    log.setup_logging()
    logger = logging.getLogger(__name__)

    # use '0.0.0.0' to ensure your REST API is reachable from all your
    # network (and not only your computer).
    app.run(host='0.0.0.0', port=cfg.BACKENDAPI_PORT, debug=True)
