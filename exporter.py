"""
exporter.py
Saves IP results to files so technicians can attach them to tickets or
reports. Nothing in this file prints; each function returns the saved
file's path and display.py shows it.

Functions
---------
build_report(ipv4, ipv6, details, timestamp=None) -> dict
export_json(data, folder="exports", timestamp=None) -> str
export_csv(data, folder="exports", timestamp=None)  -> str
"""

import csv
import json
import os
from datetime import datetime

EXPORT_FOLDER = "exports"


def build_report(ipv4, ipv6, details, timestamp=None):
    """
    Combine both public IPs and the details dict into one flat report.

    The export time and the two IPs come first, followed by every field
    returned by ipapi.co, so the JSON and CSV list them in the same order.
    """
    timestamp = timestamp or datetime.now()
    report = {
        "exported_at": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "public_ipv4": ipv4,
        "public_ipv6": ipv6,
    }
    report.update(details)
    return report


def _report_path(folder, timestamp, extension):
    """
    Build exports/ip_report_<YYYYMMDD_HHMMSS>.<extension>.

    Creates the folder if it does not exist yet.
    """
    os.makedirs(folder, exist_ok=True)
    stamp = (timestamp or datetime.now()).strftime("%Y%m%d_%H%M%S")
    return os.path.join(folder, f"ip_report_{stamp}.{extension}")


def export_json(data, folder=EXPORT_FOLDER, timestamp=None):
    """Save data as an indented JSON file and return the file path."""
    path = _report_path(folder, timestamp, "json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return path


def export_csv(data, folder=EXPORT_FOLDER, timestamp=None):
    """
    Save data as a two-column CSV (Field, Value) and return the file path.

    Empty values are written as N/A so the sheet has no blank cells.
    """
    path = _report_path(folder, timestamp, "csv")
    # newline="" stops Windows from adding blank lines between rows;
    # utf-8-sig lets Excel read accented city names correctly.
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Field", "Value"])
        for field, value in data.items():
            writer.writerow([field, "N/A" if value in (None, "") else value])
    return path
