"""
Utility functions for retrieving basic Linux system information.

The functions rely only on the Python standard library and are safe to run on any
POSIX‑compatible system. They provide a lightweight alternative to external tools
such as ``lsb_release`` or third‑party packages like ``psutil``.
"""

from __future__ import annotations

import os
import platform
from pathlib import Path
from typing import Dict, Any


def _parse_os_release() -> Dict[str, str]:
    """
    Parse the ``/etc/os-release`` file used by most modern Linux distributions.

    Returns
    -------
    dict
        Mapping of keys to values found in the file. Keys are returned exactly as
        they appear (e.g., ``NAME``, ``VERSION_ID``). If the file cannot be read,
        an empty dictionary is returned.
    """
    os_release_path = Path("/etc/os-release")
    data: Dict[str, str] = {}
    if not os_release_path.is_file():
        return data

    try:
        for line in os_release_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            # Strip surrounding quotes if present
            if value and value[0] in ('"', "'") and value[-1] == value[0]:
                value = value[1:-1]
            data[key] = value
    except OSError:
        # If the file cannot be read for any reason, return an empty dict.
        return {}
    return data


def get_os_release() -> Dict[str, str]:
    """
    Return a dictionary with distribution information extracted from
    ``/etc/os-release``. Typical keys include ``NAME``, ``VERSION``,
    ``ID``, ``VERSION_ID`` and ``PRETTY_NAME``.

    Returns
    -------
    dict
        Distribution metadata; empty if the file is missing or unreadable.
    """
    return _parse_os_release()


def get_uname() -> platform.uname_result:
    """
    Wrapper around :func:`platform.uname` that returns a named tuple with
    system, node, release, version, machine and processor information.

    Returns
    -------
    platform.uname_result
        The result of ``platform.uname()``.
    """
    return platform.uname()


def get_kernel_version() -> str:
    """
    Retrieve the kernel version string (e.g., ``5.15.0-76-generic``).

    Returns
    -------
    str
        The kernel release as reported by :func:`platform.release`.
    """
    return platform.release()


def get_cpu_info() -> Dict[str, Any]:
    """
    Gather basic CPU information.

    Returns
    -------
    dict
        ``processor`` – the processor name reported by :func:`platform.processor`.
        ``cores`` – number of logical CPUs as reported by :func:`os.cpu_count`.
    """
    return {
        "processor": platform.processor(),
        "cores": os.cpu_count(),
    }


def get_memory_info() -> Dict[str, int]:
    """
    Retrieve total physical memory in bytes.

    The implementation uses ``os.sysconf`` which is available on POSIX platforms.
    If the required configuration values are missing, ``total`` will be ``0``.

    Returns
    -------
    dict
        ``total`` – total RAM in bytes.
    """
    try:
        pages = os.sysconf("SC_PHYS_PAGES")
        page_size = os.sysconf("SC_PAGE_SIZE")
        total = pages * page_size
    except (ValueError, OSError, AttributeError):
        total = 0
    return {"total": total}


__all__ = [
    "get_os_release",
    "get_uname",
    "get_kernel_version",
    "get_cpu_info",
    "get_memory_info",
]