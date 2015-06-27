__author__ = 'omarsubhiabdelhafith'

from .mapping_item import *
from functools import partial
from mockpy.utils import config


class MappingItemsManager(object):

    def __init__(self, inout_path, res_path):
        self.yaml_files = config.filter_yml(os.listdir(inout_path))
        self.mappings = list(map(partial(load_file, inout_path, res_path), self.yaml_files))

    def response_for_mapping_request(self, request):
        return [item.response for item in self.mappings if item.handles_mapping_request(request)]

    def mapping_item_for_mapping_request(self, request):
        return [item for item in self.mappings if item.handles_mapping_request(request)]


def load_file(inout_path, res_path, yml_file):
    file_to_open = inout_path + "/" + yml_file
    with open(file_to_open, "r") as file:
        return MappingItem(yaml.load(file), file_to_open, res_path)


