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

ADDRESS = helper.get_default_address()
define('address', default=ADDRESS, multiple=True, help='Server address or addresses to listen on.')

PORT = helper.get_default_port()
define('port', default=PORT, type=int, help='Server port to listen on.')

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
APPLICATION = OpenvpnStatusWsApplication()
SERVER = HTTPServer(APPLICATION)

if options.address:
    if isinstance(options.address, (list,)):
        for address in options.address:
            SERVER.listen(options.port, address=address)
            logging.info('> Starting server on %s:%s.', address, options.port)
    else:
        SERVER.listen(options.port, address=options.address)
        logging.info('> Starting server on %s:%s.', options.address, options.port)

signal.signal(signal.SIGINT, lambda sig, frame: shutdown(SERVER, APPLICATION))

NODES = helper.get_node_ids()

for node in NODES:
    APPLICATION.watcher(node)

IOLoop.instance().start()
