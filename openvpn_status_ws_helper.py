#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""File that contains helper functions."""

import os
import json
import re


def validate_config():
    """Checks if configuration file is valid and return boolean based on it."""
    if not get_config_path():
        print("> Configuration file 'config.json' doesn't exist, unable to continue.")
        return False
    return True

def get_node_from_uri(uri):
    """Parses given URI and returns it."""
    node = re.sub(r'\D', '', uri)
    return int(node)

def get_config_path():
    """Returns path of the config file, None upon failure."""
    container = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(container, 'config.json')

    if not os.path.isfile(config_path):
        return None

    return config_path

def get_config_dict():
    """Returns contents of the config file as dict, None upon failure."""
    config_path = get_config_path()

    with open(config_path, 'r') as file_handle:
        data = json.load(file_handle)
        return data

    return None

def get_default_port():
    """Returns value that will be used as default server port."""
    config = get_config_dict()

    try:
        return int(config['port'])
    except KeyError:
        pass

    return 12200

def get_address():
    """Returns address from config file, None upon failure."""
    config = get_config_dict()

    try:
        if bool(config['address']):
            return config['address']
    except KeyError:
        return None

    return None

def get_addresses():
    """Returns list of addresses from config file, None upon failure."""
    config = get_config_dict()

    try:
        return config['addresses']
    except KeyError:
        return None

def get_default_address():
    """Returns value that will be used as default server address."""
    address = get_address()

    if not address:
        addresses = get_addresses()

        if addresses:
            return addresses

        return ['0.0.0.0', '::']

    return address

def get_node_ids():
    """Returns list of ids, it can be empty list."""
    data = get_config_dict()
    nodes = list()

    for node in data['nodes']:
        nodes.append(int(node['id']))

    return nodes

def get_status_log_path_for_node(node_id):
    """Returns path of the status log for node, None upon failure."""
    data = get_config_dict()
    nodes = data['nodes']

    for node in nodes:
        if int(node['id']) == int(node_id):
            return node['path'].strip()

    return None

def get_origins_for_node(node_id):
    """Returns list of origins for node, None upon failure."""
    data = get_config_dict()
    nodes = data['nodes']

    for node in nodes:
        if int(node['id']) == int(node_id):
            try:
                return node['origins']
            except KeyError:
                return None

    return None

def build_open_node_log_string(request, node):
    """Method that builds up string that gets appended to log later."""
    values = list()

    try:
        values.append(request.remote_ip)
    except KeyError:
        values.append('UNKNOWN_IP')

    values.append(node)

    try:
        values.append(request.headers['Origin'])
    except KeyError:
        values.append('UNKNOWN_ORIGIN')

    try:
        values.append(request.headers['User-Agent'])
    except KeyError:
        values.append('UNKNOWN_USER_AGENT')

    return '{NODE} %s - OPEN %s FROM %s - %s' % tuple(values)
