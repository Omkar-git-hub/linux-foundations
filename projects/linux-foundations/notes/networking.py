"""
Linux Networking Fundamentals Notes

This module provides a concise overview of essential Linux networking
concepts. The `networking_fundamentals` function returns a formatted string
containing the key topics that are typically covered when learning Linux
networking.

The content is deliberately kept simple and self‑contained so that it can be
used in documentation, tutorials, or unit tests without requiring any
external resources.
"""

def networking_fundamentals() -> str:
    """
    Return a multiline string that outlines the core Linux networking
    fundamentals.

    The returned string includes sections on:

    * Network interfaces and the ``ip`` command
    * Basic IP addressing (IPv4/IPv6)
    * Routing tables and the ``ip route`` command
    * Common network utilities (ping, traceroute, netstat, ss)
    * Firewall basics with ``iptables``/``nftables``
    * DNS resolution via ``/etc/resolv.conf``
    * Hostname configuration
    * Basic troubleshooting workflow

    Returns
    -------
    str
        Formatted notes describing the fundamentals.
    """
    notes = """
Linux Networking Fundamentals
==============================

1. Network Interfaces
---------------------
- Physical (e.g., eth0, wlan0) and virtual (e.g., lo, tun0) interfaces.
- Managed with the ``ip`` command:
  ``ip link show`` – list interfaces
  ``ip link set dev <iface> up|down`` – enable/disable

2. IP Addressing
----------------
- IPv4: dotted decimal (e.g., 192.168.1.10/24)
- IPv6: colon‑hexadecimal (e.g., 2001:db8::1/64)
- Assign with ``ip addr add <addr>/<prefix> dev <iface>``

3. Routing
----------
- Kernel routing table determines packet forwarding.
- View with ``ip route show``.
- Add static route: ``ip route add <dest>/<prefix> via <gateway> dev <iface>``.

4. Common Utilities
-------------------
- ``ping`` – ICMP echo request for reachability.
- ``traceroute`` / ``tracepath`` – path discovery.
- ``ss`` / ``netstat`` – socket statistics, listening ports.
- ``curl`` / ``wget`` – HTTP client testing.

5. Firewall (iptables / nftables)
---------------------------------
- Packet filtering framework.
- Basic iptables example:
  ``iptables -A INPUT -p tcp --dport 22 -j ACCEPT``
- Modern replacement: ``nft`` with tables, chains, and rules.

6. DNS Resolution
-----------------
- Resolver reads ``/etc/resolv.conf`` for nameserver entries.
- ``dig`` and ``nslookup`` query DNS records.

7. Hostname Configuration
-------------------------
- Set hostname: ``hostnamectl set-hostname <name>``.
- ``/etc/hosts`` provides static name‑to‑IP mappings.

8. Troubleshooting Workflow
---------------------------
1. Verify interface state: ``ip link``.
2. Check IP configuration: ``ip addr``.
3. Test connectivity: ``ping`` the gateway, then an external IP.
4. Examine routing: ``ip route``.
5. Look at firewall rules: ``iptables -L`` or ``nft list ruleset``.
6. Review DNS: ``cat /etc/resolv.conf`` and ``dig`` queries.

These fundamentals form the basis for deeper topics such as
network namespaces, bonding, bridging, VPNs, and advanced routing
protocols.
"""
    return notes.strip()