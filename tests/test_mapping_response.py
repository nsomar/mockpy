__author__ = 'omarsubhiabdelhafith'

import unittest
from mockpy.models.mapping_respone import BodyResponse


class MappingResponseTests(unittest.TestCase):

    def test_mapping_response_loads_from_file(self):
        body = BodyResponse({"body_file": "test1.json"})
        assert "key1" in body.read_value().decode("utf-8")

        assert body.body_type == BodyResponse.FILE

    def test_mapping_response_loads_from_yml(self):

        # with self.subTest("the value is a string"):
        body = BodyResponse({"body": "test test test"})
        assert "test test test" in body.read_value().decode("utf-8")

        # with self.subTest("the value is a dict or array"):
        body = BodyResponse({"body": {"key": "value"}})
        assert "key" in body.read_value().decode("utf-8")

        body = BodyResponse({"body": ["v1", "v2"]})
        assert "v1" in body.read_value().decode("utf-8")

        assert body.body_type == BodyResponse.RAW

    def test_mapping_returns_an_image(self):
        body = BodyResponse({"body_image": "cat.png"})
        assert body.body_type == BodyResponse.IMAGE