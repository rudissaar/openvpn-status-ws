#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
from tornado.websocket import WebSocketHandler, WebSocketClosedError
from openvpn_status_ws_helper import get_status_log_path_for_node, parse_status_log


class OpenvpnStatusWsHandler(WebSocketHandler):
    options = dict()
    options['node'] = None
    options['status_log_path'] = None
    options['timestamp'] = None

    def check_origin(self, origin):
        return True

    def open(self, node):
        self.node = node
        self.status_log_path = get_status_log_path_for_node(self.node)

        if self.status_log_path is None:
            self.close()

        try:
            self.application.peers[self.node].append(self)
        except KeyError:
            self.application.peers[self.node] = list()

    def on_message(self, message):
        if message.strip() == 'ping':
            data = json.dumps({'marker': 'ping'})
            self.write_message(data)
        elif message.strip() == 'fetch':
            self.send()

    def on_close(self):
        self.application.peers[self.node].remove(self)

    def send(self):
        print('Sending');
        mtime = os.stat(self.status_log_path).st_mtime

        if mtime != self.timestamp:
            self.timestamp = mtime
            data = parse_status_log(self.status_log_path)
            self.write_message(data)

    @property
    def node(self):
        return self.options['node']

    @node.setter
    def node(self, value):
        if isinstance(value, str) and value.isnumeric():
            self.options['node'] = int(value)
        elif isinstance(value, int):
            self.options['node'] = value

    @property
    def status_log_path(self):
        return self.options['status_log_path']

    @status_log_path.setter
    def status_log_path(self, value):
        if self.node:
            self.options['status_log_path'] = value

    @property
    def timestamp(self):
        return self.options['timestamp']

    @timestamp.setter
    def timestamp(self, value):
        self.options['timestamp'] = value