#!/usr/bin/env python
import argparse
from . import config
from config import *
import os
import sys


def parse():
    parser = argparse.ArgumentParser(
        description='Start a mock server that reads input yaml res from inout directory.')

    add_top_level_parser(parser)
    add_init_parser(parser)

    parsed_args = parser.parse_args()

    config.verbose = parsed_args.verbose is not None

    is_version = parsed_args.version == 1
    is_init = parsed_args.init is not None

    if is_version is False and is_init is False:
        validate_input(parsed_args)

    return parsed_args


def add_top_level_parser(parser):
    parser.add_argument('--port',
                        default=9090, type=int,
                        help='Selects the desired port.')

    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('--proxy', '-x', action='count')

    parser.add_argument('--version', action="count")

    parser.add_argument('--inout', '-i', help="folder containing YAML input output files", type=str, default="inout")
    parser.add_argument('--res', '-r', help="folder containing json/html/image resources", type=str, default="res")


def add_init_parser(parser):
    parser.add_argument("init",
                        nargs="?", help="Creates an 'inout' and 'res' folder in"
                        " the current directory", action="store")


def validate_input(parsed_args):
    if not os.path.exists(parsed_args.inout):
        path = os.popen("pwd").read().strip() + "/" + parsed_args.inout
        show_error(path, "input/output", "<path-to-inout-folder>")

    if not os.path.exists(parsed_args.res):
        path = os.popen("pwd").read().strip() + "/" + parsed_args.res
        show_error(path, "resources", "<path-to-resources-folder>")


def show_error(path, folder, hint):

    error("Default %s directory cannot be found at '%s'" % (folder, path))
    info("Make sure the folder exists or use"
         "\nmockpy -i %s" % hint)

    info("\nIf this is a new direcotry use `mockpy init` to create"
         " default inout and res folders")
    sys.exit(0)
