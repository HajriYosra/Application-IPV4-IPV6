
import requests


class IPInfo:

    def __init__(self):
        self.ipv4 = "Not available"
        self.ipv6 = "Not available"
        self.details = {}
        self.error_message = ""

    # Get IPv4 or IPv6 address
    def get_ip(self, version):

        if version == "IPv4":
            url = "https://api.ipify.org?format=json"

        elif version == "IPv6":
            url = "https://api6.ipify.org?format=json"

        else:
            return "Not available"

        try:
            response = requests.get(url, timeout=8)
            response.raise_for_status()

            data = response.json()
            return data.get("ip") or "Not available"

        except (requests.RequestException, ValueError):
            return "Not available"

    # Get location and network details
    def get_details(self):

        public_ip = self.ipv4

        if public_ip == "Not available" or public_ip is None:
            public_ip = self.ipv6

        if public_ip == "Not available" or public_ip is None:
            self.error_message = "No IP address available"
            return False

        try:
            response = requests.get(
                f"https://ipwho.is/{public_ip}",
                timeout=10
            )

            response.raise_for_status()
            data = response.json()

            if not data.get("success", False):
                self.error_message = "Location information unavailable"
                return False

            connection = data.get("connection") or {}
            timezone = data.get("timezone") or {}

            self.details = {
                # IP information
                "ip": data.get("ip") or "Unknown",
                "type": data.get("type") or "Unknown",

                # Geographic information
                "country": data.get("country") or "Unknown",
                "country_code": data.get("country_code") or "Unknown",
                "continent": data.get("continent") or "Unknown",
                "city": data.get("city") or "Unknown",
                "region": data.get("region") or "Unknown",
                "postal_code": data.get("postal") or "Unknown",

                # Coordinates
                "latitude": data.get("latitude") or "Unknown",
                "longitude": data.get("longitude") or "Unknown",

                # Time information
                "timezone": timezone.get("id") or "Unknown",
                "utc_offset": timezone.get("utc") or "Unknown",

                # Network information
                "isp": connection.get("isp") or "Unknown",
                "organization": connection.get("org") or "Unknown",
                "asn": connection.get("asn") or "Unknown",
                "domain": connection.get("domain") or "Unknown"
            }

            return True

        except (requests.RequestException, ValueError):
            self.error_message = "Unable to contact the information API"
            return False
