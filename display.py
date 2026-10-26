"""
display.py
Everything that prints to the screen lives here.

Output uses the rich library for colors, panels and tables. Function
names and parameters are the same as the plain-text base version, so
main.py and other features call them without any changes.
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

import config

# One shared console for the whole app (tests capture its output).
console = Console()

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
    """Print the application banner as a colored panel."""
    title = Text(f"{config.APP_NAME} v{config.APP_VERSION}", style="bold cyan")
    console.print(Panel(title, subtitle="DEVASC Project Activity 3",
                        border_style="cyan", expand=False))


def show_ip(label, ip):
    """Print a single IP address in green, or 'not available' in yellow."""
    line = Text(f"{label}: ", style="bold")
    if ip:
        line.append(ip, style="green")
    else:
        line.append("Not available on this network", style="yellow")
    console.print(line)


def show_details(details):
    """Print the details dict from get_ip_details() as a Field | Value table."""
    table = Table(title="IP Details", title_style="bold cyan")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")
    for label, key in DETAIL_FIELDS:
        value = details.get(key)
        if value in (None, ""):
            value = "N/A"
        # Text() keeps API values from being read as rich markup.
        table.add_row(label, Text(str(value)))
    console.print(table)


def show_error(message):
    """Print an error message in red."""
    # Text() rather than a markup string, so brackets in the message
    # (including the [ERROR] prefix or user input) print as-is.
    console.print(Text(f"[ERROR] {message}", style="bold red"))


def show_saved_files(paths):
    """Print the paths of exported files."""
    console.print(Text("Report saved:", style="bold green"))
    for path in paths:
        console.print(Text(f"  {path}", style="green"))


def show_menu(menu):
    """Print the main menu. menu is the MENU dict from main.py."""
    console.print()
    for key, (description, _) in menu.items():
        console.print(Text.assemble(("  [", "dim"), (key, "bold cyan"),
                                    ("] ", "dim"), description))
    console.print(Text.assemble(("  [", "dim"), ("q", "bold cyan"),
                                ("] ", "dim"), "Quit"))
