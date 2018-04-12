#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from tornado.websocket import WebSocketHandler, WebSocketClosedError
from time import sleep
from openvpn_status_ws_helper import get_status_log_path_for_node

class OpenvpnStatusWsHandler(WebSocketHandler):
    subscribers = set()
    status_log_path = None
    timestamp = None
    
    def check_origin(self, origin):
        return True

    def open(self, node):
        self.status_log_path = get_status_log_path_for_node(node)
        print(self.status_log_path)
        OpenvpnStatusWsHandler.subscribers.add(self)

    def on_message(self, message):
        if message.strip() == 'ping':
            self.write_message(message)

        self.write_message('message')
        self.send()

    def on_close(self):
        OpenvpnStatusWsHandler.subscribers.remove(self)

    def send(self):
        mtime = os.stat('/etc/openvpn/openvpn-status.log').st_mtime
        if mtime != self.timestamp:
            self.timestamp = mtime
            self.write_message('Changed.')
        sleep(1)
