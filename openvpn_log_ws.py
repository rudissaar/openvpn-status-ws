#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
from openvpn_log_parse import parse

class OpenvpnLogWs:
    settings_file = 'settings.json'
    settings_file_path = None
    nodes = list()

    def __init__(self):
        self.get_settings_file_path()
        self.load_nodes()
        self.parse_nodes()

    def get_settings_file_path(self):
        file_path = os.path.dirname(os.path.realpath(__file__))

        if not file_path.endswith('/'):
            file_path += '/'

        file_path += self.settings_file

        if not os.path.isfile(file_path):
            print('> ' + file_path + " doesn't exists, exiting.")
            exit(1)

        self.settings_file_path = file_path

    def load_nodes(self):
        with open(self.settings_file_path, 'r') as file_handle:
            data = json.load(file_handle)

            for node in data['nodes']:
                self.nodes.append(node)

    def parse_nodes(self):
        for node in self.nodes:
            parse(node['path'])
