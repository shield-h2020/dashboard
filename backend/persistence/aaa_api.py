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

from abc import ABCMeta, abstractmethod
from dashboardutils import http_utils


class AaaApi(metaclass=ABCMeta):

    def __init__(self, protocol, host, port, username, password, service_admin, logger=None):
        self.logger = logger or logging.getLogger(__name__)

        self.api_basepath = http_utils.build_url(server=host, port=port, basepath='v3', protocol=protocol)

        self.username = username
        self.password = password
        self.service_admin = service_admin

    @property
    def login(self):
        raise NotImplementedError

    @property
    def tenants(self):
        raise NotImplementedError

    @property
    def tenant_query(self):
        raise NotImplementedError

    @property
    def for_tenant(self):
        raise NotImplementedError

    @property
    def groups(self):
        raise NotImplementedError

    @property
    def for_group(self):
        raise NotImplementedError

    @property
    def roles(self):
        raise NotImplementedError

    @property
    def for_role(self):
        raise NotImplementedError

    @property
    def for_group_role(self):
        raise NotImplementedError

    @property
    def users(self):
        raise NotImplementedError

    @property
    def for_group_user(self):
        raise NotImplementedError

    @abstractmethod
    def create_group(self, tenant_id, description, code, role_id):
        raise NotImplementedError

    @abstractmethod
    def create_role(self, role_code, description):
        raise NotImplementedError

    @abstractmethod
    def create_tenant(self, tenant, description):
        raise NotImplementedError

    @abstractmethod
    def remove_tenant(self, tenant):
        raise NotImplementedError

    @abstractmethod
    def get_tenant(self, tenant):
        raise NotImplementedError

    @abstractmethod
    def set_tenant_status(self, tenant_id, enabled):
        raise NotImplementedError

    @abstractmethod
    def create_tenant_user(self, tenant_id, user_data):
        raise NotImplementedError
