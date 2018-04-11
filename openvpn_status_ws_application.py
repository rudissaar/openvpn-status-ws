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
