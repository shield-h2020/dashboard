import logging

import requests


class SecurityPolicyPersistence:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def persist(self, policy):
        try:
            url = 'http://localhost:3030/admin/policies'

            headers = {'Content-Type': 'application/json'}

            r = requests.post(url, headers=headers, data=policy)

            if len(r.text) > 0:
                self.logger.debug(r.text)

            if not r.status_code == 201:
                self.logger.error('Persistence error for {}. Status: {}'.format(url, r.status_code))
                raise Exception

        except requests.exceptions.ConnectionError:
            self.logger.error('Error persisting the policy at {}'.format(url))
            raise Exception
