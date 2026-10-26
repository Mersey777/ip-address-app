"""
test_api_client.py
Unit tests for api_client.py. The real APIs are replaced with fake
responses, so these tests run offline and never hit rate limits.

Run:  python -m unittest -v
"""

import unittest
from unittest.mock import MagicMock, patch

import requests

import api_client


def fake_response(json_data, status=200):
    """Build a fake requests.Response object."""
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = json_data
    return resp


class TestApiClient(unittest.TestCase):

    @patch("api_client.requests.get")
    def test_ipv4_success(self, mock_get):
        mock_get.return_value = fake_response({"ip": "203.0.113.25"})
        self.assertEqual(api_client.get_public_ipv4(), "203.0.113.25")

    @patch("api_client.requests.get")
    def test_ipv6_success(self, mock_get):
        mock_get.return_value = fake_response({"ip": "2001:db8::1"})
        self.assertEqual(api_client.get_public_ipv6(), "2001:db8::1")

    @patch("api_client.requests.get")
    def test_ipv6_unavailable_returns_none(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError()
        self.assertIsNone(api_client.get_public_ipv6())

    @patch("api_client.requests.get")
    def test_ipv6_fallback_to_ipv4_returns_none(self, mock_get):
        mock_get.return_value = fake_response({"ip": "203.0.113.25"})
        self.assertIsNone(api_client.get_public_ipv6())

    @patch("api_client.requests.get")
    def test_details_success(self, mock_get):
        mock_get.return_value = fake_response(
            {"ip": "203.0.113.25", "org": "Example ISP", "asn": "AS64500",
             "country_code": "PH"}
        )
        details = api_client.get_ip_details("203.0.113.25")
        self.assertEqual(details["asn"], "AS64500")
        self.assertEqual(details["country_code"], "PH")

    @patch("api_client.requests.get")
    def test_details_api_error(self, mock_get):
        mock_get.return_value = fake_response({"error": True, "reason": "RateLimited"})
        with self.assertRaises(api_client.IPLookupError):
            api_client.get_ip_details("203.0.113.25")

    @patch("api_client.requests.get")
    def test_rate_limit_status(self, mock_get):
        mock_get.return_value = fake_response({}, status=429)
        with self.assertRaises(api_client.IPLookupError):
            api_client.get_public_ipv4()

    @patch("api_client.requests.get")
    def test_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout()
        with self.assertRaises(api_client.IPLookupError):
            api_client.get_public_ipv4()


if __name__ == "__main__":
    unittest.main()
