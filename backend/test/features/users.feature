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


Feature: Users CRUD
  Validates the user management operations.

  @smoke
  Scenario Outline: Create tenants
    Given The Platform Admin is logged in
    When The Platform Admin creates a Tenant from <tenant_data>
    Then I expect the response code <status>

    Examples:
      | tenant_data                    | status |
      | tenants/tenant_uw.json         | 201    |
      | tenants/tenant_a.json          | 201    |
      | tenants/tenant_developers.json | 201    |
      | tenants/tenant_cyberagency.json | 201    |


  @smoke
  Scenario Outline: Create tenant administrators
    Given The Platform Admin is logged in
    Given The Tenant in use is <tenant_data>
    When The Platform Admin creates a Tenant Admin from <tenant_admin>
#    Then Associate add Tenant Admin.... TODO!
    When The Tenant Admin is logged in
    Then I expect the response code <status>

    Examples:
      | tenant_data            | tenant_admin              | status |
      | tenants/tenant_uw.json | users/tenant_admin.json   | 201    |
      | tenants/tenant_a.json  | users/tenant_a_admin.json | 201    |


  @smoke
  Scenario Outline: Create users
    Given The User logs in using <credentials>
    Given The User creates another from <user_data>
    When The New User logs in
    Then I expect the response code <status>

    Examples:
      | credentials                | user_data                | status |
      | login/tenant_uw_admin.json | users/tenant_user.json   | 201    |
      #| login/tenant_uw_admin.json | users/cyberagent.json    | 201    |
      | login/tenant_a_admin.json  | users/tenant_a_user.json | 201    |


  @smoke
  Scenario Outline: Create developers
    Given The Platform Admin is logged in
    Given The Tenant in use is <tenant_data>
    When The Platform Admin creates a Developer from <user>
    When The Developer is logged in
    Then I expect the response code <status>

    Examples:
      | tenant_data                    | user                 | status |
      | tenants/tenant_developers.json | users/developer.json | 201    |

  @smoke
  Scenario Outline: Create cyberagents
    Given The Platform Admin is logged in
    Given The Tenant in use is <tenant_data>
    When The Platform Admin creates a Developer from <user>
    When The Developer is logged in
    Then I expect the response code <status>

    Examples:
      | tenant_data                    | user                 | status |
      | tenants/tenant_cyberagency.json | users/cyberagent.json | 201    |
