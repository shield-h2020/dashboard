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

  # TODO: Invalid Username Scenario
  # TODO: Invalid InfluxDB

@smoke
Feature: CSV Attack
  Ensures the CSV attack data is processed and correctly stored

  Background: Ensure the environment is up and running
    Given The Recommendations Queue is ready

  @smoke
  Scenario Outline: Attack message
    Given A clean influx <measurement>
    Given I mock the association response with <mock_file>
    When I receive an attack message with <attack_message>
    Then The attack message must be stored <in_influx>
    Then A clean influx <measurement>

    Examples:
      | measurement | mock_file                                         | attack_message                        | in_influx                              |
      | attack      | tenant_ips/tenant-ip-association-csv-success.json | attack/Slowloris_message.txt          | attack/Slowloris_message.json          |
      | attack      | tenant_ips/tenant-ip-association-csv-success.json | attack/Slowloris_multiple_message.txt | attack/Slowloris_multiple_message.json |
