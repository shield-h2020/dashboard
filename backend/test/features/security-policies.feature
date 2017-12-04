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

Feature: Security Policies
  Validates the security recommendations notification operation.

  Background: Ensure the environment is up and running
    Given The Recommendations Queue is ready
    Given The Recommendations Socket is ready

  @smoke
  Scenario Outline: Recommendations successful notification
    When I receive a security recommendation <MSPL>
    Then The security recommendation must be persisted <in_datastore>
    Then The security recommendation notification must be received <from_socket>

    Examples:
      | MSPL                             | in_datastore                                | from_socket                                    |
      # Basic MSPL.
      | mspl/ddos-mspl-small.xml         | mspl/ddos-mspl-persisted-small.json         | mspl/ddos-mspl-notification-small.json         |
      # Several vNSFs in one recommendation.
      | mspl/ddos-mspl-multiple-vnsf.xml | mspl/ddos-mspl-persisted-multiple-vnsf.json | mspl/ddos-mspl-notification-multiple-vnsf.json |
      # Rules for 1000 IPs.
      | mspl/ddos-mspl-large.xml         | mspl/ddos-mspl-persisted-large.json         | mspl/ddos-mspl-notification-large.json         |
