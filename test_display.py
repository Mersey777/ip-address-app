"""
test_display.py
Checks that the rich-based display functions print the expected text.
Output is captured from the shared console, so nothing reaches the screen.

Run:  python -m unittest -v
"""

import unittest

import display


class TestDisplay(unittest.TestCase):

    def capture(self, func, *args):
        """Run a display function and return what it printed as plain text."""
        with display.console.capture() as captured:
            func(*args)
        return captured.get()

    def test_show_ip_with_address(self):
        self.assertIn("203.0.113.25", self.capture(display.show_ip, "Public IPv4", "203.0.113.25"))

    def test_show_ip_not_available(self):
        out = self.capture(display.show_ip, "Public IPv6", None)
        self.assertIn("Not available on this network", out)

    def test_show_details_table(self):
        out = self.capture(display.show_details, {"asn": "AS64500", "org": "Example ISP"})
        self.assertIn("IP Details", out)
        self.assertIn("AS64500", out)
        self.assertIn("N/A", out)  # fields missing from the dict

    def test_show_analysis_table_ipv4(self):
        out = self.capture(display.show_analysis, {
            "ip": "192.168.1.1", "version": "IPv4",
            "type": "Private", "address_class": "C"})
        self.assertIn("IP Analysis", out)
        self.assertIn("Private", out)
        self.assertIn("Address Class", out)

    def test_show_analysis_hides_class_for_ipv6(self):
        out = self.capture(display.show_analysis, {
            "ip": "2001:4860:4860::8888", "version": "IPv6",
            "type": "Public", "address_class": None})
        self.assertIn("IPv6", out)
        self.assertNotIn("Address Class", out)

    def test_show_info(self):
        out = self.capture(display.show_info, "Location lookup isn't possible.")
        self.assertIn("Location lookup isn't possible.", out)

    def test_show_error_keeps_prefix_and_ignores_markup(self):
        # Square brackets in user input must print as-is, not as rich markup.
        out = self.capture(display.show_error, "'[bold]x' is not a valid IP address.")
        self.assertIn("[ERROR] '[bold]x' is not a valid IP address.", out)


if __name__ == "__main__":
    unittest.main()
