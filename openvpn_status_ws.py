#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Bootstrap file and entry point."""

import signal
import time
import logging

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, parse_command_line, options

import openvpn_status_ws_helper as helper
from openvpn_status_ws_application import OpenvpnStatusWsApplication

define('debug', default=False, type=bool, help='Run in debug mode.')
define('port', default=12200, type=int, help='Server port.')
define('address', default='0.0.0.0', help='Server address.')

def shutdown(server, application):
    """Stops application and server."""
    application.running = False
    ioloop = IOLoop.instance()
    logging.info('> Stopping server.')
    server.stop()

    def finalize():
        """Makes sure that script will be terminated."""
        ioloop.stop()
        logging.info('> Stopped.')

    ioloop.add_timeout(time.time() + 1, finalize)

parse_command_line()
APPLICATION = OpenvpnStatusWsApplication(debug=options.debug)
SERVER = HTTPServer(APPLICATION)
SERVER.listen(options.port, address=options.address)
signal.signal(signal.SIGINT, lambda sig, frame: shutdown(SERVER, APPLICATION))
logging.info('Starting server on %s:%s', options.address, options.port)

NODES = helper.get_nodes()

for node in NODES:
    APPLICATION.watcher(node)

IOLoop.instance().start()
