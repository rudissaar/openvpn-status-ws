#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json

def parse_status_log(status_log_path):
    with open(status_log_path, 'r') as file_handle:
        data = dict()
        data['marker'] = 'data'
        data['content'] = file_handle.read()
        return json.dumps(data)
    return False

def get_status_log_path_for_node(node_id):
    container = os.path.dirname(os.path.realpath(__file__))

    if not container.endswith('/'):
        container += '/'
    settings_path = container + 'settings.json'

    if not os.path.isfile(settings_path):
        return False

    with open(settings_path, 'r') as file_handle:
        data = json.load(file_handle)

        if data and 'nodes' in data:
            nodes = data['nodes']
        else:
            return False

        for node in nodes:
            if int(node['id']) == int(node_id) and node['path']:
                return node['path'].strip()

    return False
