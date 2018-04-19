#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

def get_address():
    """Returns address from settings file, None upon failure."""
    settings = get_settings_dict()

    try:
        if bool(settings['address']):
            return settings['addresses']
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
    address = get_address()
    
    if not address:
        addresses = get_addresses()
        
        if addresses:
            return addresses
        else:
            return ['0.0.0.0', '::']

    return address

def get_nodes():
    settings_path = get_settings_path()
    nodes = list()
    
    if not settings_path:
        return nodes
    
    with open(settings_path, 'r') as file_handle:
        data = json.load(file_handle)

        for node in data['nodes']:
            nodes.append(int(node['id']))
    
    return nodes

def parse_status_log(status_log_path):
    with open(status_log_path, 'r') as file_handle:
        data = dict()
        data['marker'] = 'data'
        data['content'] = file_handle.read()
        return json.dumps(data)
    return False

def get_status_log_path_for_node(node_id):
    data = get_settings_dict()

    if data and 'nodes' in data:
        nodes = data['nodes']
    else:
        return None

    for node in nodes:
        if int(node['id']) == int(node_id) and node['path']:
            return node['path'].strip()

    return None
