from netlib.odict import ODictCaseless
from libmproxy.protocol.http import HTTPRequest, HTTPResponse
from ..models.mapping_items_manager import *


"""
    Extensions
"""


def to_mapper_request(self):
    headers = dict(self.headers.items())

    params = {"url": self.url,
              "method": self.method,
              "headers": headers,
              "body": self.content}

    flow_request = MappingRequest(params)
    return flow_request

HTTPRequest.to_mapper_request = to_mapper_request


def from_httplib_headers(cls, headers):
    odict = cls()

    if type({}) is type(headers):
        for key in headers.keys():
            odict[key] = [headers[key]]

    if type([]) is type(headers):
        for header in headers:
            odict[header[0]] = [header[1]]

    return odict

ODictCaseless.from_httplib_headers = classmethod(from_httplib_headers)


def from_intercepted_response(cls, response):
    headers = ODictCaseless.from_httplib_headers(response.headers)
    response = cls(code=response.status,
                   content=response.body_response(),
                   msg="",
                   httpversion=(1, 1),
                   headers=headers)
    return response


def with_html(cls, html):
    response = cls(code=200,
                   content=html,
                   msg="",
                   headers=ODictCaseless(),
                   httpversion=(1, 1))
    return response


HTTPResponse.from_intercepted_response = classmethod(from_intercepted_response)
HTTPResponse.with_html = classmethod(with_html)
