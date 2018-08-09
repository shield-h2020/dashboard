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

  @smoke
  Scenario Outline: CSV Attack request
    Given A clean influx <measurement>
    Given I mock the association response with <mock_file>
    When I receive a CSV attack request with <csv_attack_file>
    Then I expect the response code <status>
    Then The CSV attack must be registered <in_datastore>
    Then The CSV data must be registered <in_influx>


    Examples:
      | measurement | mock_file                                         | csv_attack_file              | in_datastore                            | in_influx                            | status |
      | attack      | tenant_ips/tenant-ip-association-csv-success.json | csv_attack/High-DoS-5083.csv | csv_attack/High-DoS-5083-persisted.json | csv_attack/High-DoS-5083-influx.json | 201    |