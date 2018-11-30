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


from api_endpoints_def import Endpoint


class EndpointHelper(object):

    @staticmethod
    def _get_field(endpoint, field):
        return Endpoint[endpoint.name].value.get(field, None)

    @staticmethod
    def _get_resource(endpoint):
        return Endpoint[endpoint.name].value.get(Endpoint.__RESOURCE__, None)

    @staticmethod
    def _get_item(endpoint):
        return Endpoint[endpoint.name].value.get(Endpoint.__ITEM__, None)

    @staticmethod
    def get_name(endpoint):
        return EndpointHelper._get_field(endpoint, Endpoint.__NAME__)

    @staticmethod
    def get_url(endpoint):
        return EndpointHelper._get_field(endpoint, Endpoint.__URL__)

    @staticmethod
    def get_schema(endpoint):
        return EndpointHelper._get_field(endpoint, Endpoint.__SCHEMA__)

    @staticmethod
    def get_resource_policies(endpoint):
        resource = EndpointHelper._get_resource(endpoint)

        if resource is None:
            return {}

        policies = {}
        for method in resource.keys():
            policies[method] = resource[method][Endpoint.__POLICY__]

        return policies

    @staticmethod
    def get_resource_methods(endpoint):
        resource = EndpointHelper._get_resource(endpoint)

        if resource is None:
            return []

        return list(resource.keys())

    @staticmethod
    def get_item_policies(endpoint):
        item = EndpointHelper._get_item(endpoint)

        if item is None:
            return {}

        policies = {}
        for method in item.keys():
            policies[method] = item[method][Endpoint.__POLICY__]

        return policies

    @staticmethod
    def get_item_methods(endpoint):
        item = EndpointHelper._get_item(endpoint)

        if item is None:
            return []

        return list(item.keys())
