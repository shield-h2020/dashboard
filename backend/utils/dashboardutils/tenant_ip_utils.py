import logging

import requests
from dashboardutils import http_utils

logger = logging.getLogger(__name__)


def get_tenant_by_ip(url, ip):
    """
    Associates a given IP address to a tenant interacting with the association service.

    :param url: The URL to collect the association between tenant and IP
    :param ip: The IP to collect the given tenant
    :return: String with the tenant name associated with the IP
    :raise TenantAssociationError when the IP is associated with more then one tenant or none association was found
    """
    logger.debug(f"Associating IP: {ip}")

    # Create the query string to search for the IP
    payload = dict(where=f'{{"ip":"{ip}"}}')
    try:
        r = requests.get(url, params=payload)
        if r.text:
            logger.debug(r.text)
        if not r.status_code == http_utils.HTTP_200_OK:
            raise AssociationCodeError(ip, r.status_code)

        response_data = r.json()
        if response_data['_meta']['total'] != 1:
            raise MultipleAssociation(response_data['_meta']['total'])

        tenant = response_data.get('_items')[0].get('tenant_id', None)
        logger.debug(f"IP {ip} belongs to Tenant {tenant}")
        return tenant

    except requests.exceptions.ConnectionError as e:
        logger.error('Error associating the IP at {}.'.format(url), e)
        raise Exception


class AssociationCodeError(BaseException):
    def __init__(self, ip, status_code):
        super().__init__(f"Association error for {ip}. Status: {status_code}")
        self.status_code = status_code


class MultipleAssociation(BaseException):
    def __init__(self, total_associations):
        super().__init__(f"Invalid association with total results of: {total_associations}")
        self.total_associations = total_associations
