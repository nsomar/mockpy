import json
from cherrypy.lib.static import serve_file
import os


class MappingResponse(object):

    def __init__(self, response_dic, res_path):
        self.res_path = res_path
        self.response_dic = response_dic

        self.setup_status()
        self.setup_body()
        self.setup_headers()

    def title(self):
        return self.res_path + "/" + self.body.file_name

    def setup_status(self):
        self.status = self.response_dic["status"] if "status" in self.response_dic else 200

    def setup_body(self):
        self.body = BodyResponse(self.response_dic, self.res_path)

    def setup_headers(self):
        self.headers = self.response_dic.get("headers", {})
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

    def __init__(self, dic, res_path):
        self.res_path = res_path
        self.value = ""
        self._body_type = BodyResponse.NONE

        if "body_file" in dic:
            self._body_type = BodyResponse.FILE
            self.file_name = dic["body_file"]
            self.value_from_file(self.file_name)

        elif "body" in dic:
            self._body_type = BodyResponse.RAW
            self.file_name = ""
            self.set_from_object(dic["body"])

        elif "body_image" in dic:
            self._body_type = BodyResponse.IMAGE
            self.file_name = dic["body_image"]
            self.value_from_image(self.file_name)

    def read_value(self):
        return self.value()

    """
        Reading file
    """
    def value_from_file(self, file):
        self.value = lambda: self.read_file(file, decode_utf8=True)

    def set_from_object(self, object):
        if isinstance(object, str):
            self.value = lambda: json.dumps(object).encode('utf8')

        elif isinstance(object, dict) or isinstance(object, list):
            self.value = lambda: json.dumps(object).encode('utf8')

    def value_from_image(self, image):
        self.value = lambda: self.read_file(image, decode_utf8=False)

    def read_file(self, file, decode_utf8=True):
        with open(self.res_path + "/" + file, "r") as the_file:
            content = the_file.read()
            if decode_utf8:
                return content.encode('utf8')
            else:
                return content

    RAW = "raw"
    IMAGE = "image"
    FILE = "file"
    NONE = "none"
