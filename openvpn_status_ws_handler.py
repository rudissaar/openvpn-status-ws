#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""File that contains OpenvpnStatusWsHandler class."""

import os
import json

from tornado.websocket import WebSocketHandler
from urllib.parse import urlparse

import openvpn_status_ws_helper as helper
from openvpn_status_ws_parser import OpenvpnStatusWsParser


class OpenvpnStatusWsHandler(WebSocketHandler):
    """Class that handler WebSocket connections."""
    # pylint: disable=W0223
    options = dict()
    options['node'] = None
    options['status_log_path'] = None
    options['timestamp'] = None

    def check_origin(self, origin):
        node = helper.get_node_from_uri(self.request.uri)
        domain = urlparse(origin).netloc.lower()

        if not node in helper.get_node_ids():
            return False

        return True

    def open(self, node):
        # pylint: disable=W0221
        self.node = node
        self.status_log_path = helper.get_status_log_path_for_node(self.node)

        if self.status_log_path is None:
            self.close()

        try:
            self.application.peers[self.node].append(self)
        except KeyError:
            self.application.peers[self.node] = list()

        # Reset timestamp value on connect so client gets message on next send action.
        self.timestamp = None
        self.send()

    def on_message(self, message):
        """Reads client's message and executes logic passed on that message."""
        if message.strip() == 'ping':
            data = json.dumps({'marker': 'ping'})
            self.write_message(data)
        elif message.strip() == 'fetch':
            self.send()

    def on_close(self):
        self.application.peers[self.node].remove(self)

    def send(self):
        """Sends parsed data to client if source file is modified since last check."""
        mtime = os.stat(self.status_log_path).st_mtime

        if mtime != self.timestamp:
            self.timestamp = mtime
            parser = OpenvpnStatusWsParser(self.status_log_path)
            parsed_log = parser.data

            if parsed_log:
                data = dict()
                data['marker'] = 'data'
                data['content'] = parsed_log
                self.write_message(data)

    @property
    def node(self):
        """Returns value of node property."""
        return self.options['node']

    @node.setter
    def node(self, value):
        if isinstance(value, str) and value.isnumeric():
            self.options['node'] = int(value)
        elif isinstance(value, int):
            self.options['node'] = value

    @property
    def status_log_path(self):
        """Returns value of status_log_path property."""
        return self.options['status_log_path']

    @status_log_path.setter
    def status_log_path(self, value):
        if self.node:
            self.options['status_log_path'] = value

    @property
    def timestamp(self):
        """Returns value of timestamp property."""
        return self.options['timestamp']

    @timestamp.setter
    def timestamp(self, value):
        self.options['timestamp'] = value
