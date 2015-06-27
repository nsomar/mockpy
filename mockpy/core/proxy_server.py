#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import httplib
from threading import Thread
import signal
import sys

from libmproxy import controller, proxy
from libmproxy.proxy.server import ProxyServer
from libmproxy.protocol.http import HTTPRequest, HTTPResponse
from netlib.odict import ODictCaseless

from ..utils.config import *
from ..models.mapping_items_manager import *


class MITMProxy(controller.Master):
    def __init__(self, server, inout_path, res_path, http_proxy):
        controller.Master.__init__(self, server)
        self.http_proxy = http_proxy
        self.handler = MappingItemsManager(inout_path, res_path)
        success("Proxy server started")

    def handle_request(self, flow):
        request = flow.request.to_mapper_request()
        mapping_items = self.handler.mapping_item_for_mapping_request(request)

        if len(mapping_items) == 1:
            self.perform_mapping_request(flow, mapping_items[0])
        else:
            self.perform_http_request(flow)

    def perform_mapping_request(self, flow, mapping_item):
        response, request = mapping_item.response, mapping_item.request
        self.log_intercepted_request(flow, request)

        response = HTTPResponse.from_intercepted_response(response)
        flow.reply(response)

    def perform_http_request(self, flow):
        if self.http_proxy is None:
            flow.reply()
        else:
            thread = Thread(target=self.threaded_perform_http_request, args=(flow, self.http_proxy))
            thread.start()

    def threaded_perform_http_request(self, flow, proxy_settings):
        response = self.perform_request(flow.request, proxy_settings[0], proxy_settings[1])
        flow.reply(response)

    @staticmethod
    def perform_request(request, url, port):
        try:
            conn = httplib.HTTPConnection(url, port)
            headers = dict(request.headers.items())

            conn.request(request.method, request.url,
                         body=request.content, headers=headers)
            httplib_response = conn.getresponse()

            headers = ODictCaseless.from_httplib_headers(httplib_response.getheaders())
            response = HTTPResponse(code=httplib_response.status,
                                    content=httplib_response.read(),
                                    msg="",
                                    httpversion=(1, 1),
                                    headers=headers)
            return response
        except Exception as ex:
            error("Error Happened")
            error(ex)
            error("method: %s\nurl: %s\nbody: --\nheaders: --" %
                  (request.method, request.url))
            return None

    """
        Logging
    """
    @staticmethod
    def log_intercepted_request(flow, request):
        info("\nIntercepting request for URL %s"
              "\nMatching:\n%s" % (flow.request.url, str(request)))


def start_proxy_server(port, inout_path, res_path, http_proxy):
    config = proxy.ProxyConfig(port=port)
    server = ProxyServer(config)
    m = MITMProxy(server, inout_path, res_path, http_proxy)

    def signal_handler(signal, frame):
        info("\nShutting down proxy server")
        m.shutdown()
        success("Proxy server stopped")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    m.run()


def to_mapper_request(self):
    headers = dict(self.headers.items())

    params = {"url": self.url,
              "method": self.method,
              "headers": headers,
              "body": self.content}

    flow_request = MappingRequest(params)
    return flow_request


def from_httplib_headers(cls, headers):
    odict = cls()

    if type({}) is type(headers):
        for key in headers.keys():
            odict[key] = [headers[key]]

    if type([]) is type(headers):
        for header in headers:
            odict[header[0]] = [header[1]]

    return odict

def from_intercepted_response(cls, response):
    headers = ODictCaseless.from_httplib_headers(response.headers)
    response = cls(code=response.status,
                   content=response.body_response(),
                   msg="",
                   httpversion=(1, 1),
                   headers=headers)
    return response

HTTPRequest.to_mapper_request = to_mapper_request
ODictCaseless.from_httplib_headers = classmethod(from_httplib_headers)
HTTPResponse.from_intercepted_response = classmethod(from_intercepted_response)
