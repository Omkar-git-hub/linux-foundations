"""
Utility functions and examples for common networking tools such as ``curl``,
``wget``, port inspection, and DNS resolution.

The functions are intentionally lightweight and rely only on the Python
standard library. They are meant for educational purposes and can be used
in the interactive notes or in unit‑tests.
"""

from __future__ import annotations

import socket
import subprocess
from typing import List


def curl_example() -> str:
    """
    Return a short example command line for ``curl`` that demonstrates a
    typical use‑case (downloading a file).

    Returns
    -------
    str
        Example ``curl`` command.
    """
    return "curl -O https://example.com/file.txt"


def wget_example() -> str:
    """
    Return a short example command line for ``wget`` that demonstrates a
    typical use‑case (downloading a file).

    Returns
    -------
    str
        Example ``wget`` command.
    """
    return "wget https://example.com/file.txt"


def list_open_ports() -> str:
    """
    Retrieve a list of listening TCP/UDP ports on the local machine.

    The implementation prefers the ``ss`` utility (available on most modern
    Linux distributions). If ``ss`` is not found, it falls back to ``netstat``.
    The raw command output is returned as a string.

    Returns
    -------
    str
        The output of the port‑listing command.
    """
    commands: List[List[str]] = [
        ["ss", "-tuln"],          # modern replacement for netstat
        ["netstat", "-tuln"],     # older fallback
    ]

    for cmd in commands:
        try:
            output = subprocess.check_output(
                cmd,
                stderr=subprocess.DEVNULL,
                text=True,
                errors="ignore",
            )
            return output.strip()
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue

    return "No port‑listing utility (ss or netstat) found on this system."


def resolve_dns(hostname: str) -> str:
    """
    Resolve a hostname to its IPv4 address using the system DNS resolver.

    Parameters
    ----------
    hostname : str
        The domain name to resolve (e.g., ``'example.com'``).

    Returns
    -------
    str
        The resolved IPv4 address, or an error message if resolution fails.
    """
    try:
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.gaierror as exc:
        return f"DNS resolution error for '{hostname}': {exc}"


__all__ = [
    "curl_example",
    "wget_example",
    "list_open_ports",
    "resolve_dns",
]