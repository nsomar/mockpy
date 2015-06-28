from mockpy.utils.config import *
from mockpy.utils import config


def print_seperator():
    info("_" * 80)


def log_multiple_matches(items):
    string = "Matched %d items, choosing the first one" % (len(items))

    for item in items:
        string += "\n- " + item.file_name
        string += "\n" + str(item.request) + "\n"

    warn(string)
    return string


def log_url(url):
    info("Request with url '%s'" % url)


def log_request(request):
    if config.verbose:
        info("===============")
        info(json.dumps(request.__dict__))
        info(json.dumps(request.__dict__))
        info("===============")

    success("\nRequest matched")
    info(str(request))


def log_response(response):
    info("Response with file: '%s'" % response.title())
