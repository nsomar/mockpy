#!/usr/bin/env python

from .utils import args_parser
from .utils.network import NetworkConfig
from .core.cherrypy_server import start_mock_server
from .core.proxy_server import start_proxy_server
from .utils.config import *


def start():
    args = args_parser.parse()

    def print_environment():
        info("Running with configuration:\n"
             "Input:'%s'\n" % args.inout +
             "Resources: '%s'\n" % args.res)

    if args.proxy:
        info("Enabling network proxy on {0}:{1}".format("127.0.0.1", args.port))

        warn("Note: sudo password may be asked to enable network http/https proxies\n")

        network = NetworkConfig(args.port)
        network.apply()

        print_environment()
        info("Starting proxy server")
        start_proxy_server(args.port, args.inout, args.res, network.previous_http_proxy)
    else:
        info("Starting mock server")
        print_environment()
        start_mock_server(args.port, args.inout, args.res)
