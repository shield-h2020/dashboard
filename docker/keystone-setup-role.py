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

import os

import requests

KEYSTONE_BASE_URL = 'http://{}:{}/v3'.format(os.environ.get("AAA_HOST"), os.environ.get("AAA_ADMIN_PORT"))

AUTH_HEADER = {
    'X-AUTH-TOKEN': ''
}


class ScriptException(BaseException):
    def __init__(self, status_code, text):
        message = "Exception with status code {} and text {}".format(status_code, text)
        super().__init__(message)


def get_admin_id(obj):
    endpoint = '/{}?name=admin'.format(obj)

    r = requests.get(KEYSTONE_BASE_URL + endpoint, headers=AUTH_HEADER)

    if r.status_code < 299:
        data = r.json()
        if data.get(obj):
            return data[obj][0]['id']
    else:
        raise ScriptException(r.status_code, r.text)


def get_auth_token():
    endpoint = '/auth/tokens'

    data = {
        "auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "name": os.environ.get("AAA_SCV_ADMIN_USER"),
                        "domain": {"id": "default"},
                        "password": os.environ.get("AAA_SCV_ADMIN_PASS")
                    }
                }
            },
            "scope": {
                "project": {
                    "name": "admin",
                    "domain": {"id": "default"}
                }
            }
        }
    }
    r = requests.post(KEYSTONE_BASE_URL + endpoint, json=data)

    if r.status_code < 299:
        AUTH_HEADER['X-AUTH-TOKEN'] = r.headers.get('X-Subject-Token')
    else:
        raise ScriptException(r.status_code, r.text)


def update_role(user_id, role_id):
    endpoint = '/domains/default/users/{}/roles/{}'.format(user_id, role_id)
    r = requests.put(KEYSTONE_BASE_URL + endpoint, headers=AUTH_HEADER)

    if r.status_code > 299:
        raise ScriptException(r.status_code, r.text)
    else:
        print('Update role result: {}'.format(r.status_code))


def main():
    get_auth_token()
    user_id = get_admin_id('users')
    role_id = get_admin_id('roles')
    update_role(user_id, role_id)


if __name__ == '__main__':
    main()
