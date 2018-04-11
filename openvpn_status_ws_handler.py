#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from tornado.websocket import WebSocketHandler, WebSocketClosedError

class OpenvpnStatusWsHandler(WebSocketHandler):
    subscribers = set()
    timestamp = None

    def check_origin(self, origin):
        return True

    def open(self, node):
        self.node = node
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
