__author__ = 'omarsubhiabdelhafith'

import unittest
from mockpy.core.cherrypy_mapper import *


class MappingRequestTests(unittest.TestCase):

    def test_equal_to_url(self):
        request_1 = MappingRequest({"url": ".*1/2.*"})
        request_2 = MappingRequest({"url": ".*1/2.*"})
        assert request_1 == request_2

        request_2 = MappingRequest({"url": ".*1/2/3.*"})
        assert request_1 == request_2

        request_1 = MappingRequest({"url": ".*1/2/3.*"})
        request_2 = MappingRequest({"url": ".*1/2.*"})
        assert request_1 != request_2

    def test_check_method_is_equal(self):
        request_1 = MappingRequest({"url": ".*1/2.*", "method": "get"})
        request_2 = MappingRequest({"url": ".*1/2.*", "method": "gEt"})
        assert request_1 == request_2

        request_1 = MappingRequest({"url": ".*1/2.*", "method": "get"})
        request_2 = MappingRequest({"url": ".*1/2.*"})
        assert request_1 != request_2

        request_1 = MappingRequest({"url": ".*1/2.*"})
        request_2 = MappingRequest({"url": ".*1/2.*", "method": "get"})
        assert request_1 == request_2

        request_1 = MappingRequest({"url": ".*1/2.*", "method": "post"})
        request_2 = MappingRequest({"url": ".*1/2.*", "method": "get"})
        assert request_1 != request_2

    def test_check_method_is_equal(self):
        request_1 = MappingRequest({"url": ".*1/2.*", "method": "get"})
        request_2 = MappingRequest({"url": ".*1/2.*", "method": "gEt"})
        assert request_1 == request_2

    def test_check_matches_body(self):
        request_1 = MappingRequest({"url": ".*1/2.*", "body": ".*TheKey.*Value.*"})
        request_2 = MappingRequest({"url": ".*1/2.*", "body": "TheKeyEqual=ATestValueIs"})
        assert request_1 == request_2

        request_1 = MappingRequest({"url": ".*1/2.*", "body": ".*TheKey.*XTheValue.*"})
        request_2 = MappingRequest({"url": ".*1/2.*", "body": "TheKeyEqual=TestTheValueIs"})
        assert request_1 != request_2

    def test_check_matches_headers(self):

        dic_headers = {"key1": "value1", "key2": "value2"}
        request_2 = MappingRequest({"url": ".*1/2.*", "headers": dic_headers})

        # with self.subTest("no headers"):
        request_1 = MappingRequest({"url": ".*1/2.*"})
        assert request_1 == request_2

        # with self.subTest("does not have equal headers"):
        dic_headers = {"keyx": "valuex"}
        request_1 = MappingRequest({"url": ".*1/2.*", "headers": dic_headers})
        assert request_1 != request_2

        # with self.subTest("has exact headers"):
        dic_headers = {"key1": "value1"}
        request_1 = MappingRequest({"url": ".*1/2.*", "headers": dic_headers})
        assert request_1 == request_2

        # with self.subTest("has pattern value headers"):
        dic_headers = {"key1": "va.*1"}
        request_1 = MappingRequest({"url": ".*1/2.*", "headers": dic_headers})
        assert request_1 == request_2

        # with self.subTest("has pattern key headers"):
        dic_headers = {"k.*1": "value1"}
        request_1 = MappingRequest({"url": ".*1/2.*", "headers": dic_headers})
        assert request_1 == request_2

        # with self.subTest("all headers must match"):
        dic_headers = {"k.*1": "value1", "key2": "value2"}
        request_1 = MappingRequest({"url": ".*1/2.*", "headers": dic_headers})
        assert request_1 == request_2

        dic_headers = {"k.*1": "value1", "k.*2": "v.*2"}
        request_1 = MappingRequest({"url": ".*1/2.*", "headers": dic_headers})
        assert request_1 == request_2

        # with self.subTest("only some match returns false"):
        dic_headers = {"k.*1": "value1", "key3": "value2"}
        request_1 = MappingRequest({"url": ".*1/2.*", "headers": dic_headers})
        assert request_1 != request_2

    def test_matches_headers_also_as_string(self):
        dic_headers = {"key1": "value1", "key2": "value2"}
        request_2 = MappingRequest({"url": ".*1/2.*", "headers": dic_headers})

        # with self.subTest("matches"):
        request_1 = MappingRequest({"url": ".*1/2.*", "headers": "ke.*val.*"})
        assert request_1 == request_2

        # with self.subTest("does not matches"):
        request_1 = MappingRequest({"url": ".*1/2.*", "headers": "kex.*val.*"})
        assert request_1 != request_2

    def test_matches_headers_also_as_array(self):
        dic_headers = {"key1": "value1", "key2": "value2"}
        request_2 = MappingRequest({"url": ".*1/2.*", "headers": dic_headers})

        # with self.subTest("all matches"):
        request_1 = MappingRequest({"url": ".*1/2.*", "headers": ["k.*1.*v.*1", "k.*2.*v.*2"]})
        assert request_1 == request_2

        # with self.subTest("some dont match"):
        request_1 = MappingRequest({"url": ".*1/2.*", "headers": ["k.*1.*v.*1", "k.*3.*v.*2"]})
        assert request_1 != request_2
