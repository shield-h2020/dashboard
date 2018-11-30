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


Feature: NSs Inventory
  Validates the NSs inventory management operations.

  # Background: Ensure the environment is up and running
  #   Given The Recommendations Queue is ready
  #   Given The Recommendations Socket is ready

  @smoke
  Scenario Outline: Enroll Network Service successfully
    Given The Platform Admin is logged in
    When The Platform Admin enrolls a NS from <file>
    Then I expect the response code <status>

    Examples:
      | file                        | status |
      | nss/ns_enroll_idps.json     | 201    |
      | nss/ns_enroll_tunnel.json   | 201    |
      | nss/ns_enroll_firewall.json | 201    |


  @smoke
  Scenario Outline: Not authorized to enroll a Network Service
    Given The User logs in with <credentials>
    When The User enrolls a NS from <file>
    Then I expect the response code <status>

    Examples:
      | credentials                | file                        | status |
      | login/tenant_uw_admin.json | nss/ns_enroll_idps.json     | 403    |
      | login/tenant_a_admin.json  | nss/ns_enroll_firewall.json | 403    |
      | login/tenant_uw_user.json  | nss/ns_enroll_idps.json     | 403    |

  @smoke
  Scenario Outline: Enroll vNSF successfully
    Given The Platform Admin is logged in
    When The Platform Admin enrolls a vNSF from <file>
    Then I expect the response code <status>

    Examples:
      | file                            | status |
      | vnsfs/vnsf_enroll_dpi.json      | 201    |
      | vnsfs/vnsf_enroll_ids.json      | 201    |
      | vnsfs/vnsf_enroll_l3filter.json | 201    |
      | vnsfs/vnsf_enroll_vpn.json      | 201    |


  @smoke
  Scenario Outline: Not authorized to enroll a vNSF
    Given The User logs in with <credentials>
    When The User enrolls a vNSF from <file>
    Then I expect the response code <status>

    Examples:
      | credentials                | file                            | status |
      | login/tenant_uw_admin.json | vnsfs/vnsf_enroll_dpi.json      | 403    |
      | login/tenant_uw_admin.json | vnsfs/vnsf_enroll_ids.json      | 403    |
      | login/tenant_uw_admin.json | vnsfs/vnsf_enroll_vpn.json      | 403    |
      | login/tenant_a_admin.json  | vnsfs/vnsf_enroll_l3filter.json | 403    |


  @smoke
  Scenario Outline: Network Service successful provisioning
    Given The Platform Admin is logged in
    Given The User logs in with <credentials>
    When The User provisions a NS from <file>
    Then I expect the response code <status>

    Examples:
      | credentials                | file                           | status |
      | login/tenant_uw_admin.json | nss/ns_provision_idps.json     | 201    |
      | login/tenant_uw_admin.json | nss/ns_provision_firewall.json | 201    |
      | login/tenant_a_admin.json  | nss/ns_provision_tunnel.json   | 201    |

