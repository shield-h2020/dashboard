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


Feature: Onboarding
  Validates the vNSF & NS onboarding operations.

  # Background: Ensure the environment is up and running
  #   Given The Recommendations Queue is ready
  #   Given The Recommendations Socket is ready

  @smoke
  Scenario Outline: Onboard vNSFs
    Given The Platform Admin is logged in
    Given The Platform Admin creates a Developers Tenant from <tenant_data>
    Given The Platform Admin creates a Developer from <developer>
#    Given The Developer is logged in
#    When The Developer onboards a <vNSF>
#    Then I expect the response code <status>

    Examples:
      | tenant_data                  | developer            | vNSF                   | status |
      | login/tenant_developers.json | users/developer.json | vnsf/dummy-vnsf.tar.gz | 123    |
