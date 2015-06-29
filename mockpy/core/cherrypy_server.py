#!/usr/bin/env python

import cherrypy
from mockpy.models.mapping_items_manager import *
from cherrypy_mapper import *
import signal
from mockpy.utils.config import *


class CherryPyServer(object):
    exposed = True

    def __init__(self, inout_path, res_path):
        self.handler = MappingItemsManager(inout_path, res_path)
        success("Server started successfully at %s:%s" %
                ("http://127.0.0.1", cherrypy.config["server.socket_port"]))

    @cherrypy.expose
    def default(self, *args, **kwargs):
        mapper = CherryPyMapper(mapping_handler=self.handler, cherrypy=cherrypy)
        return mapper.handle_request()


def start_mock_server(port, inout_path, res_path):
    cherrypy.config.update({'server.socket_port': port, "environment": "embedded"})

    def signal_handler(signal, frame):
        info("\nShutting down server")
        cherrypy.engine.exit()
        success("Server shutdown successfully")

    signal.signal(signal.SIGINT, signal_handler)
    cherrypy.quickstart(CherryPyServer(inout_path, res_path))
