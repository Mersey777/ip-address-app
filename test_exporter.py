"""
test_exporter.py
Unit tests for exporter.py and the export menu option. Files are written
to a temporary folder, and the APIs are faked, so these tests run offline
and leave nothing behind.

Run:  python -m unittest -v
"""

import csv
import json
import os
import shutil
import tempfile
import unittest
from datetime import datetime
from unittest.mock import patch

import exporter
import main

SAMPLE = {
    "public_ipv4": "203.0.113.25",
    "public_ipv6": None,
    "org": "Example ISP",
    "asn": "AS64500",
    "country_code": "PH",
}
STAMP = datetime(2026, 10, 26, 21, 5, 9)


class TestExporter(unittest.TestCase):

    def setUp(self):
        # A fresh temp folder per test; "exports" inside it does not exist yet.
        self.tmp = tempfile.mkdtemp()
        self.folder = os.path.join(self.tmp, "exports")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_json_creates_folder_and_file(self):
        path = exporter.export_json(SAMPLE, folder=self.folder, timestamp=STAMP)
        self.assertTrue(os.path.isdir(self.folder))
        self.assertEqual(os.path.basename(path), "ip_report_20261026_210509.json")
        with open(path, encoding="utf-8") as f:
            self.assertEqual(json.load(f), SAMPLE)

    def test_csv_has_header_and_one_row_per_field(self):
        path = exporter.export_csv(SAMPLE, folder=self.folder, timestamp=STAMP)
        self.assertEqual(os.path.basename(path), "ip_report_20261026_210509.csv")
        with open(path, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.reader(f))
        self.assertEqual(rows[0], ["Field", "Value"])
        self.assertIn(["asn", "AS64500"], rows)
        self.assertEqual(len(rows), len(SAMPLE) + 1)

    def test_csv_writes_missing_values_as_na(self):
        path = exporter.export_csv(SAMPLE, folder=self.folder, timestamp=STAMP)
        with open(path, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.reader(f))
        self.assertIn(["public_ipv6", "N/A"], rows)

    def test_default_filename_uses_current_time(self):
        path = exporter.export_json(SAMPLE, folder=self.folder)
        self.assertRegex(os.path.basename(path), r"^ip_report_\d{8}_\d{6}\.json$")

    def test_build_report_combines_ips_and_details(self):
        report = exporter.build_report("203.0.113.25", None, {"asn": "AS64500"}, STAMP)
        self.assertEqual(report["exported_at"], "2026-10-26 21:05:09")
        self.assertEqual(report["public_ipv4"], "203.0.113.25")
        self.assertIsNone(report["public_ipv6"])
        self.assertEqual(report["asn"], "AS64500")


class TestExportOption(unittest.TestCase):

    def test_menu_option_5_is_export(self):
        self.assertIs(main.MENU["5"][1], main.option_export)

    @patch("main.display.show_saved_files")
    @patch("main.exporter.export_csv", return_value="exports/a.csv")
    @patch("main.exporter.export_json", return_value="exports/a.json")
    @patch("main.api_client.get_ip_details", return_value={"asn": "AS64500"})
    @patch("main.api_client.get_public_ipv6", return_value=None)
    @patch("main.api_client.get_public_ipv4", return_value="203.0.113.25")
    def test_option_export_saves_both_files(self, _v4, _v6, _details,
                                            mock_json, mock_csv, mock_show):
        main.option_export()
        report = mock_json.call_args[0][0]
        self.assertEqual(report["public_ipv4"], "203.0.113.25")
        self.assertEqual(report["asn"], "AS64500")
        # Both files share one timestamp so they pair up by name.
        self.assertEqual(mock_json.call_args.kwargs["timestamp"],
                         mock_csv.call_args.kwargs["timestamp"])
        mock_show.assert_called_once_with(["exports/a.json", "exports/a.csv"])


if __name__ == "__main__":
    unittest.main()
