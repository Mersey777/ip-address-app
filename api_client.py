"""
api_client.py
All REST API calls live here. Nothing in this file prints to the screen;
it only fetches data and returns Python dictionaries/strings.
display.py is responsible for showing the results.

Functions
---------
get_public_ipv4()        -> str | None
get_public_ipv6()        -> str | None
get_ip_details(ip=None)  -> dict

Errors are raised as IPLookupError so the caller (main.py) can show a
friendly message instead of a Python traceback.
"""

import requests

import config


class IPLookupError(Exception):
    """Raised when an API call fails or returns unusable data."""


def _get_json(url):
    """
    Send a GET request and return the parsed JSON body.

    Raises IPLookupError on network problems, bad HTTP status codes,
    or a response that is not valid JSON.
    """
    try:
        response = requests.get(
            url, headers=config.HEADERS, timeout=config.TIMEOUT_SECONDS
        )
    except requests.exceptions.Timeout:
        raise IPLookupError(f"Request timed out after {config.TIMEOUT_SECONDS}s.")
    except requests.exceptions.ConnectionError:
        raise IPLookupError("Could not connect to the API (check your internet).")
    except requests.exceptions.RequestException as err:
        raise IPLookupError(f"Request failed: {err}")

    if response.status_code == 429:
        raise IPLookupError("API rate limit reached. Please wait and try again.")
    if response.status_code != 200:
        raise IPLookupError(f"API returned HTTP status {response.status_code}.")

    try:
        return response.json()
    except ValueError:
        raise IPLookupError("API response was not valid JSON.")


def get_public_ipv4():
    """Return this computer's public IPv4 address as a string."""
    data = _get_json(config.IPV4_URL)
    return data.get("ip")


def get_public_ipv6():
    """
    Return this computer's public IPv6 address as a string, or None if the
    network has no IPv6 connectivity (very common on home/school networks).
    """
    try:
        data = _get_json(config.IPV6_URL)
    except IPLookupError:
        # api6.ipify.org can only be reached over IPv6, so a connection
        # failure here almost always means "no IPv6 on this network".
        return None
    ip = data.get("ip")
    # If the network fell back to IPv4, don't report it as IPv6.
    if ip and ":" not in ip:
        return None
    return ip


def get_ip_details(ip=None):
    """
    Return geolocation / ISP / ASN details for an IP as a dictionary.

    If ip is None, the details are for this computer's own public IPv4.

    Keys returned by ipapi.co include: ip, version, city, region,
    country_name, country_code, postal, latitude, longitude, timezone,
    utc_offset, asn, org (the ISP), currency.
    """
    if ip is None:
        ip = get_public_ipv4()

    data = _get_json(config.DETAILS_URL.format(ip=ip))

    # ipapi.co reports problems in the body: {"error": true, "reason": "..."}
    if data.get("error"):
        raise IPLookupError(f"Lookup failed: {data.get('reason', 'unknown reason')}")

    return data
