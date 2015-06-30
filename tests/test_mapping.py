import unittest
from mockpy.models.mapping_items_manager import *
from mock import Mock
from mockpy.core.cherrypy_mapper import *

from os import path

input_path = os.path.dirname(path.abspath(__file__)) + "/inout"
res_path = os.path.dirname(path.abspath(__file__)) + "/res"


class MapperTests(unittest.TestCase):

    def setUp(self):
        self.mapper = MappingItemsManager(input_path, res_path)

    def test_display_name_is_correct(self):
        names = [mapping.display_name for mapping in self.mapper.mappings]
        assert "Some great name" in names
        assert "test1" in names

    def test_returns_all_matching_requests(self):
        mock_mapping_request = Mock(url="http://www.some_base.com/1/2/x/IPrintBoardingPass?test", method="get")
        assert len(self.mapper.response_for_mapping_request(mock_mapping_request)) == 2

        mock_mapping_request = Mock(url="http://www.some_base.com/IPrintBoardingPass?test", method="get")
        assert len(self.mapper.response_for_mapping_request(mock_mapping_request)) == 1

        mock_mapping_request = Mock(url="http://www.some_base.com/1/2/x/ss?test", method="get")
        assert len(self.mapper.response_for_mapping_request(mock_mapping_request)) == 1

    def test_returns_all_matching_requests_for_method(self):
        mock_mapping_request = Mock(url="..2/x/IPrintBoardingPass?test", method="Get")
        assert len(self.mapper.response_for_mapping_request(mock_mapping_request)) == 1

        mock_mapping_request = Mock(url="..2/x/IPrintBoardingPass?test", method="gEt")
        assert len(self.mapper.response_for_mapping_request(mock_mapping_request)) == 1

        mock_mapping_request = Mock(url="..2/x/IPrintBoardingPass?test", method="post")
        assert len(self.mapper.response_for_mapping_request(mock_mapping_request)) == 0


class MapperResponseTests(unittest.TestCase):

    def setUp(self):
        self.mapper = MappingItemsManager(input_path, res_path)

    def test_return_body(self):
        mock_mapping_request = Mock(url="http://www.some_base.com/1/2/x/ss?test", method="get")
        response = self.mapper.response_for_mapping_request(mock_mapping_request)[0]

        assert "key1" in response.body_response().decode("utf-8")
        assert "abc" not in response.body_response().decode("utf-8")

    def test_return_status_code(self):
        mock_mapping_request = Mock(url="http://www.some_base.com/1/2/x/ss?test", method="get")
        response = self.mapper.response_for_mapping_request(mock_mapping_request)[0]

        assert response.status == 200

    def test_return_correct_header(self):
        mock_mapping_request = Mock(url="http://www.some_base.com/1/2/x/ss?test", method="get")
        response = self.mapper.response_for_mapping_request(mock_mapping_request)[0]

        assert response.headers["Content-type"] == "application/json; charset=utf-8"


class CherryPyMapperTests(unittest.TestCase):

    def test_can_set_headers(self):
        mock_mapper = Mock()
        item1 = Mock()
        item1.response = Mock(status=1, headers={"header_key": "header_value"})
        mock_mapper.mapping_item_for_mapping_request = Mock(return_value=[item1])

        mock_cherry = Mock()
        mock_cherry.response = Mock(status=1, headers={})
        mock_cherry.url = Mock(return_value="ss")

        assert mock_cherry.response.headers == {}

        cherry_mapper = CherryPyMapper(mapping_handler=mock_mapper, cherrypy=mock_cherry)
        cherry_mapper.handle_request()

        assert mock_cherry.response.headers == {"header_key": "header_value"}

if __name__ == '__main__':
    unittest.main()
