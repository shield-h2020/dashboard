//  Copyright (c) 2017 SHIELD, UBIWHERE
// ALL RIGHTS RESERVED.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// Neither the name of the SHIELD, UBIWHERE nor the names of its
// contributors may be used to endorse or promote products derived from this
// software without specific prior written permission.
//
// This work has been performed in the framework of the SHIELD project,
// funded by the European Commission under Grant number 700199 through the
// Horizon 2020 program. The authors would like to acknowledge the contributions
// of their colleagues of the SHIELD partner consortium (www.shield-h2020.eu).


// Connect to the database.
conn = new Mongo('127.0.0.1:' + PORT);
db = conn.getDB(STORE_COLLECTION);

db.login.deleteMany({})

db.tenants_catalogue.deleteMany({})
db.tenant_users_catalogue.deleteMany({})

db.tenant_ips.deleteMany({})

db.tenant_scopes.deleteMany({})
db.tenant_groups.deleteMany({})
db.tenant_roles.deleteMany({})
db.tenant_scope_groups.deleteMany({})
db.tenant_group_roles.deleteMany({})

db.nss_catalogue.deleteMany({})
db.vnsfs_catalogue.deleteMany({})

db.nss_inventory.deleteMany({})

db.validations.deleteMany({})

db.policies.deleteMany({})
db.notifications.deleteMany({})

db.policies.insert( { tenant_id: "tbd", detection: "2018-03-04T11:23:48", "attack": "DoS",
"recommendation": "<mspl-set xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns=\"http://security.polito.it/shield/mspl\">\n  <context>\n    <severity>3</severity>\n    <type>DoS</type>\n    <timestamp>2017-10-17T13:32:00</timestamp>\n  </context>\n  <it-resource id=\"vNSF-filtering\">\n    <configuration xsi:type=\"filtering-configuration\">\n      <default-action>accept</default-action>\n      <resolution-strategy>FMR</resolution-strategy>\n      <rule>\n        <priority>1</priority>\n        <action>drop</action>\n        <condition>\n          <packet-filter-condition>\n            <direction>inbound</direction>\n            <source-address>100.114.244.222</source-address>\n            <source-port>*</source-port>\n            <destination-address>10.101.20.230</destination-address>\n            <destination-port>80</destination-port>\n            <protocol>TCP</protocol>\n          </packet-filter-condition>\n        </condition>\n      </rule>\n    </configuration>\n  </it-resource>\n</mspl-set>\n",
"severity": 3,
"status": "Not applied" } )

db.policies.insert( { tenant_id: "tbd",
"detection": "2017-12-13T13:32:00",
"attack": "DoS",
"recommendation": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<mspl-set xmlns=\"http://security.polito.it/shield/mspl\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://security.polito.it/shield/mspl mspl.xsd \">\n\n\t<!-- TCP SYN flood (high severity) - drop the packets -->\n\n\t<context>\n\t\t <severity>3</severity>\n\t\t <type>DoS</type>\n\t\t <timestamp>2017-10-17T13:32:00</timestamp>\n\t</context>\n\n\t<it-resource id=\"vNSF1\">\n\t\t<configuration xsi:type=\"filtering-configuration\">\n\t\t\t<default-action>accept</default-action>\n\t\t\t<resolution-strategy>FMR</resolution-strategy>\n\t\t\t<rule> <!-- for each DARE attacker/attack target pairs -->\n\t\t\t\t<priority>1</priority>\n\t\t\t\t<action>drop</action>\n\t\t\t\t<condition>\n\t\t\t\t\t<packet-filter-condition>\n\t\t\t\t\t\t<direction>inbound</direction>\n\t\t\t\t\t\t<!--  <source-address></source-address> --> <!-- insert DARE attacker IP here -->\n\t\t\t\t\t\t<!--  <source-port></source-port> --> <!-- insert DARE attacker ports here (if any) -->\n\t\t\t\t\t\t<!--  <destination-address></destination-address> --> <!-- insert DARE attack target IP here -->\n\t\t\t\t\t\t<!--  <destination-port></destination-port> --> <!-- insert DARE attack target port here (if any) -->\n\t\t\t\t\t\t<protocol>TCP</protocol>\n\t\t\t\t\t</packet-filter-condition>\n\t\t\t\t</condition>\n\t\t\t</rule>\n\t\t</configuration>\n\t</it-resource>\n\n\t<!-- TCP SYN flood (low severity) - limit the packets -->\n\n\t<it-resource id=\"vNSF2\">\n\t\t<configuration xsi:type=\"filtering-configuration\">\n\t\t\t<default-action>drop</default-action>\n\t\t\t<resolution-strategy>FMR</resolution-strategy>\n\t\t\t<rule>\n\t\t\t\t<priority>1</priority>\n\t\t\t\t<action>accept</action>\n\t\t\t\t<condition>\n\t\t\t\t\t<packet-filter-condition>\n\t\t\t\t\t\t<direction>inbound</direction>\n\t\t\t\t\t\t<protocol>TCP</protocol>\n\t\t\t\t\t</packet-filter-condition>\n\t\t\t\t\t<traffic-flow-condition>\n\t\t\t\t\t\t<max-connections>10</max-connections>\n\t\t\t\t\t</traffic-flow-condition>\n\t\t\t\t</condition>\n\t\t\t</rule>\n\t\t\t<rule> <!-- for each DARE attacker/attack target pairs -->\n\t\t\t\t<priority>2</priority>\n\t\t\t\t<action>accept</action>\n\t\t\t\t<condition>\n\t\t\t\t\t<packet-filter-condition>\n\t\t\t\t\t\t<direction>inbound</direction>\n\t\t\t\t\t\t<!-- <source-address></source-address> --> <!-- insert DARE attacker IP here -->\n\t\t\t\t\t\t<!-- <source-port></source-port> --> <!-- insert DARE attacker ports here (if any) -->\n\t\t\t\t\t\t<!-- <destination-address></destination-address> --> <!-- insert DARE attack target IP here -->\n\t\t\t\t\t\t<!-- <destination-port></destination-port> --> <!-- insert DARE attack target port here (if any) -->\n\t\t\t\t\t\t<protocol>TCP</protocol>\n\t\t\t\t\t</packet-filter-condition>\n\t\t\t\t\t<traffic-flow-condition>\n\t\t\t\t\t\t<rate-limit>100/s</rate-limit>\n\t\t\t\t\t</traffic-flow-condition>\n\t\t\t\t</condition>\n\t\t\t</rule>\n\t\t</configuration>\n\t</it-resource>\n\n\t<!-- UDP flood (high severity) - drop the datagrams -->\n\n\t<it-resource id=\"vNSF3\">\n\t\t<configuration xsi:type=\"filtering-configuration\">\n\t\t\t<default-action>accept</default-action>\n\t\t\t<resolution-strategy>FMR</resolution-strategy>\n\t\t\t<rule> <!-- for each DARE attacker/attack target pairs -->\n\t\t\t\t<priority>1</priority>\n\t\t\t\t<action>drop</action>\n\t\t\t\t<condition>\n\t\t\t\t\t<packet-filter-condition>\n\t\t\t\t\t\t<direction>inbound</direction>\n\t\t\t\t\t\t<!-- <source-address></source-address> --> <!-- insert DARE attacker IP here -->\n\t\t\t\t\t\t<!-- <source-port></source-port> --> <!-- insert DARE attacker ports here (if any) -->\n\t\t\t\t\t\t<!-- <destination-address></destination-address>  --> <!-- insert DARE attack target IP here -->\n\t\t\t\t\t\t<!-- <destination-port></destination-port> --> <!-- insert DARE attack target port here (if any) -->\n\t\t\t\t\t\t<protocol>UDP</protocol>\n\t\t\t\t\t</packet-filter-condition>\n\t\t\t\t</condition>\n\t\t\t</rule>\n\t\t</configuration>\n\t</it-resource>\n\n\t<!-- UDP flood (low severity)  - limit the datagrams -->\n\n\t<it-resource id=\"vNSF4\">\n\t\t<configuration xsi:type=\"filtering-configuration\">\n\t\t\t<default-action>drop</default-action>\n\t\t\t<resolution-strategy>FMR</resolution-strategy>\n\t\t\t<rule> <!-- for each DARE attacker/attack target pairs -->\n\t\t\t\t<priority>1</priority>\n\t\t\t\t<action>accept</action>\n\t\t\t\t<condition>\n\t\t\t\t\t<packet-filter-condition>\n\t\t\t\t\t\t<direction>inbound</direction>\n\t\t\t\t\t\t<!-- <source-address></source-address> --> <!-- insert DARE attacker IP here -->\n\t\t\t\t\t\t<!-- <source-port></source-port>  --> <!-- insert DARE attacker ports here (if any) -->\n\t\t\t\t\t\t<!-- <destination-address></destination-address>  --> <!-- insert DARE attack target IP here -->\n\t\t\t\t\t\t<!-- <destination-port></destination-port>  --> <!-- insert DARE attack target port here (if any) -->\n\t\t\t\t\t\t<protocol>UDP</protocol>\n\t\t\t\t\t</packet-filter-condition>\n\t\t\t\t\t<traffic-flow-condition>\n\t\t\t\t\t\t<rate-limit>100/s</rate-limit>\n\t\t\t\t\t</traffic-flow-condition>\n\t\t\t\t</condition>\n\t\t\t</rule>\n\t\t</configuration>\n\t</it-resource>\n\n</mspl-set>\n",
"severity": 3,
"status": "Not applied" } )
