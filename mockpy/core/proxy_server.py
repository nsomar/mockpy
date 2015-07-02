#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import signal
import sys

from libmproxy import proxy, flow
from libmproxy.proxy.server import ProxyServer

from .proxy_mapper import *


class MITMProxy(flow.FlowMaster):

    def __init__(self, server, state, proxy_mapper):
        flow.FlowMaster.__init__(self, server, state)
        self.proxy_mapper = proxy_mapper
        self.start_app("mitm.it", 80)
        self.start_app("mockpycert", 80)
        self.start_app("mockpycerts", 80)
        self.start_app("mockpycerts.com", 80)
        self.start_app("mockpycert.com", 80)

    def run(self):
        flow.FlowMaster.run(self)

    def handle_request(self, f):
        f = flow.FlowMaster.handle_request(self, f)
        if f:
            self.proxy_mapper.handle_request(f)
        return f

    def handle_response(self, f):
        f = flow.FlowMaster.handle_response(self, f)
        if f:
            f.reply()
        return f


def start_proxy_server(port, inout_path, res_path, http_proxy):
    mapping_handler = MappingItemsManager(inout_path, res_path)
    proxy_mapper = ProxyMapper(mapping_handler, http_proxy)

    config = proxy.ProxyConfig(port=port, cadir="~/.mitmproxy/")

    server = ProxyServer(config)

    state = flow.State()

    m = MITMProxy(server, state, proxy_mapper)

    def signal_handler(signal, frame):
        info("\nShutting down proxy server")
        m.shutdown()
        success("Proxy server stopped")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    m.run()
