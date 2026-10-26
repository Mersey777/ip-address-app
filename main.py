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

import api_client
import display
import ip_analysis


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


def option_lookup_ip():
    """Look up details for any IP the user enters, with a technical analysis."""
    result = ip_analysis.analyze_ip(input("Enter an IP address: "))
    if not result["valid"]:
        display.show_error(result["error"])
        return

    display.show_analysis(result)
    if result["is_public"]:
        display.show_details(api_client.get_ip_details(result["ip"]))
    else:
        print(f"Location lookup isn't possible for {result['type'].lower()} addresses.")


# ---------------------------------------------------------------------------
# Menu: "key": ("description shown to user", function_to_run)
# Teammates: add your feature as a new line here.
# ---------------------------------------------------------------------------
MENU = {
    "1": ("Show my public IPv4 address", option_show_ipv4),
    "2": ("Show my public IPv6 address", option_show_ipv6),
    "3": ("Show full IP details (location, ISP, ASN)", option_show_details),
    "4": ("Look up any IP address", option_lookup_ip),
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
