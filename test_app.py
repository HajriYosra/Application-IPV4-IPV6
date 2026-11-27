
import unittest
from unittest.mock import patch, Mock
import requests

from ip_info import IPInfo


class TestIPInfo(unittest.TestCase):

    def setUp(self):
        self.info = IPInfo()

    # Test 1: IPv4
    @patch("ip_info.requests.get")
    def test_get_ipv4(self, mock_get):
        response = Mock()
        response.json.return_value = {"ip": "192.0.2.1"}
        mock_get.return_value = response

        result = self.info.get_ip("IPv4")

        self.assertEqual(result, "192.0.2.1")

    # Test 2: IPv6
    @patch("ip_info.requests.get")
    def test_get_ipv6(self, mock_get):
        response = Mock()
        response.json.return_value = {"ip": "2001:db8::1"}
        mock_get.return_value = response

        result = self.info.get_ip("IPv6")

        self.assertEqual(result, "2001:db8::1")

    # Test 3: Invalid version
    def test_invalid_version(self):
        result = self.info.get_ip("Unknown")

        self.assertEqual(result, "Not available")

    # Test 4: API error
    @patch("ip_info.requests.get")
    def test_api_error(self, mock_get):
        mock_get.side_effect = requests.RequestException()

        result = self.info.get_ip("IPv4")

        self.assertEqual(result, "Not available")

    # Test 5: Get details
    @patch("ip_info.requests.get")
    def test_get_details(self, mock_get):
        self.info.ipv4 = "192.0.2.1"

        response = Mock()
        response.json.return_value = {
            "success": True,
            "ip": "192.0.2.1",
            "type": "IPv4",
            "country": "Tunisia",
            "country_code": "TN",
            "continent": "Africa",
            "city": "Bizerte",
            "region": "Bizerte",
            "postal": "7000",
            "latitude": 37.27,
            "longitude": 9.87,
            "timezone": {
                "id": "Africa/Tunis",
                "utc": "+01:00"
            },
            "connection": {
                "isp": "Test ISP",
                "org": "Test Organization",
                "asn": 12345,
                "domain": "example.com"
            }
        }

        mock_get.return_value = response

        result = self.info.get_details()

        self.assertTrue(result)
        self.assertEqual(self.info.details["country"], "Tunisia")
        self.assertEqual(self.info.details["city"], "Bizerte")
        self.assertEqual(self.info.details["isp"], "Test ISP")
        self.assertEqual(self.info.details["timezone"], "Africa/Tunis")
        self.assertEqual(self.info.details["asn"], 12345)

    # Test 6: No IP available
    def test_no_ip_available(self):
        result = self.info.get_details()

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
