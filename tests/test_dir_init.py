import unittest
from mockpy.utils.dir_init import *
import tempfile
from os import path
import sys
from StringIO import StringIO


class DirInitTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        dir_init = DirInit(self.temp_dir)
        self.dir_init = dir_init

    def test_creates_inout_and_res(self):

        self.dir_init.initialize()

        assert os.path.exists(self.temp_dir + "/inout") == True
        assert os.path.exists(self.temp_dir + "/res") == True

    def test_does_note_overwrite_exisiting(self):

        self.dir_init.initialize()

        out = StringIO()
        sys.stdout = out
        self.dir_init.initialize()
        output = out.getvalue().strip()

        self.assertEqual("inout" in output, True)
        self.assertEqual("res" in output, True)

    def test_creates_sample_yaml(self):

        self.dir_init.initialize()
        assert os.path.exists(self.temp_dir + "/inout/sample.yml") == True

    def tearDown(self):
        self.dir_init.clear()
