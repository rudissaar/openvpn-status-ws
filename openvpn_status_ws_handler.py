#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tornado.websocket import WebSocketHandler, WebSocketClosedError

class OpenvpnStatusWsHandler(WebSocketHandler):
    node = None

    def check_origin(self, origin):
        return True

    def open(self, node):
        self.node = node
        self.application.add_subscriber(self.node, self)

    def on_message(self, message):
        self.application.broadcast(message, channel=self.node, sender=self)

    def on_close(self):
        self.application.remove_subscriber(self.node, self)
