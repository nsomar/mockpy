__author__ = 'omarsubhiabdelhafith'

import unittest
from mockpy.models.mapping_respone import BodyResponse
import os


class MappingResponseTests(unittest.TestCase):


    def test_mapping_response_loads_from_file(self):

        body = BodyResponse({"body_file": "test1.json"}, os.path.dirname(__file__) + "/res")
        assert "key1" in body.read_value().decode("utf-8")

        assert body.body_type == BodyResponse.FILE


    def test_mapping_response_loads_from_yml(self):

        body = BodyResponse({"body": "test test test"}, os.path.dirname(__file__) + "/res")
        assert "test test test" in body.read_value().decode("utf-8")

        body = BodyResponse({"body": {"key": "value"}}, os.path.dirname(__file__) + "/res")
        assert "key" in body.read_value().decode("utf-8")

        body = BodyResponse({"body": ["v1", "v2"]}, os.path.dirname(__file__) + "/res")
        assert "v1" in body.read_value().decode("utf-8")

        assert body.body_type == BodyResponse.RAW


    def test_mapping_returns_an_image(self):
        body = BodyResponse({"body_image": "cat.png"}, os.path.dirname(__file__) + "/res")
        assert body.body_type == BodyResponse.IMAGE


    def test_has_correct_file_name_for_file(self):

        body = BodyResponse({"body_file": "test1.json"}, os.path.dirname(__file__) + "/res")
        assert body.file_name == "test1.json"


    def test_has_correct_file_name_for_object(self):
        body = BodyResponse({"body": "test test test"}, os.path.dirname(__file__) + "/res")
        assert body.file_name == ""


    def test_has_correct_file_name_for_image(self):
        body = BodyResponse({"body_image": "cat.png"}, os.path.dirname(__file__) + "/res")
        assert body.file_name == "cat.png"
