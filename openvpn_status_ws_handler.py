#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
from tornado.websocket import WebSocketHandler, WebSocketClosedError
from time import sleep
from openvpn_status_ws_helper import get_status_log_path_for_node, parse_status_log

class OpenvpnStatusWsHandler(WebSocketHandler):
    status_log_path = None
    timestamp = None
    
    def check_origin(self, origin):
        return True

    def open(self, node):
        self.status_log_path = get_status_log_path_for_node(node)
        
        if not self.status_log_path:
            self.close()

    def on_message(self, message):
        if message.strip() == 'ping':
            data = json.dumps({'marker': 'ping'})
            self.write_message(data)

        self.send()

    def send(self):
        mtime = os.stat(self.status_log_path).st_mtime

        if mtime != self.timestamp:
            self.timestamp = mtime
            data = parse_status_log(self.status_log_path)
            self.write_message(data)
        sleep(0.5)
