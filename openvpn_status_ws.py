#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import signal
import time
import logging
from tornado.options import define, parse_command_line, options
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler, WebSocketClosedError
from tornado.web import Application
from collections import defaultdict
import openvpn_status_ws_helper as helper
import json


from openvpn_status_ws_application import OpenvpnStatusWsApplication

define('debug', default=False, type=bool, help='Run in debug mode')
define('port', default=12200, type=int, help='Server port')
define('address', default='0.0.0.0', help='Server address')
define('allowed_hosts', default="localhost:12200", multiple=True,
       help='Allowed hosts for cross domain connections')


def shutdown(server, application):
    application.running = False
    ioloop = IOLoop.instance()
    logging.info('> Stopping server.')
    server.stop()

    def finalize():
        ioloop.stop
        logging.info('> Stopped.')
        exit(0)

    ioloop.add_timeout(time.time() + 1, finalize)

parse_command_line()
application = OpenvpnStatusWsApplication(debug=options.debug)
server = HTTPServer(application)
server.listen(options.port, address=options.address)
signal.signal(signal.SIGINT, lambda sig, frame: shutdown(server, application))
logging.info('Starting server on {}:{}'.format(options.address, options.port))

nodes = helper.get_nodes()
for node in nodes:
    application.watcher(node)

IOLoop.instance().start()
