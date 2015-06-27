__author__ = 'omarsubhiabdelhafith'

import re
from mockpy.utils import config


class MappingRequest(object):

    def __init__(self, request_dic):
        self.url = request_dic.get("url", "")
        self.method = request_dic.get("method", "")
        self.headers = request_dic.get("headers", {})
        self.body = request_dic.get("body", "")

    def __eq__(self, other):
        matches_method = self.method_matches(other.method)
        matches_url = self.url_matches(other.url)
        matches_body = self.body_matches(other.body)
        matches_headers = HeaderMatcher(self.headers).matches(other.headers)

        if config.verbose:
            print("this_url %s, other_url %s" % (self.url, other.url))
            print("matches_method %d, matches_url %d, matches_body %d, matches_headers %d" %
                  ( matches_method, matches_url, matches_body, matches_headers))

        return  matches_method and matches_url and matches_body and matches_headers

    def __ne__(self, other):
        return not self.__eq__(other)

    def method_matches(self, method):
        return method.lower() == self.method.lower() if self.method else True

    def url_matches(self, url):
        return re.match(self.url, url) is not None

    def body_matches(self, body):
        has_body = self.body != ""
        return re.match(self.body, body) if has_body else True

    def __str__(self):
        str = "URL %s" % self.url
        if self.method != "":
            str += "\nMethod %s " % self.method
        if self.method != {}:
            str += "\nHeader %s " % self.headers
        if self.body != "":
            str += "\nBody %s " % self.body

        return str


class HeaderMatcher(object):

    def __init__(self, headers):
        self.headers = headers

    def matches(self, other_headers):
        if isinstance(self.headers, dict):
            return self.headers_matches(other_headers)
        elif isinstance(self.headers, list):
            return self.list_header_matches(other_headers)
        elif isinstance(self.headers, str):
            return self.string_header_matches(other_headers)

    def headers_matches(self, headers):
        matching_keys = self.keys_matching_other_headers_keys(headers)

        if len(matching_keys) != len(self.headers.keys()):
            return False

        return all([self.header_match(key_tuple, headers) for key_tuple in matching_keys])

    def keys_matching_other_headers_keys(self, other_headers):
        ret = []
        for key in self.headers.keys():
            matched_key = self.key_matching_headers_key(other_headers, key)
            if matched_key:
                ret.append((key, matched_key))
        return ret

    def key_matching_headers_key(self, other_headers, key):
        arr = [a_key for a_key in other_headers.keys() if re.match(key, a_key)]
        return arr[0] if arr else None

    def header_match(self, key_tuple, other_header):
        this_key = key_tuple[0]
        other_key = key_tuple[1]

        has_value = other_key in other_header
        if not has_value:
            return False

        this_value = self.headers[this_key]
        other_value = other_header[other_key]
        return re.match(this_value, other_value)

    def string_header_matches(self, other_headers, this_header= ""):
        this_header = this_header if this_header else self.headers
        other_header_strings = [k + v for (k, v) in other_headers.items()]
        return any(re.match(this_header, value) for value in other_header_strings)

    def list_header_matches(self, other_headers):
        return all(self.string_header_matches(other_headers, a_header) for a_header in self.headers)
