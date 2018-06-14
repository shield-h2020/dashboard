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

import re

from eve.io.mongo import Validator


class NetworkValidator(Validator):
    """
    A simple JSON data validator with a custom data type for IPv4 addresses
    """

    def _validate_type_ipv4address(self, field, value):
        """
        checks that the given value is a valid IPv4 address
        """
        m = re.search("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$", value)
        if not m:
            self._error(field, "Not a valid IPv4 address")
