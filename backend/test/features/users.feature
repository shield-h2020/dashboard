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

  # Background: Ensure the environment is up and running
  #   Given The Recommendations Queue is ready
  #   Given The Recommendations Socket is ready

#  @smoke
#  Scenario Outline: Create tenants
#    Given The Platform Admin is logged in
#    Given The Platform Admin creates a Tenant from <tenant_data>
#    Given The Platform Admin creates a Tenant Admin from <tenant_admin>
#    Given The Tenant Admin is logged in
#    Given The Tenant Admin creates a User from <user>
#    Given The Tenant User is logged in
#    When The Tenant User lists the users
#    Then I expect the response code <status>
#    When The Tenant User lists itself
#    Then I expect the response code <statuz>
#    When The Tenant User updates from <user_update>
#    When The Tenant User patches from <user_patch>
##    When The Tenant User deletes itself
##    When The Tenant Admin deletes the User
#
#    Examples:
#      | tenant_data            | tenant_admin              | user                     | status | statuz | user_update                   | user_patch                   |
#      | tenants/tenant_uw.json | users/tenant_admin.json   | users/tenant_user.json   | 500    | 200    | users/tenant_user_update.json | users/tenant_user_patch.json |
#      | tenants/tenant_a.json  | users/tenant_a_admin.json | users/tenant_a_user.json | 500    | 200    | users/tenant_user_update.json | users/tenant_user_patch.json |


  @smoke
  Scenario Outline: Create tenants
    Given The Platform Admin is logged in
    Given The Platform Admin creates a Tenant from <tenant_data>
    Given The Platform Admin creates a Tenant Admin from <tenant_admin>
    Given The Tenant Admin is logged in
    Given The Tenant Admin creates a User from <user>
    Given The Tenant User is logged in
    When The Tenant User lists the users
    Then I expect the response code <status>
    When The Tenant User lists itself
    Then I expect the response code <statuz>

    Examples:
      | tenant_data            | tenant_admin              | user                     | status | statuz |
      | tenants/tenant_uw.json | users/tenant_admin.json   | users/tenant_user.json   | 500    | 200    |
      | tenants/tenant_a.json  | users/tenant_a_admin.json | users/tenant_a_user.json | 500    | 200    |


  @smoke
  Scenario Outline: Create developers
    Given The Platform Admin is logged in
    Given The Platform Admin creates a Tenant from <tenant_data>
    Given The Platform Admin creates a Developer from <user>
    Given The Developer is logged in

    Examples:
      | tenant_data                    | user                 |
      | tenants/tenant_developers.json | users/developer.json |
