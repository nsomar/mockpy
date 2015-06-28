#!/usr/bin/env python
import argparse
from . import config
from config import *
import os


def parse():
    global parser, args
    parser = argparse.ArgumentParser(
        description='Start a mock server that reads input yaml res from inout directory.')

    parser.add_argument('--port',
                        default=9090, type=int,
                        help='Selects the desired port.')

    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('--proxy', '-x', action='count')

    path = os.popen("pwd").read().strip()

    inout = path + "/inout"
    res = path + "/res"

    parser.add_argument('--inout', '-i', help="folder containing YAML input output files", type=str, default=inout)
    parser.add_argument('--res', '-r', help="folder containing json/html/image resources", type=str, default=res)

    parsed_args = parser.parse_args()

    config.verbose = parsed_args.verbose is not None

    validate_input(parsed_args)

    return parsed_args


def validate_input(parsed_args):
    if not os.path.exists(parsed_args.inout):
        error("The input/output YAML folder cannot be found at '%s'\n" % parsed_args.inout +
              "Make sure the folder exists or use -i [INOUT] to specify a new path")
        exit(0)

    if not os.path.exists(parsed_args.res):
        error("The resources folder cannot be found at '%s'\n" % parsed_args.res +
              "Make sure the folder exists or use -r [RES] to specify a new path")
        exit(0)
