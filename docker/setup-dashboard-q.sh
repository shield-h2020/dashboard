#!/bin/bash

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


# Ensure the message queue server is up and running. Exit if timeout waiting for it.
${CNTR_FOLDER_DEV}/docker/wait-for-it.sh ${MSGQ_HOST}:${MSGQ_PORT} --timeout=10 --strict

pip3 install -r ${CNTR_FOLDER_DEV}/docker/requirements-dashboard-q.txt

# Install SHIELD packages.
cd ${CNTR_FOLDER_DEV}/backend/utils && pip3 install --upgrade .
cd ${CNTR_FOLDER_DEV}/backend/dare && pip3 install --upgrade .



#
# DO NOT REMOVE THIS - LEAVE IT AS THE LAST LINE IN THE FILE.
# Convey the commands from the command line so the container does what it is intended to do once it is up and running.
exec "$@"
