#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""File that contains helper functions."""

import os
import json

def get_settings_path():
    """Returns path of the settings file, None upon failure."""
    container = os.path.dirname(os.path.realpath(__file__))

    if not container.endswith('/'):
        container += '/'
    settings_path = container + 'settings.json'

    if not os.path.isfile(settings_path):
        return None

    return settings_path

def get_settings_dict():
    """Returns contents of the settings file as dict, None upon failure."""
    settings_path = get_settings_path()

    with open(settings_path, 'r') as file_handle:
        data = json.load(file_handle)
        return data

    return None

def get_default_port():
    """Returns value that will be used as default server port."""
    settings = get_settings_dict()

    try:
        return int(settings['port'])
    except KeyError:
        pass

    return 12200

def get_address():
    """Returns address from settings file, None upon failure."""
    settings = get_settings_dict()

    try:
        if bool(settings['address']):
            return settings['address']
    except KeyError:
        return None

    return None

def get_addresses():
    """Returns list of addresses from settings file, None upon failure."""
    settings = get_settings_dict()

    try:
        return settings['addresses']
    except KeyError:
        return None

def get_default_address():
    """Returns value that will be used as default server address."""
    address = get_address()

    if not address:
        addresses = get_addresses()

        if addresses:
            return addresses
        else:
            return ['0.0.0.0', '::']

    return address

def get_node_ids():
    """Returns list of ids, it can be empty list."""
    data = get_settings_dict()
    nodes = list()

    for node in data['nodes']:
        nodes.append(int(node['id']))

    return nodes

def get_status_log_path_for_node(node_id):
    """Returns path of the status log for node, None upon failure."""
    data = get_settings_dict()
    nodes = data['nodes']

    for node in nodes:
        if int(node['id']) == int(node_id):
            return node['path'].strip()

def parse_status_log(status_log_path):
    """Parses OpenVPN's status log and returns it in json format, None upon failure."""
    with open(status_log_path, 'r') as file_handle:
        raw_data = file_handle.read()

        data = dict()
        data['raw_data'] = raw_data

        return json.dumps(data)

    return None
