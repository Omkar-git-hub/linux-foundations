"""
Linux Networking Notes

This module provides concise reference notes for common Linux networking
commands, configuration files, and concepts. The notes are stored in the
`NOTES` constant and can be accessed via the `get_notes` function.

The content is deliberately kept short and focused on frequently used
operations such as inspecting interfaces, configuring IP addresses,
managing routing tables, and troubleshooting connectivity.
"""

from __future__ import annotations

__all__: list[str] = ["NOTES", "get_notes"]


NOTES: str = """\
# Linux Networking Reference

## Interface Inspection
- `ip link show` – List all network interfaces and their status.
- `ifconfig -a` – Legacy command to display interfaces (requires net-tools).

## IP Address Management
- `ip addr show <iface>` – Show IP configuration for a specific interface.
- `ip addr add <addr>/<prefix> dev <iface>` – Assign an IPv4/IPv6 address.
- `ip addr del <addr>/<prefix> dev <iface>` – Remove an address.
- `ifconfig <iface> <addr> netmask <mask> up` – Legacy way to set an address.

## Bringing Interfaces Up/Down
- `ip link set <iface> up` – Activate an interface.
- `ip link set <iface> down` – Deactivate an interface.
- `ifup <iface>` / `ifdown <iface>` – Debian/Ubuntu helper scripts.

## Routing
- `ip route show` – Display the routing table.
- `ip route add default via <gateway> dev <iface>` – Set default gateway.
- `ip route del <dest>` – Remove a route.
- `route -n` – Legacy routing table view.

## DNS Configuration
- `/etc/resolv.conf` – Contains nameserver entries.
  Example:
  ```
  nameserver 8.8.8.8
  nameserver 1.1.1.1
  ```

## Common Troubleshooting Tools
- `ping <host>` – Test ICMP reachability.
- `traceroute <host>` – Show path packets take to a destination.
- `ss -tuln` – List listening TCP/UDP sockets.
- `netstat -tulnp` – Legacy socket list (requires net-tools).
- `dig <domain>` / `nslookup <domain>` – DNS query utilities.
- `tcpdump -i <iface>` – Capture packets on an interface.
- `nmap <target>` – Network scanning and host discovery.

## Wireless (Wi‑Fi) Utilities
- `iwconfig` – Show wireless interface parameters.
- `nmcli` – NetworkManager command‑line tool.
- `wpa_supplicant` – WPA/WPA2 authentication daemon.

## Persistent Configuration (Debian/Ubuntu)
- `/etc/network/interfaces` – Classic static configuration file.
- `/etc/netplan/*.yaml` – Netplan YAML configuration (used on newer releases).

## Persistent Configuration (RHEL/CentOS)
- `/etc/sysconfig/network-scripts/ifcfg-<iface>` – Interface definition files.

## Quick One‑Liners
- Show public IP: `curl -s https://ifconfig.me`
- Restart networking service:
  - Systemd: `systemctl restart networking` (Debian) or `systemctl restart NetworkManager`
  - SysVinit: `/etc/init.d/networking restart`

--- End of Notes ---
"""


def get_notes() -> str:
    """
    Return the networking notes string.

    Returns
    -------
    str
        The multiline networking reference notes.
    """
    return NOTES