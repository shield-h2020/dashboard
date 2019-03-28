import argparse
import re
from datetime import datetime, timedelta
from random import randint, choice

import pika

ip_valid = re.compile('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')


def validate_ip(_ip):
    """
    Check if a given IP is valid
    :param _ip: IP address to validate
    :return None
    :raise ValueError: When the IP is invalid
    """
    if not re.match(ip_valid, _ip):
        raise ValueError(f'Invalid IP address {_ip}')


def get_comma_separated_list(_list, validator=None):
    """
    Generate an object list based on a comma separated string.
    The function strips any white spaces from the items
    :param _list: String with the list to be transformed
    :param validator: Function to validate any entry on the list
    """

    objs = _list.split(',')
    for obj in objs:
        obj = obj.strip()
        if validator:
            validator(obj)
    return objs


def attack_generator(date, jump, entries, attack_types, severity, ips):
    """
    Attack generator
    :param date: The base date for the entries
    :param jump: Difference between two date entries
    :param entries: Number of entries that will be generated
    :param attack_types:  List with attack types to use
    :param severity: Attack severity
    :param ips: List with attacked ips
    :return: Generator that will yield a new entry for the Database
    """
    index = 0
    while index < entries:
        name_entry = ["0001\t", f"{severity}\t", f"{choice(attack_types)}\t"]
        attack_entries = ['192.168.4.90\t', f'{choice(ips)}\t', '443\t', '50228\t', 'TCP\t']
        date_entry = [f"{datetime.strftime(date, '%Y-%m-%d %H:%M:%S')}\t", f"{date.year}\t", f"{date.month}\t",
                      f"{date.day}\t", f"{date.hour}\t", f"{date.minute}\t", f"{date.second}\t"]
        duration = [f"{randint(1, 180)}\t"]
        pck_entries = [f"{randint(1, 1024)}\t", f"{randint(1, 1024)}\t", "0\t", "0\t", "0.000132496798604"]

        entry = name_entry + date_entry + duration + attack_entries + pck_entries
        yield ''.join(entry)
        index += 1
        date += timedelta(minutes=jump)


def get_args():
    """
    Parse arguments to generate data for InfluxDB
    Based on the user input creates an attack generator
    :return: Generator that will yield each entry for the Database
    """
    parser = argparse.ArgumentParser(
        description='Script to create new InfluxDB entries')

    parser.add_argument(
        '-d', '--date', type=str,
        help='Date string in the format of YYYY-MM-DD, e.g., 2018-08-14',
        required=True)
    parser.add_argument(
        '-e', '--entries', type=int, help='Number of entries to generate. Default 500.', default=500)
    parser.add_argument(
        '-t', '--type', type=str,
        help='String with attack type, multiple attack types can be set separated by comma and'
             ' surrounded by double quotes, e.g.,"DoS, Slowloris". Default DoS.', default='DoS'
    )
    parser.add_argument(
        '-s', '--severity', type=str, help='String with severity type. Default High', default='High',
        choices=['High', 'Medium', 'Low']
    )
    parser.add_argument(
        '-j', '--jump', type=int, help='Time difference between entries in minutes. Default 1 minute', default=1
    )
    parser.add_argument(
        '-i', '--ips', type=str,
        help='Comma separated tenant IPs target of attacks, multiple values can be sent with double quotes, '
             'e.g., "192.168.1.1, 192.168.1.2". Default 10.101.30.60',
        default='10.101.30.60'
    )

    args = parser.parse_args()

    # Convert user input to date object
    date = datetime.strptime(args.date, '%Y-%m-%d')

    # Create list objects based on input
    ips = get_comma_separated_list(args.ips, validate_ip)
    types = get_comma_separated_list(args.type)

    return attack_generator(date, args.jump, args.entries, types, args.severity, ips)


def submit_data(_generator):
    """
    Submit data to RabbitMQ
    :param _generator: Python data generator
    :return:
    """
    _connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=35672))
    channel = _connection.channel()
    channel.exchange_declare(exchange='shield-dashboard-exchange',
                             exchange_type='topic')

    for index, message in enumerate(_generator):
        channel.basic_publish(exchange='shield-dashboard-exchange',
                              routing_key='shield.notifications.attack.qa',
                              body=message)
        print(f"[{index}] Sent: {message}")
    _connection.close()


if __name__ == '__main__':
    generator = get_args()
    submit_data(generator)
