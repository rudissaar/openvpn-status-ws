#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""File that contains OpenvpnStatusWsApplication class."""

import datetime
from tornado.web import Application
from tornado import gen
from tornado.ioloop import IOLoop


class OpenvpnStatusWsApplication(Application):
    """Class that handler requests."""

    def __init__(self, **kwargs):
        """Sets up routes and properties."""
        from openvpn_status_ws_handler import OpenvpnStatusWsHandler

        self.peers = dict()

        routes = [
            (r'/(?P<node>[0-9]+)', OpenvpnStatusWsHandler),
        ]

        super().__init__(routes, **kwargs)

    @gen.coroutine
    def watcher(self, node):
        """Watch for status log file changes, and send messages if it's changed."""
        while True:
            print(self.peers)
            try:
                for peer in self.peers[node]:
                    peer.send()

                yield gen.Task(
                    IOLoop.current().add_timeout,
                    datetime.timedelta(milliseconds=500))
            except KeyError:
                self.peers[node] = list()
