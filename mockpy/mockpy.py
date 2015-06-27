#!/usr/bin/env python

from .utils import args_parser
from .utils.network import NetworkConfig
from .core.cherrypy_server import start_mock_server
from .core.proxy_server import start_proxy_server
import os

def start():
    args = args_parser.parse()

    def print_environment():
        print("Reading inout from '%s'\n" % args.inout +
              "Resources from '%s'" % args.res)

    if args.proxy:
        print("Enabling network proxy on {0}:{1}".format("127.0.0.1", args.port))
        network = NetworkConfig(args.port)
        network.apply()

        print_environment()
        print("Starting proxy server")
        start_proxy_server(args.port, args.inout, args.res, network.previous_http_proxy)
    else:
        print("Starting mock server on port {0}".format(args.port))
        print_environment()
        start_mock_server(args.port, args.inout, args.res)
