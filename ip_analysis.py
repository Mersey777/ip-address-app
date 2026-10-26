"""
ip_analysis.py
Technical analysis of any IPv4/IPv6 address (Feature A).

Pure logic: nothing here prints or calls an API. main.py decides what to
show based on the dict returned by analyze_ip().
"""

import ipaddress


def _classify_type(ip):
    """Return Public / Private / Loopback / Link-local / Multicast / Reserved."""
    if ip.is_loopback:
        return "Loopback"
    if ip.is_link_local:
        return "Link-local"
    if ip.is_multicast:
        return "Multicast"
    if ip.is_unspecified or ip.is_reserved:
        return "Reserved"
    if ip.is_private:
        return "Private"
    if ip.is_global:
        return "Public"
    # Not private, not global: e.g. shared address space 100.64.0.0/10.
    return "Reserved"


def _ipv4_class(ip):
    """Return the classful address class (A-E) from the first octet."""
    first_octet = int(str(ip).split(".")[0])
    if first_octet <= 127:
        return "A"
    if first_octet <= 191:
        return "B"
    if first_octet <= 223:
        return "C"
    if first_octet <= 239:
        return "D"
    return "E"


def analyze_ip(ip_string):
    """
    Analyze an IP address string and return a dict.

    Keys: valid, input, and (when valid) ip, version, type, address_class
    (IPv4 only, else None), is_public. When invalid, valid is False and
    error holds the message to show the user.
    """
    text = (ip_string or "").strip()
    try:
        ip = ipaddress.ip_address(text)
    except ValueError:
        return {
            "valid": False,
            "input": text,
            "error": f"'{text}' is not a valid IP address.",
        }

    ip_type = _classify_type(ip)
    return {
        "valid": True,
        "input": text,
        "ip": str(ip),
        "version": f"IPv{ip.version}",
        "type": ip_type,
        "address_class": _ipv4_class(ip) if ip.version == 4 else None,
        "is_public": ip_type == "Public",
    }
