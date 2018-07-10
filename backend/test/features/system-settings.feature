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


Feature: Setup the platform
  Creates all the necessary configurations for the platform to be up and running.


  @smoke
  Scenario Outline: Create scopes
    Given The Platform Admin is logged in
    Given The Platform Admin creates a tenant scope from <scope>
    Then I expect the response code <status>

    Examples:
      | scope                               | status |
      | definitions/scope_tenant.json       | 201    |
      | definitions/scope_tenant_admin.json | 201    |
      | definitions/scope_tenant_user.json  | 201    |
      | definitions/scope_developer.json    | 201    |
      | definitions/scope_cyber-agent.json  | 201    |


  @smoke
  Scenario Outline: Create groups
    Given The Platform Admin is logged in
    Given The Platform Admin creates a tenant group from <group>
    Then I expect the response code <status>

    Examples:
      | group                                | status |
      | definitions/group_tenant_admins.json | 201    |
      | definitions/group_tenant_users.json  | 201    |
      | definitions/group_developers.json    | 201    |
      | definitions/group_cyber-agents.json  | 201    |


  @smoke
  Scenario Outline: Create roles
    Given The Platform Admin is logged in
    Given The Platform Admin creates a tenant role from <role>
    Then I expect the response code <status>

    Examples:
      | role                               | status |
      | definitions/role_tenant_admin.json | 201    |
      | definitions/role_tenant_user.json  | 201    |
      | definitions/role_developer.json    | 201    |
      | definitions/role_cyber-agent.json  | 201    |


  @smoke
  Scenario Outline: Associate groups with scopes
    Given The Platform Admin is logged in
    Given The Platform Admin associates groups to a scope from <file>
    Then I expect the response code <status>

    Examples:
      | file                                       | status |
      | definitions/scope_groups_tenant.json       | 201    |
      | definitions/scope_groups_tenant_admin.json | 201    |
      | definitions/scope_groups_tenant_user.json  | 201    |
      | definitions/scope_groups_developer.json    | 201    |
      | definitions/scope_groups_cyber-agent.json  | 201    |


  @smoke
  Scenario Outline: Associate roles with groups
    Given The Platform Admin is logged in
    Given The Platform Admin associates roles to a group from <file>
    Then I expect the response code <status>

    Examples:
      | file                                      | status |
      | definitions/group_roles_tenant_admin.json | 201    |
      | definitions/group_roles_tenant_user.json  | 201    |
      | definitions/group_roles_developer.json    | 201    |
      | definitions/group_roles_cyber-agent.json  | 201    |
