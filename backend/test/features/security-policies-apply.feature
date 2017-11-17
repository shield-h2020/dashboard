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

Feature: Security Policies application
  Validates the operation to convey security recommendations to the vNSF Orchestrator.

  @smoke
  Scenario Outline: Recommendations successful notification
    Given I mock the vNSFO response with <mock_file>
    Given I mock the latest security recommendation <MSPL>
    When I want to apply the latest security recommendation
    Then I expect the response code <status>
    Then I expect the JSON response to be as in <file>

    Examples:
      | mock_file                             | MSPL                |  status | file                                  |
      # HTTP_200_OK
      | mspl/mspl-apply-success.json         | mspl/mspl-apply-success.json         | 200 | mspl/mspl-apply-success.json         |
