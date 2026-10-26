"""
config.py
Central settings for the IPv4/IPv6 Address Application.

Keep every URL and tunable value here so nobody has to hunt through the
code to change an API or a timeout.
"""

# --- Public IP APIs (free, no API key needed) -------------------------------
# ipify returns ONLY your public IP. api.ipify.org is IPv4-only and
# api6.ipify.org is IPv6-only, so each call tests one protocol.
IPV4_URL = "https://api.ipify.org?format=json"
IPV6_URL = "https://api6.ipify.org?format=json"

# ipapi.co returns details for an IP: geolocation, ISP (org), ASN,
# country code, timezone, etc. {ip} is filled in at runtime.
# Free tier: about 1,000 requests/day, no key required.
DETAILS_URL = "https://ipapi.co/{ip}/json/"

# --- Request settings -------------------------------------------------------
TIMEOUT_SECONDS = 10

# ipapi.co may reject requests that have no User-Agent header.
HEADERS = {"User-Agent": "DEVASC-IP-Address-App/1.0"}

APP_NAME = "IPv4/IPv6 Address Application"
APP_VERSION = "1.0.0"
