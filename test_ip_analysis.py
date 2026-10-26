"""Offline tests for ip_analysis.analyze_ip()."""

import unittest

from ip_analysis import analyze_ip


class AnalyzeIPTests(unittest.TestCase):
    """Check version, type and class for representative addresses."""

    def test_public_ipv4_class_a(self):
        """8.8.8.8 is a public class A IPv4 address."""
        r = analyze_ip("8.8.8.8")
        self.assertTrue(r["valid"])
        self.assertEqual(r["version"], "IPv4")
        self.assertEqual(r["type"], "Public")
        self.assertEqual(r["address_class"], "A")
        self.assertTrue(r["is_public"])

    def test_private_ipv4_class_c(self):
        """192.168.1.1 is private, class C, and must not be looked up."""
        r = analyze_ip("192.168.1.1")
        self.assertEqual(r["type"], "Private")
        self.assertEqual(r["address_class"], "C")
        self.assertFalse(r["is_public"])

    def test_loopback(self):
        """127.0.0.1 is loopback."""
        self.assertEqual(analyze_ip("127.0.0.1")["type"], "Loopback")

    def test_public_ipv6(self):
        """2001:4860:4860::8888 is public IPv6 with no address class."""
        r = analyze_ip("2001:4860:4860::8888")
        self.assertEqual(r["version"], "IPv6")
        self.assertEqual(r["type"], "Public")
        self.assertIsNone(r["address_class"])
        self.assertTrue(r["is_public"])

    def test_invalid_input(self):
        """Non-IP text is reported invalid with the required message."""
        r = analyze_ip("abc")
        self.assertFalse(r["valid"])
        self.assertEqual(r["error"], "'abc' is not a valid IP address.")

    def test_link_local_multicast_reserved(self):
        """Link-local, multicast and reserved ranges are classified."""
        self.assertEqual(analyze_ip("169.254.1.1")["type"], "Link-local")
        self.assertEqual(analyze_ip("224.0.0.1")["type"], "Multicast")
        self.assertEqual(analyze_ip("224.0.0.1")["address_class"], "D")
        self.assertEqual(analyze_ip("240.0.0.1")["type"], "Reserved")
        self.assertEqual(analyze_ip("240.0.0.1")["address_class"], "E")

    def test_whitespace_is_trimmed(self):
        """Surrounding spaces do not make a valid IP invalid."""
        self.assertTrue(analyze_ip("  1.1.1.1 ")["valid"])


if __name__ == "__main__":
    unittest.main()
