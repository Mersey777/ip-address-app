"""
main.py
Entry point for the IPv4/IPv6 Address Application.

Run:  python main.py

HOW TO ADD A NEW FEATURE (for teammates)
----------------------------------------
1. Write a function that takes no arguments, e.g. def export_results(): ...
   (put API logic in api_client.py and printing in display.py if you can).
2. Add ONE line to the MENU dict below with the next free number.
That's it -- the menu, input handling and error catching are already done.
Adding only one line here keeps merge conflicts between branches small.
"""

from datetime import datetime

import api_client
import display
import exporter


# ---------------------------------------------------------------------------
# Feature functions (one per menu option)
# ---------------------------------------------------------------------------

def option_show_ipv4():
    """Show this computer's public IPv4 address."""
    display.show_ip("Public IPv4", api_client.get_public_ipv4())


def option_show_ipv6():
    """Show this computer's public IPv6 address (if the network has IPv6)."""
    display.show_ip("Public IPv6", api_client.get_public_ipv6())


def option_show_details():
    """Show both IPs plus geolocation, ISP and ASN for the IPv4 address."""
    ipv4 = api_client.get_public_ipv4()
    ipv6 = api_client.get_public_ipv6()
    display.show_ip("Public IPv4", ipv4)
    display.show_ip("Public IPv6", ipv6)
    display.show_details(api_client.get_ip_details(ipv4))


def option_export():
    """Fetch both IPs and the details, then save them as JSON and CSV."""
    ipv4 = api_client.get_public_ipv4()
    ipv6 = api_client.get_public_ipv6()
    details = api_client.get_ip_details(ipv4)
    # One timestamp for both files so the .json and .csv pair up by name.
    now = datetime.now()
    report = exporter.build_report(ipv4, ipv6, details, now)
    paths = [
        exporter.export_json(report, timestamp=now),
        exporter.export_csv(report, timestamp=now),
    ]
    display.show_saved_files(paths)


# ---------------------------------------------------------------------------
# Menu: "key": ("description shown to user", function_to_run)
# Teammates: add your feature as a new line here.
# ---------------------------------------------------------------------------
MENU = {
    "1": ("Show my public IPv4 address", option_show_ipv4),
    "2": ("Show my public IPv6 address", option_show_ipv6),
    "3": ("Show full IP details (location, ISP, ASN)", option_show_details),
    "5": ("Export my IP details (JSON + CSV)", option_export),
}


def main():
    """Main loop: show the menu, run the chosen option, repeat until quit."""
    display.show_header()
    while True:
        display.show_menu(MENU)
        choice = input("\nSelect an option: ").strip().lower()

        if choice in ("q", "quit", "exit"):
            print("Goodbye!")
            break

        if choice not in MENU:
            display.show_error("Invalid option. Please choose from the menu.")
            continue

        _, feature = MENU[choice]
        try:
            feature()
        except api_client.IPLookupError as err:
            display.show_error(str(err))


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
