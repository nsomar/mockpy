__author__ = 'omarsubhiabdelhafith'
import unittest
from mockpy.status.status import Status

class StatusTests(unittest.TestCase):

    def test_gets_status_correctly(self):
        self.assertEqual(Status.is_status("http://127.0.0.1/status"), True)
        self.assertEqual(Status.is_status("127.0.0.1/status"), True)
        self.assertEqual(Status.is_status("http://localhost/status"), True)
        self.assertEqual(Status.is_status("http://localhost123/status"), False)
        self.assertEqual(Status.is_status("http://1.1.1.1/status/123"), False)
        self.assertEqual(Status.is_status("http://1.1.1.1/sanotus"), False)

    def test_gets_status_correctly_with_mockpy_domain(self):
        self.assertEqual(Status.is_status("http://mockpy/status"), True)
