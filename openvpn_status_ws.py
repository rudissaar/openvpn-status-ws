#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Bootstrap file and entry point."""

import signal
import time
import logging

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.log import LogFormatter
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
    logging.info('{SERVER} Preparing to stop server.')
    server.stop()

    def finalize():
        """Makes sure that script will be terminated."""
        ioloop.stop()
        logging.info('{SERVER} Server successfully stopped.')

    ioloop.add_timeout(time.time() + 1, finalize)

parse_command_line()

LOG_FORMAT = '%(color)s[%(levelname)s] %(asctime)s :%(end_color)s %(message)s'
LOG_FORMATTER = LogFormatter(fmt=LOG_FORMAT, color=True, datefmt='%Y-%m-%d %H:%M:%S %z')
APP_LOGGER = logging.getLogger()
APP_STREAM_HANDLER = APP_LOGGER.handlers[0]
APP_STREAM_HANDLER.setFormatter(LOG_FORMATTER)

APPLICATION = OpenvpnStatusWsApplication()
SERVER = HTTPServer(APPLICATION)

if options.address:
    if isinstance(options.address, (list,)):
        for address in options.address:
            try:
                SERVER.listen(options.port, address=address)
                logging.info('{SERVER} Starting server on %s:%s.', address, options.port)
            except OSError as ex:
                if ex.errno == 98:
                    print("Interface that you are trying to bind port on is already in use.")
                    print('...')
                    print('In case you are using IP address 0.0.0.0 or [::] inside your ')
                    print("configuration, make sure that this address is only address in it's ")
                    print("IP family (IPv4/IPv6).")
                else:
                    print('>' + ex)

                exit(1)
    else:
        SERVER.listen(options.port, address=options.address)
        logging.info('{SERVER} Starting server on %s:%s.', options.address, options.port)

signal.signal(signal.SIGINT, lambda sig, frame: shutdown(SERVER, APPLICATION))

NODES = helper.get_node_ids()

for node in NODES:
    APPLICATION.watcher(node)

IOLoop.instance().start()
