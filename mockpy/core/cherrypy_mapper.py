import types
import json
from mockpy.models.mapping_request import *
from mockpy.utils import log
from mockpy.utils.config import *
from mockpy.status.status import Status


class CherryPyMapper(object):

    def __init__(self, mapping_handler=None, cherrypy=None):
        self.mapping_handler = mapping_handler
        self.cherrypy = cherrypy
        self.status = Status(self.mapping_handler)

    def handle_request(self):

        if Status.is_status(self.cherrypy.url()):
            info("Accessing Satus")
            self.print_seperator()
            return self.status.html_response()

        request = MappingRequest(self.cherry_request_dict())
        items = self.mapping_handler.mapping_item_for_mapping_request(request)
        log.log_url(self.cherrypy.url())

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

    def cherry_request_dict(self):
        dic = {"method": self.cherrypy.request.method,
               "url": self.cherrypy.url(),
               "headers": self.cherrypy.request.headers}

        if self.cherrypy.request.process_request_body:
            dic["body"] = self.cherrypy.request.body.read()

        return dic

    def fill_headers(self, headers):
        if type({}) is not type(headers):
            return

        for key in headers.keys():
            self.cherrypy.response.headers[key] = headers[key]
