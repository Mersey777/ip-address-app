"""
display.py
Everything that prints to the screen lives here.

The base version uses plain text on purpose. Enhanced formatting
(colors, tables) is a separate feature: replace or extend the functions
below and main.py will use them automatically.
"""

import config

# Fields shown in the "full details" view: (label, key in the API dict)
DETAIL_FIELDS = [
    ("IP Address", "ip"),
    ("IP Version", "version"),
    ("ISP / Organization", "org"),
    ("ASN", "asn"),
    ("City", "city"),
    ("Region", "region"),
    ("Country", "country_name"),
    ("Country Code", "country_code"),
    ("Postal Code", "postal"),
    ("Latitude", "latitude"),
    ("Longitude", "longitude"),
    ("Timezone", "timezone"),
    ("UTC Offset", "utc_offset"),
]


def show_header():
    """Print the application banner."""
    title = f"{config.APP_NAME} v{config.APP_VERSION}"
    print("=" * len(title))
    print(title)
    print("=" * len(title))


def show_ip(label, ip):
    """Print a single IP address, or a 'not available' message."""
    if ip:
        print(f"{label}: {ip}")
    else:
        print(f"{label}: Not available on this network")


def show_details(details):
    """Print the full details dictionary returned by get_ip_details()."""
    width = max(len(label) for label, _ in DETAIL_FIELDS)
    print("-" * 40)
    for label, key in DETAIL_FIELDS:
        value = details.get(key)
        if value in (None, ""):
            value = "N/A"
        print(f"{label:<{width}} : {value}")
    print("-" * 40)


def show_error(message):
    """Print an error message."""
    print(f"[ERROR] {message}")


def show_menu(menu):
    """Print the main menu. menu is the MENU dict from main.py."""
    print()
    for key, (description, _) in menu.items():
        print(f"  [{key}] {description}")
    print("  [q] Quit")
