#!/usr/bin/env python

from utils import args_parser
from utils.network import NetworkConfig, turn_off_all_proxies
from core.cherrypy_server import start_mock_server
from core.proxy_server import start_proxy_server
from utils.dir_init import *
from utils.config import *
import sys
import version
import os


def start():
    args = args_parser.parse()

    if args.version:
        print_version()

    if args.init:
        perform_init()

    if args.cleanup:
        perform_cleanup()

    if args.proxy:
        previous_http_proxy = get_updated_network_proxy(args)

        show_visit_certs_if_needed(args)
        print_environment(args)
        info("Starting proxy server")
        start_proxy_server(args.port, args.inout, args.res, previous_http_proxy)
    else:
        info("Starting mock server")
        print_environment(args)
        start_mock_server(args.port, args.inout, args.res)


def get_updated_network_proxy(args):
    if not args.no_proxy_update:
        return None

    try:
        info("Enabling network proxy on {0}:{1}".format("127.0.0.1", args.port))
        warn("Note: sudo password may be asked to enable network http/https proxies\n")
        network = NetworkConfig(args.port, not args.no_https)
        network.apply()

        return network.previous_http_proxy
    except KeyboardInterrupt:
        error("Exiting...")
        sys.exit(0)


def show_visit_certs_if_needed(args):
    if args.no_proxy_update and not args.no_https:
        warn("You are using HTTPS proxying, make sure to visit http://mockpycerts.com to install "
             "SSL certificates on your machine\n")


def print_environment(args):
    path = os.popen("pwd").read().strip() + "/"
    info("Running with configuration:\n"
         "Input:'%s'\n" % (path + args.inout) +
         "Resources: '%s'\n" % (path + args.res))


def perform_init():
    current = os.popen("pwd").read().strip()
    dir_init = DirInit(current)
    dir_init.initialize()
    success("\nCurrent directory have been initialized successfully")
    info("\nTODO:\n1.Run 'mockpy'\n2.Visit http://localhost:9090/mockpy_hello_world to confirm mockpy is working")
    sys.exit(0)


def perform_cleanup():
    try:
        info("Turning off HTTP/HTTPS proxy for all networks...")
        warn("Note: sudo password may be asked to enable network http/https proxies\n")
        turn_off_all_proxies()
        success("\nHTTP/HTTPS proxy settings turned off successfully")
    except KeyboardInterrupt:
        error("Exiting...")
    finally:
        sys.exit(0)


def print_version():
    info(version.VERSION_STRING)
    sys.exit(0)
