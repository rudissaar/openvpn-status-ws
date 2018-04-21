#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""File that contains OpenvpnStatusWsParser class."""


class OpenvpnStatusWsParser():
    log_path = None
    log_type = None
    raw_data = None

    def __init__(self, status_log_path):
        self.log_path = status_log_path
        self.fetch_raw_data()
        self.fetch_log_type()

    def fetch_raw_data(self):
        with open(self.log_path, 'r') as file_handle:
            self.raw_data = file_handle.read().strip()

    def fetch_log_type(self):
        first_line = self.raw_data.split("\n")[0].strip()
        
        if first_line == 'OpenVPN CLIENT LIST':
            self.log_type = 'subnet'
        elif first_line == 'OpenVPN STATISTICS':
            self.log_type = 'ptp'

    def get_clients(self):
        lines = self.raw_data.split("\n")
        start = lines.index('Common Name,Real Address,Bytes Received,Bytes Sent,Connected Since')
        end = lines.index('ROUTING TABLE')

        headers = ['common_name', 'real_address', 'bytes_received', 'bytes_sent', 'connected_since']
        clients = dict()

        for line in lines[start + 1:end]:
            client_row = line.strip().split(',')
            client = dict()

            for index, header in enumerate(headers):
                client[header] = client_row[index]

            clients[client['common_name']] = client
         
        return clients

    def get_clients_connected(self):
        return len(self.get_clients())

    @property
    def data(self):
        data = dict()

        if self.log_type == 'subnet':
            data['topology'] = self.log_type
            data['clients'] = self.get_clients()
            data['clients_connected'] = self.get_clients_connected()
        elif self.log_type == 'ptp':
            data['topology'] = self.log_type

        return data
