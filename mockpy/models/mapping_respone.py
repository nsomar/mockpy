import json
from cherrypy.lib.static import serve_file
import os

RESOURCE_DIR = "res"


class MappingResponse(object):

    def __init__(self, response_dic, res_path):
        global RESOURCE_DIR
        RESOURCE_DIR = res_path

        self.status = response_dic["status"] if "status" in response_dic else 200
        self.body = BodyResponse(response_dic)
        self.headers = response_dic.get("headers", {})
        self.adjust_header_for_body_type()

    def adjust_header_for_body_type(self):
        if self.body.body_type == BodyResponse.IMAGE:
            self.headers["Content-Type"] = "image/png"
            self.headers["Accept-Ranges"] = "bytes"

    def body_response(self):
        return self.body.read_value()

    def headers(self):
        return self.headers


class BodyResponse(object):

    @property
    def body_type(self):
        return self._body_type

    def __init__(self, dic):
        self.value = ""

        self._body_type = BodyResponse.NONE
        if "body_file" in dic:
            self._body_type = BodyResponse.FILE
            self.set_from_file(dic["body_file"])
        elif "body" in dic:
            self._body_type = BodyResponse.RAW
            self.set_from_object(dic["body"])
        elif "body_image" in dic:
            self._body_type = BodyResponse.IMAGE
            self.set_from_image(dic["body_image"])

    def read_value(self):
        return self.value()

    def set_from_object(self, object):
        if isinstance(object, str):
            self.value = lambda: json.dumps(object).encode('utf8')

        elif isinstance(object, dict) or isinstance(object, list):
            self.value = lambda: json.dumps(object).encode('utf8')

    def set_from_file(self, file):
        self.value = lambda: BodyResponse.read_file(file, decode_utf8=True)

    def set_from_image(self, image):
        self.value = lambda: BodyResponse.read_file(image, decode_utf8=False)

    @staticmethod
    def read_file(file, decode_utf8=True):
        with open(RESOURCE_DIR + "/" + file, "r") as the_file:
            content = the_file.read()
            if decode_utf8:
                return content.encode('utf8')
            else:
                return content

    RAW = "raw"
    IMAGE = "image"
    FILE = "file"
    NONE = "none"
