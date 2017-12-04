#!/bin/sh

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


CURRENT_PATH=${PWD}

TESTS_REPORT_JSON=${FOLDER_TESTS_REPORT}/result.json
TESTS_REPORT_HTML=${FOLDER_TESTS_REPORT}/report.html
REPORT_TOOL=${FOLDER_TESTS_TOOLS}/html_report.js

cd ${FOLDER_TESTS_BASEPATH}

# Run tests.
radish --cucumber-json ${TESTS_REPORT_JSON} ${FOLDER_TESTS_FEATURES}

# Beautify tests report.
node ${REPORT_TOOL} -s ${TESTS_REPORT_JSON} -o ${TESTS_REPORT_HTML}

cd ${CURRENT_PATH}
