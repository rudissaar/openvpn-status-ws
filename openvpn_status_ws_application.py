#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import defaultdict
from tornado.web import Application
from tornado.websocket import WebSocketClosedError
from openvpn_status_ws_handler import OpenvpnStatusWsHandler
from time import sleep

class OpenvpnStatusWsApplication(Application):
    def __init__(self, **kwargs):
        routes = [
            (r'/(?P<node>[0-9]+)', OpenvpnStatusWsHandler),
        ]

        super().__init__(routes, **kwargs)
        self.subscriptions = defaultdict(list)

    def add_subscriber(self, channel, subscriber):
        self.subscriptions[channel].append(subscriber)

    def remove_subscriber(self, channel, subscriber):
        self.subscriptions[channel].remove(subscriber)

    def get_subscribers(self, channel):
        return self.subscriptions[channel]

    def broadcast(self, message, channel=None, sender=None):
        if channel is None:
            for channel in self.subscriptions.keys():
                self.broadcast(message, channel=channel, sender=sender)
        else:
            peers = self.get_subscribers(channel)
            for peer in peers:
                while True:
                    peer.write_message('Tick.')
                    sleep(1)
                try:
                    peer.write_message(message)
                except WebSocketClosedError:
                    self.remove_subscriber(channel, peer)
