import types
import json
from mockpy.models.mapping_request import *
from mockpy.utils import config


class CherryPyMapper(object):

    def __init__(self, mapping_handler=None, cherrypy=None):
        self.mapping_handler = mapping_handler
        self.cherrypy = cherrypy

    def handle_request(self):

        if self.is_status(self.cherrypy.url()):
            return self.status_response()

        request = MappingRequest(self.cherry_request_dict())
        responses = self.mapping_handler.response_for_mapping_request(request)

        if config.verbose:
            print("===============")
            print(json.dumps(request.__dict__))
            print(json.dumps(request.__dict__))
            print("===============")

        if len(responses) == 0:
            self.cherrypy.response.status = 500
            return "no response found for request"

        if len(responses) > 1:
            self.cherrypy.response.status = 500
            return "matched multiple responses"

        response = responses[0]


        self.cherrypy.response.status = response.status
        self.fill_headers(response.headers)

        return response.body_response()

    def cherry_request_dict(self):
        dic = {"method": self.cherrypy.request.method,
               "url": self.cherrypy.url(),
               "headers": self.cherrypy.request.headers}

        if self.cherrypy.request.process_request_body:
            dic["body"] = self.cherrypy.request.body.read()

        return dic

    def status_response(self):
        string = "Server running correctly<br/><br/>"
        string += "Parsed res:<br/>"
        for file in self.mapping_handler.yaml_files:
            string += " - " + file + "<br/>"

        return string

    @staticmethod
    def is_status(url):
        return re.match(".*/status$", url) is not None

    def fill_headers(self, headers):
        if type({}) is not type(headers):
            return

        for key in headers.keys():
            self.cherrypy.response.headers[key] = headers[key]