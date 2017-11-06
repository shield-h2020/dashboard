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


import datetime
import logging
from pprint import pprint

from eve import Eve

import settings as cfg
from dashboardutils import log
from vnsfo.vnsfo import VnsfOrchestratorAdapter, VnsfOrchestratorPolicyIssue


def validate_policy(updates, original):
    """
    Sends the security policy to the vNSFO.

    :param updates: The data updated
    :param original: The original data
    """

    policy = dict(original)
    for key, value in updates.items():
        policy[key] = value

    logger.info('updated policy: \n%s', pprint(policy))
    print('updated policy: \n%s', pprint(policy))

    try:
        vnsfo = VnsfOrchestratorAdapter(cfg.VNSFO_PROTOCOL, cfg.VNSFO_HOST, cfg.VNSFO_PORT, cfg.VNSFO_API)
        vnsfo.apply_policy(cfg.VNSFO_TENANT_ID, policy)
    except VnsfOrchestratorPolicyIssue:
        logger.error('VnsfOrchestratorPolicyIssue')


def convey_policy(updates, original):
    """
    Sends the security policy to the vNSFO.

    :param updates: The data updated
    :param original: The original data
    """

    policy = dict(original)
    for key, value in updates.items():
        policy[key] = value

    logger.info('updated policy: \n%s', pprint(policy))
    print('updated policy: \n%s', pprint(policy))

    try:
        vnsfo = VnsfOrchestratorAdapter(cfg.VNSFO_PROTOCOL, cfg.VNSFO_HOST, cfg.VNSFO_PORT, cfg.VNSFO_API)
        vnsfo.apply_policy(cfg.VNSFO_TENANT_ID, policy)
    except VnsfOrchestratorPolicyIssue:
        logger.error('VnsfOrchestratorPolicyIssue')


def insert_convert_to_datetime(items):
    """
    The fields to be stored as datetime must be converted from string as it was JSON serialized.

    :param items: The json to store.
    """
    for item in items:
        item['detection'] = datetime.datetime.strptime(item['detection'], cfg.DATETIME_FIELDS_INPUT_FMT)


app = Eve()

app.on_update_policies += validate_policy
app.on_insert_policies_admin += insert_convert_to_datetime

if __name__ == '__main__':
    log.setup_logging()
    logger = logging.getLogger(__name__)

    # use '0.0.0.0' to ensure your REST API is reachable from all your
    # network (and not only your computer).
    app.run(host='0.0.0.0', port=cfg.BACKENDAPI_PORT, debug=True)
