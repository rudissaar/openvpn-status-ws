#!/usr/bin/env python3
from tornado.websocket import WebSocketHandler, WebSocketClosedError

class OpenvpnStatusWsHandler(WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.application.add_subscriber(self.sprint, self)

    def on_message(self, message):
        self.application.broadcast(message, channel=self.sprint, sender=self)

    def on_close(self):
        self.application.remove_subscriber(self.sprint, self)
