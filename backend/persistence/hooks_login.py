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

import flask
from flask import current_app


class LoginHooks:
    """
    Handles the backstage operations required for the tenants part of the Dashboard API. These operations are mostly
    targeted at pre and post hooks associated with the API.
    """

    __logger = logging.getLogger(__name__)

    @staticmethod
    def post_login(request, payload):
        LoginHooks.__logger.debug('login done')
        LoginHooks.__logger.debug(current_app.auth.get_request_auth_value())

        LoginHooks.__logger.debug('token')
        LoginHooks.__logger.debug(flask.g.get('token', 'xpto'))
        payload.headers['Vary'] = 'Shield-Authz-Token'
        payload.set_data(json.dumps(flask.g.get('token', None)))
        flask.g.token = None

    @staticmethod
    def post_user_login(request, payload):
        LoginHooks.__logger.debug('user login done')
        LoginHooks.__logger.debug(current_app.auth.get_request_auth_value())

        LoginHooks.__logger.debug('token')
        LoginHooks.__logger.debug(flask.g.get('token', 'xpto'))
        payload.headers['Vary'] = 'Shield-Authz-Token'
        payload.set_data(json.dumps(flask.g.get('token', None)))
        flask.g.token = None
