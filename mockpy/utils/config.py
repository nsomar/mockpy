import re


def filter_yml(dirs):
        return filter(lambda x: re.match(".*\.yml$", x), dirs)

global verbose
verbose = False
