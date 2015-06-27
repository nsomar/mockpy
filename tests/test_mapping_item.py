__author__ = 'omarsubhiabdelhafith'

import unittest
from mock import Mock
from mockpy.models.mapping_items_manager import *
from os import path

res_path = os.path.dirname(path.abspath(__file__)) + "/res"


class MappingItemTests(unittest.TestCase):

    def setUp(self):
        dic = {}
        dic["request"] = {"method": "GET", "url": ".*1/2.*"}
        dic["response"] = {"status": 1234}
        dic["name"] = "test1"
        self.subject = MappingItem(dic, "", res_path)

    def test_handles_mapping_request(self):
        mock_mapping_request = Mock()
        mock_mapping_request.__eq__ = Mock(return_value=True)
        self.subject.request = mock_mapping_request

        self.subject.handles_mapping_request(mock_mapping_request)
        assert self.subject.request.__eq__.called

    def test_gets_display_name(self):
        assert self.subject.display_name == "test1"