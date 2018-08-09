import asyncio
import copy
import csv
import io
import json
import logging
import os
from datetime import datetime, timezone

import aiohttp
from dashboardutils.error_utils import IssueHandling, IssueElement
from dashboardutils.tenant_ip_utils import get_tenant_by_ip, AssociationCodeError, MultipleAssociation
from settings import INFLUXDB_USER, INFLUXDB_USER_PASSWORD, INFLUXDB_URL, INFLUXDB_BATCH_SIZE, \
    ASSOCIATION_API_URL
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.exceptions import InternalServerError

# TODO: Properly Handle Exception and timeout

# === CSV Attack Config ===
GENERAL_ATTACK = {
    "tags": ['src_ip', 'dst_ip', 's_port', 'd_port', 'protocol'],
    "fields": ['duration', 'in_pkt', 'in_bytes', 'out_pkts', 'out_bytes', 'score'],
    "time_header": 'timereceived',
    "date_format": '%Y-%m-%d %H:%M:%S',
    "measurement": 'attack',
    "delimiter": '\t'
}

DOS_ATTACK = {'name': 'DoS', **GENERAL_ATTACK}
SLOWLORIS_ATTACK = {'name': 'SlowLoris', **GENERAL_ATTACK}

# Note: the attack key must be placed in lower strings
ATTACKS = {
    'dos': DOS_ATTACK,
    'ddos': DOS_ATTACK,
    'slowloris': SLOWLORIS_ATTACK
}


class CyberAttackHooks:
    """
    Class with methods related to LineProtocol conversion.
    LineProtocol is the protocol used to write data in InlfuxDB.

    There are Tags and fields.
    Tags are indexed and assume a form of string
    Fields are not indexed and assume the form of float by default

    The LineProtocol assumes the following form:

    +-----------+--------+-+---------+-+---------+
    |measurement|,tag_set| |field_set| |timestamp|
    +-----------+--------+-+---------+-+---------+

    E.g., measurement tag_1=val,tag_2=val field_1=val,field_2=val 1533126444000000000

    Note: The event loop and asyncio tasks presented in this class are managed according Python 3.6
    """

    __INTERNAL_IP_CACHE__ = {}

    __logger = logging.getLogger(__name__)

    __issue = IssueHandling(__logger)

    __errors = {
        'CYBERATTACKS': {
            'INPUT_FILE_ISSUE': {
                IssueElement.ERROR: ["Can't find File on incoming request."],
                IssueElement.EXCEPTION: InternalServerError("Can't find attack file.")
            },
            'INPUT_FILE_EXTENSION_ISSUE': {
                IssueElement.ERROR: ["Invalid input file extension, missing .csv."],
                IssueElement.EXCEPTION: InternalServerError("Invalid input file extension.")
            },
            'INPUT_FILE_FORMAT_ISSUE': {
                IssueElement.ERROR: ["Invalid input file name <severity>-<attack type>-<id>.csv."],
                IssueElement.EXCEPTION: InternalServerError("Invalid input file name.")
            },
            'INFLUX_CONNECTION_ISSUE': {
                IssueElement.ERROR: ["Can't report cyberattack metrics due to connection problems."],
                IssueElement.EXCEPTION: InternalServerError("Can't report cyberattack metrics.")
            },
            'INFLUX_CONNECTION_TIMEOUT_ISSUE': {
                IssueElement.ERROR: ["Can't report cyberattack metrics due to a connection timeout."],
                IssueElement.EXCEPTION: InternalServerError("Can't report cyberattack metrics.")
            },
            'INFLUX_RESPONSE_ISSUE': {
                IssueElement.ERROR: ["Can't report cyberattack metrics due to a response issue."],
                IssueElement.EXCEPTION: InternalServerError("Can't report cyberattack metrics.")
            },
            'ASSOCIATION_RESPONSE_ISSUE': {
                IssueElement.ERROR: ["Unexpected response code from association."],
                IssueElement.EXCEPTION: InternalServerError("Invalid response from association: {}")
            },
            'MULTIPLE_ASSOCIATION_ISSUE': {
                IssueElement.ERROR: ["The given IP has multiple associations."],
                IssueElement.EXCEPTION: InternalServerError("IP {} has multiple associations: {}")
            }
        }
    }

    @classmethod
    async def async_submit_influx(cls, session, _data):
        """
        Submit a new InfluxDB request asynchronousy.
        :param session: aiohttp session (it is required because the session must be shared)
        :param _data: list with line protocol rows
        """
        async with session.post(
                INFLUXDB_URL, data=b'\n'.join(_row.encode() for _row in _data)) as r:
            cls.__logger.debug("Get Response from influx db")
            if r.status > 299:
                CyberAttackHooks.__issue.raise_ex(IssueElement.ERROR,
                                                  CyberAttackHooks.__errors['CYBERATTACKS'][
                                                      'INFLUX_RESPONSE_ISSUE'])

    @classmethod
    async def async_task_submit(cls, loop, bulk_data):
        """
        Create the tasks to be submitted to InfluxDB and awaits them to finish.
        Manages the aiohttp session to be shared across tasks

        :param loop: Asyncio event loop
        :param bulk_data: Bulk list with lists containing the line protocol rows to be inserted
        """

        auth = aiohttp.BasicAuth(login=INFLUXDB_USER, password=INFLUXDB_USER_PASSWORD)
        async with aiohttp.ClientSession(auth=auth) as session:
            tasks = [cls.async_submit_influx(session, bulk) for bulk in bulk_data]
            await asyncio.gather(*tasks, loop=loop)

    @classmethod
    def parse_csv_file(cls, request):

        def parse_file_name(filename):
            """
            Return list with filename format. Splits the filename from the extension first

            :param filename: string to parse
            :return: SEVERITY, ATTACK_TYPE and CSV_ID
            """
            return os.path.splitext(filename)[0].split('-')

        def parse_tenant():
            """
            Given the destination IP address find the related tenant.
            The association is found by means of a dictionary or by requesting the association IP directly
            """
            ip = row[tag_dict['dst_ip']]

            # search the IP on the Internal Cache
            if ip in cls.__INTERNAL_IP_CACHE__:
                return cls.__INTERNAL_IP_CACHE__[ip]

            try:
                _tenant = get_tenant_by_ip(ASSOCIATION_API_URL, ip)
                cls.__INTERNAL_IP_CACHE__[ip] = _tenant  # Store the association on the dictionary
                return _tenant
            except MultipleAssociation as e:
                CyberAttackHooks.__issue.raise_ex(IssueElement.ERROR,
                                                  CyberAttackHooks.__errors['CYBERATTACKS'][
                                                      'MULTIPLE_ASSOCIATION_ISSUE'],
                                                  [[ip, e.total_associations]])
            except AssociationCodeError as e:
                CyberAttackHooks.__issue.raise_ex(IssueElement.ERROR,
                                                  CyberAttackHooks.__errors['CYBERATTACKS'][
                                                      'ASSOCIATION_RESPONSE_ISSUE'],
                                                  [[ip, e.status_code], [ip, e.status_code]])

        def parse_row():
            """
            Parses current row of the file converting it to Line Protocol

            :return: CSV file row in Line Protocol Format
            """
            field_str = [f"{field}={row[_index]}" for field, _index in field_dict.items()]
            field_str.append(f"csv_id={csv_id}")

            tag_str = [f"{field}={row[_index]}" for field, _index in tag_dict.items()]
            tag_str.append(f'severity={severity}')
            tag_str.append(f'attack_type={attack_config.get("name", attack.lower())}')
            tag_str.append(f'tenant={tenant}')

            new_date = datetime.strptime(row[time_field], attack_config['date_format'])
            timestamp = int(new_date.replace(tzinfo=timezone.utc).timestamp())  # Return POSIX UTC timestamp
            timestamp = timestamp * 1000 * 1000 * 1000  # ms us ns

            line_protocol = f"{attack_config['measurement']},{','.join(tag_str)} {','.join(field_str)} {timestamp}"
            return line_protocol

        # Collect file from request
        # Note: From the performed tests the file is mandatory so no validation is required
        file = request.files['file']

        # File Validations
        if not file.filename.endswith('.csv'):
            CyberAttackHooks.__issue.raise_ex(IssueElement.ERROR,
                                              CyberAttackHooks.__errors['CYBERATTACKS']['INPUT_FILE_EXTENSION_ISSUE'])
        if file.filename.count('-') != 2:
            CyberAttackHooks.__issue.raise_ex(IssueElement.ERROR,
                                              CyberAttackHooks.__errors['CYBERATTACKS']['INPUT_FILE_FORMAT_ISSUE'])

        cls.__logger.info(f"Parsing attack CSV {file.filename}")

        # Parse filename
        severity, attack, csv_id = parse_file_name(file.filename)

        # Check attack type by name
        attack_config = ATTACKS.get(attack.lower(), GENERAL_ATTACK)

        # Convert to stream
        with io.StringIO(file.stream.read().decode('UTF-8'), newline=None) as stream:
            csv_reader = csv.reader(stream, delimiter=attack_config['delimiter'])
            header = next(csv_reader)

            tag_dict = {}
            field_dict = {}
            time_field = -1

            # Parse header Tags and Field indexes to fasten search
            for index, head in enumerate(header[0].split(',')):
                head = head.strip()
                if head in attack_config['tags']:
                    tag_dict[head] = index
                elif head in attack_config['fields']:
                    field_dict[head] = index
                elif head == attack_config['time_header']:
                    time_field = index

            bulk_data = []
            data = []
            # Convert to line protocol
            for row in csv_reader:
                tenant = parse_tenant()
                data.append(parse_row())
                # Submit partial data once the list gets to large
                if len(data) > INFLUXDB_BATCH_SIZE:
                    bulk_data.append(copy.deepcopy(data))
                    data.clear()
            bulk_data.append(data)

        # Sets the event loop to be used
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            # When no event loop exists an exception is raised
            # and a loop is set
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        cls.__logger.info("Start requesting influxDB")
        loop.run_until_complete(cls.async_task_submit(loop, bulk_data))
        loop.close()

        form_data = request.form.copy()
        form_data['filename'] = file.filename
        request.form = ImmutableMultiDict(form_data)
        cls.__logger.info(f"Parsed attack CSV {file.filename}")

    @classmethod
    def post_parse_csv_file(cls, request, response):
        # TODO: Send message to RMQ with the ID
        data = json.loads(response.get_data())
        print(data["_id"])

    @classmethod
    def clean_response_data(cls, request, response):
        """
        Removes the empty file field from the response

        :return: Response without the file field
        """

        # Note: the JSON load and dump is used because the response data is type bytes
        data = json.loads(response.get_data())
        if '_items' in data:
            for item in data['_items']:
                if not item['file']:
                    del item['file']
        response.set_data(json.dumps(data))
