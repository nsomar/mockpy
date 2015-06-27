__author__ = 'omarsubhiabdelhafith'

from .mapping_item import *
from functools import partial
import re

class MappingItemsManager(object):

    def __init__(self, inout_path, res_path):
        self.yaml_files = get_yaml_files(inout_path)
        create_mapping_item_with_yaml = partial(create_mapping_item, inout_path, res_path)
        self.mappings = list(map(create_mapping_item_with_yaml, self.yaml_files))

    def response_for_mapping_request(self, request):
        return [item.response for item in self.mappings if item.handles_mapping_request(request)]

    def mapping_item_for_mapping_request(self, request):
        return [item for item in self.mappings if item.handles_mapping_request(request)]


def get_yaml_files(path):
    files = os.listdir(path)
    return filter(lambda file: re.match(".*\.yml$", file), files)


def create_mapping_item(inout_path, res_path, yml_file):
    file_to_open = inout_path + "/" + yml_file
    with open(file_to_open, "r") as file:
        return MappingItem(yaml.load(file), file_to_open, res_path)


