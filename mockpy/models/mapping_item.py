import yaml
from .mapping_request import MappingRequest
from .mapping_respone import MappingResponse
from os.path import basename
import os


class MappingItem(object):

    def __init__(self, dic, file_name, res_path):
        self.request = MappingRequest(dic["request"])
        self.response = MappingResponse(dic["response"], res_path)

        self.display_name = self.get_display_name(dic, file_name)

    def get_display_name(self, dic, file_name):
        if "name" in dic:
            return dic["name"]
        else:
            return os.path.splitext(basename(file_name))[0]

    def handles_mapping_request(self, other_request):
        return self.request == other_request
