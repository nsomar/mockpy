from mockpy.models.mapping_request import *
from mockpy.utils import log
from mockpy.utils.config import *
from mockpy.status.status import check_status_cherry_py
import mockpy.utils.cherrypy_extensions


class CherryPyMapper(object):

    def __init__(self, mapping_handler=None, cherrypy=None):
        self.mapping_handler = mapping_handler
        self.cherrypy = cherrypy

    @check_status_cherry_py
    def handle_request(self):

        log.log_url(self.cherrypy.url())

        request = self.cherrypy.to_mapper_request()
        items = self.mapping_handler.mapping_item_for_mapping_request(request)

        if len(items) == 0:
            self.cherrypy.response.status = 500
            return "no response found for request"

        if len(items) > 1:
            log.log_multiple_matches(items)

        matched_item = items[0]
        response = matched_item.response

        self.cherrypy.response.status = response.status
        self.fill_headers(response.headers)

        log.log_request(matched_item.request)
        log.log_response(response)
        log.print_seperator()

        return response.body_response()

    def check_status(func):
        def parse_status(*args, **kwargs):
            print args
            return ""
        return parse_status

    def fill_headers(self, headers):
        if type({}) is not type(headers):
            return

        for key in headers.keys():
            self.cherrypy.response.headers[key] = headers[key]
