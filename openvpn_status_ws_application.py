#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tornado.web import Application
from tornado import gen
from tornado.ioloop import IOLoop
import datetime



class OpenvpnStatusWsApplication(Application):
    def __init__(self, **kwargs):
        from openvpn_status_ws_handler import OpenvpnStatusWsHandler

        self.peers = dict()

        routes = [
            (r'/(?P<node>[0-9]+)', OpenvpnStatusWsHandler),
        ]

        super().__init__(routes, **kwargs)

    @gen.coroutine
    def watcher(self, node):
        while True:
            print(self.peers)
            try:
                for peer in self.peers[node]:
                    print(peer)
                    peer.send()

                yield gen.Task(
                    IOLoop.current().add_timeout,
                    datetime.timedelta(milliseconds=500))
            except KeyError:
                self.peers[node] = list()

