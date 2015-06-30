import os
import shutil
import shutil
from config import *

class DirInit(object):

    def __init__(self, directory=None):
        path = os.popen("pwd").read().strip()
        self.path = directory if directory is not None else path

        self.res_path = self.path + "/res"
        self.inout_path = self.path + "/inout"

    def initialize(self):
        self.create_dir_if_needed(self.inout_path)
        self.create_dir_if_needed(self.res_path)
        self.copy_sample_yaml()

    def create_dir_if_needed(self, dir):
        if os.path.exists(dir):
            warn("Skipped path already exists %s" % dir)
        else:
            os.mkdir(dir)
            info("Created directory at %s" % dir)

    def copy_sample_yaml(self):
        path = os.path.join(os.path.dirname(__file__), "../data/sample.yml")
        path = os.path.normpath(path)

        dest_path = self.inout_path + "/sample.yml"

        if os.path.exists(dest_path):
            warn("Skipped sample yaml already exists %s" % dest_path)
        else:
            shutil.copyfile(path, dest_path)
            info("Created sample yaml at %s" % dest_path)

    def clear(self):
        shutil.rmtree(self.path)
