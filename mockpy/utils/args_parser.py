#!/usr/bin/env python
import argparse
from . import config
from config import *
import os
import sys


def parse():
    parser = argparse.ArgumentParser(
        description='Start a mock server that reads input yaml res from inout directory.')

    sub_parsers = parser.add_subparsers(title="Commands", dest="sub")

    parser.add_argument('--version', help="Display version", action="count")

    add_start_parser(sub_parsers)
    add_init_parser(sub_parsers)
    add_cleanup_parser(sub_parsers)

    if has_pre_parse(parser):
        return pre_parse()

    parsed_args = parser.parse_args()

    parsed_args.init = parsed_args.sub == "init"
    parsed_args.cleanup = parsed_args.sub == "cleanup"

    if (parsed_args.init or parsed_args.cleanup) is False:
        validate_input(parsed_args)

    return parsed_args


def has_pre_parse(parser):
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)

    return sys.argv[1] == "--version"


def pre_parse():
    is_version = sys.argv[1] == "--version"

    if is_version:
        parsed_args = argparse.Namespace()
        parsed_args.version = True
        return parsed_args

    return None


def add_start_parser(sub_parsers):
    help = "Start the mocking services"
    new_parser = sub_parsers.add_parser("start", help=help,
                                        description=help)

    new_parser.add_argument('--no-proxy-update',
                            action="store_false", dest="no_proxy_update", default=True,
                            help="Dont update mac's network "
                            "proxy settings, when used the user have to set the web proxy in "
                            "System preferences -> Netwrok manually")

    new_parser.add_argument('--no-https',
                            action="store_true", dest="no_https", default=False,
                            help="Don't update mac network proxy settings for HTTPS proxy")

    new_parser.add_argument('--verbose',
                            action="store_false", dest="verbose", default=True,
                            help="Set to verbose")

    new_parser.add_argument('--port', default=9090,
                            type=int, help='Selects the desired port.')

    new_parser.add_argument('--proxy', '-x', action='count',
                            help="Start an HTTP/HTTPS proxy server to intercept calls")

    new_parser.add_argument('--inout', '-i', help="folder containing YAML input output files",
                            type=str, default="inout")

    new_parser.add_argument('--res', '-r', help="folder containing json/html/image resources",
                            type=str, default="res")

    new_parser.required = False


def add_init_parser(sub_parsers):
    help = "Creates an 'inout' and 'res' folder in the current directory"
    new_parser = sub_parsers.add_parser("init",
                                        help=help,
                                        description=help)
    new_parser.required = False


def add_cleanup_parser(sub_parsers):
    help = "Remove HTTP/HTTPS proxy setting from all networks"
    sub_parsers.add_parser("cleanup",
                           help=help,
                           description=help)


def validate_input(parsed_args):
    if not os.path.exists(parsed_args.inout):
        path = os.popen("pwd").read().strip() + "/" + parsed_args.inout
        show_directory_error(path, "input/output", "<path-to-inout-folder>")

    if not os.path.exists(parsed_args.res):
        path = os.popen("pwd").read().strip() + "/" + parsed_args.res
        show_directory_error(path, "resources", "<path-to-resources-folder>")


def show_directory_error(path, folder, hint):

    error("Default %s directory cannot be found at '%s'" % (folder, path))
    info("Make sure the folder exists or use"
         "\nmockpy -i %s" % hint)

    info("\nIf this is a new direcotry use `mockpy init` to create"
         " default inout and res folders")
    sys.exit(0)
