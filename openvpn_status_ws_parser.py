#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""File that contains OpenvpnStatusWsParser class."""

import time
from datetime import datetime


class OpenvpnStatusWsParser():
    """Class that handles parsing OpenVPN's status log."""
    log_path = None
    log_type = None
    raw_data = None

    def __init__(self, status_log_path):
        self.log_path = status_log_path
        self.fetch_raw_data()
        self.fetch_log_type()

    def fetch_raw_data(self):
        """Fetches raw data from file and assings it to raw_data property."""
        with open(self.log_path, 'r') as file_handle:
            self.raw_data = file_handle.read().strip()

    def fetch_log_type(self):
        """Fetches log type from raw_data and assings evaluated value to log_type property."""
        first_line = self.raw_data.split("\n")[0].strip()

        if first_line == 'OpenVPN CLIENT LIST':
            self.log_type = 'subnet'
        elif first_line == 'OpenVPN STATISTICS':
            self.log_type = 'ptp'

    @staticmethod
    def get_parsed_datetime(raw_value):
        """Returns iso8601 and epoch formatted datetime of specified raw value."""
        datet = datetime.strptime(raw_value, '%a %b %d %H:%M:%S %Y')
        iso = datet.isoformat()
        tstamp = time.mktime(datet.timetuple())

        parsed_date = {
            'iso8601': iso,
            'ts': tstamp
        }

        return parsed_date

    @staticmethod
    def get_timezone():
        """Returns system's timezone."""
        return time.tzname[1]

    @staticmethod
    def get_real_address(raw_value):
        """Returns dict that contains parsed IP address and port."""
        ip_address, port = raw_value.split(':')

        address = {
            'real': {
                'ip': ip_address,
                'port': int(port)
            }
        }

        return address

    @staticmethod
    def get_traffic(byte_stats):
        """Returns dict that contains parsed traffic statistics."""
        traffic = dict()
        traffic['received'] = dict()
        traffic['sent'] = dict()

        for key, value in byte_stats.items():
            group = key.replace('bytes_', '')

            try:
                traffic[group]['bytes'] = int(value)
            except KeyError:
                traffic[group]['bytes'] = None

        return traffic

    def get_updated_at(self):
        """Returns iso8601 and epoch formatted datetime of last log update."""
        second_line = self.raw_data.split("\n")[1].strip()

        if second_line.startswith('Updated,'):
            raw_value = second_line.split(',')[1]
            updated_at = self.get_parsed_datetime(raw_value)
            return updated_at

        return None

    def get_connected_since(self, raw_value):
        """Returns iso0601 and epoch formatted datetime of client's raw Connected Since value."""
        return self.get_parsed_datetime(raw_value)

    def get_clients(self):
        """Finds client rows from raw data and returns dict that contains client information."""
        lines = self.raw_data.split("\n")
        start = lines.index('Common Name,Real Address,Bytes Received,Bytes Sent,Connected Since')
        end = lines.index('ROUTING TABLE')

        headers = ['common_name', 'address', 'bytes_received', 'bytes_sent', 'connected_since']
        clients = dict()
        byte_stats = dict()

        for line in lines[start + 1:end]:
            client_row = line.strip().split(',')
            client = dict()

            for index, header in enumerate(headers):
                if header == 'address':
                    client[header] = self.get_real_address(client_row[index])
                elif header == 'bytes_received' or header == 'bytes_sent':
                    byte_stats[header] = client_row[index]
                elif header == 'connected_since':
                    client[header] = self.get_connected_since(client_row[index])
                else:
                    client[header] = client_row[index]

            if bool(byte_stats):
                client['traffic'] = self.get_traffic(byte_stats)
            else:
                client['traffic'] = None

            clients[client['common_name']] = client
            byte_stats.clear()

        return clients

    def get_clients_connected(self):
        """Returns amount of clients currently connected."""
        return len(self.get_clients())

    @property
    def data(self):
        """Returns final output of parsed data."""
        data = dict()

        if self.log_type == 'subnet':
            data['topology'] = self.log_type
            data['updated_at'] = self.get_updated_at()
            data['timezone'] = self.get_timezone()
            data['clients'] = self.get_clients()
            data['clients_connected'] = self.get_clients_connected()
        elif self.log_type == 'ptp':
            data['topology'] = self.log_type

        return data
