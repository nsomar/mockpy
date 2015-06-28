import yaml
from .mapping_item import *
from mockpy.utils import log
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MappingItemsManager(object):

    def __init__(self, inout_path, res_path):
        self.inout_path = inout_path
        self.res_path = res_path
        self.parse_inout_and_res()
        self.install_watchers()

    def parse_inout_and_res(self):
        self.yaml_files = get_yaml_files(self.inout_path)
        self.mappings = list(map(self.create_mapping_item, self.yaml_files))

    def create_mapping_item(self, yml_file):
        full_path = self.inout_path + "/" + yml_file

        with open(full_path, "r") as file:
            return MappingItem(yaml.load(file), full_path, self.res_path)

    def response_for_mapping_request(self, request):
        return [item.response for item in self.mappings if item.handles_mapping_request(request)]

    def mapping_item_for_mapping_request(self, request):
        return [item for item in self.mappings if item.handles_mapping_request(request)]

    def install_watchers(self):
        self.event_handler = MapperDirectoryListener(self)
        self.install_watcher(self.inout_path)
        self.install_watcher(self.res_path)

    def install_watcher(self, path):
        observer = Observer()
        observer.schedule(self.event_handler, path, recursive=True)
        observer.start()


class MapperDirectoryListener(FileSystemEventHandler):

    def __init__(self, mapping_manager):
        self.mapping_manager = mapping_manager

    def on_any_event(self, event):
        log.info("Inout or Res directory changed, rebuilding mapping settings\n"
                 "File path: %s" % event.src_path +
                 "\nEvent type: %s" % event.event_type)

        self.mapping_manager.parse_inout_and_res()
        log.success("Mapping settings rebuilt successfully")
        log.print_seperator()


def get_yaml_files(path):
    files = os.listdir(path)
    return filter(lambda file: re.match(".*\.yml$", file), files)
