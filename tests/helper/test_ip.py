""" Test for module helper.ip"""

import requests
from unittest import TestCase
from unittest.mock import patch
from lib.ip import get_public_ip


class MockResponse:
    """ A mock response class"""

    def __init__(self, text, status_code):
        self.text = text
        self.status_code = status_code


def mock_valid_response():
    """ Return a requests response object with valid content"""
    return MockResponse("192.168.0.111", 200)


def mock_invalid_response_status_code():
    """ Return a requests response object with error status code"""
    return MockResponse("192.168.0.111", 404)


class TestIp(TestCase):
    """ Test suit"""

    @patch("requests.get", return_value=mock_valid_response())
    def test_get_public_ip(self, _):
        """ Target returns a valid IP"""
        self.assertEqual("192.168.0.111", get_public_ip())

    @patch("requests.get", return_value=mock_invalid_response_status_code())
    def test_get_public_ip_invalid_status_code(self, _):
        """ Target returns a valid IP"""
        self.assertEqual(None, get_public_ip())

    @patch("requests.get")
    def test_get_public_ip_with_exception(self, mock):
        """ Target returns a valid IP"""
        mock.side_effect = requests.exceptions.ConnectionError
        self.assertEqual(None, get_public_ip())
