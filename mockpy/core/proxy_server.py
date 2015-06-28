#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import httplib
from threading import Thread
import signal
import sys

from libmproxy import controller, proxy
from libmproxy.proxy.server import ProxyServer

from ..utils import log
from .proxy_mapper import *


class MITMProxy(controller.Master):

    def __init__(self, server, proxy_mapper):
        controller.Master.__init__(self, server)
        self.proxy_mapper = proxy_mapper

    def handle_request(self, flow):
        self.proxy_mapper.handle_request(flow)


def start_proxy_server(port, inout_path, res_path, http_proxy):
    config = proxy.ProxyConfig(port=port)
    server = ProxyServer(config)

    mapping_handler = MappingItemsManager(inout_path, res_path)

    proxy_mapper = ProxyMapper(mapping_handler, http_proxy)
    m = MITMProxy(server, proxy_mapper)

    def signal_handler(signal, frame):
        info("\nShutting down proxy server")
        m.shutdown()
        success("Proxy server stopped")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    m.run()
