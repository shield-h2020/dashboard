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



KEYSTONE_PUBLIC_URL=http://${AAA_HOST}:${AAA_PORT}/v3
KEYSTONE_ADMIN_URL=http://${AAA_HOST}:${AAA_ADMIN_PORT}/v3

export OS_AUTH_URL=${KEYSTONE_ADMIN_URL}
export OS_IDENTITY_API_VERSION=3
export OS_PROJECT_DOMAIN_ID=default
export OS_PROJECT_NAME=admin
export OS_PASSWORD=${AAA_SCV_ADMIN_PASS}
export OS_USERNAME=${AAA_SCV_ADMIN_USER}

CONFIG_FILE=/etc/keystone/keystone.conf
SQL_SCRIPT=/root/keystone.sql

sleep 10
echo "Waiting for mysql"
until mysql -h mysql -u ${AAA_DB_ADMIN_USER} -p${AAA_DB_ADMIN_PASS} &> /dev/null
do
  printf "."
  sleep 10
done
echo -e "\nmysql ready"
mysql -u root -proot -h mysql <$SQL_SCRIPT
rm -f $SQL_SCRIPT

# Populate the Identity service database
mkdir /var/log/keystone/

keystone-manage db_sync
keystone-manage fernet_setup --keystone-user root --keystone-group root
keystone-manage credential_setup --keystone-user root --keystone-group root

mv /etc/keystone/default_catalog.templates /etc/keystone/default_catalog

# start keystone service
uwsgi --http 0.0.0.0:${AAA_ADMIN_PORT} --wsgi-file $(which keystone-wsgi-admin) &

sleep 5 # wait for start

keystone-manage bootstrap --bootstrap-password ${AAA_SCV_ADMIN_PASS} \
  --bootstrap-admin-url ${KEYSTONE_ADMIN_URL} \
  --bootstrap-internal-url ${KEYSTONE_ADMIN_URL} \
  --bootstrap-public-url ${KEYSTONE_PUBLIC_URL} \
  --bootstrap-region-id RegionOne

sleep 5
openstack role add --domain default --user admin admin
sleep 5

mv /etc/keystone/multi_policy.json /etc/keystone/policy.json

# reboot services
pkill uwsgi
sleep 5
uwsgi --http 0.0.0.0:${AAA_PORT} --wsgi-file $(which keystone-wsgi-public) &
sleep 5
uwsgi --http 0.0.0.0:${AAA_ADMIN_PORT} --wsgi-file $(which keystone-wsgi-admin)
