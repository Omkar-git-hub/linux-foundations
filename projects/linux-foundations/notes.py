"""
File Permissions Notes Module.

This module provides human‑readable notes and utilities related to Unix
file permission concepts. It is intended for educational purposes and can
be imported by other parts of the ``linux-foundations`` package.

Typical usage:

    from projects.linux_foundations.notes import file_permissions_notes

    print(file_permissions_notes())
"""

from __future__ import annotations

import stat
from typing import List


def _octal_permission_string(mode: int) -> str:
    """
    Convert a permission ``mode`` integer to a zero‑padded octal string
    (e.g. ``0o755``).

    Parameters
    ----------
    mode: int
        The integer mode as returned by ``os.stat`` or similar.

    Returns
    -------
    str
        Octal representation of the permission bits.
    """
    # Mask only the permission bits (owner, group, others)
    perm_bits = mode & 0o777
    return f"0o{perm_bits:03o}"


def _symbolic_permission_string(mode: int) -> str:
    """
    Convert a permission ``mode`` integer to the symbolic representation
    used by ``ls -l`` (e.g. ``rwxr-xr-x``).

    Parameters
    ----------
    mode: int
        The integer mode as returned by ``os.stat`` or similar.

    Returns
    -------
    str
        Symbolic permission string.
    """
    symbols = [
        (stat.S_IRUSR, "r"),
        (stat.S_IWUSR, "w"),
        (stat.S_IXUSR, "x"),
        (stat.S_IRGRP, "r"),
        (stat.S_IWGRP, "w"),
        (stat.S_IXGRP, "x"),
        (stat.S_IROTH, "r"),
        (stat.S_IWOTH, "w"),
        (stat.S_IXOTH, "x"),
    ]

    result: List[str] = []
    for flag, char in symbols:
        result.append(char if mode & flag else "-")
    return "".join(result)


def file_permissions_notes() -> str:
    """
    Return a detailed multi‑line note describing Unix file permission
    concepts, including numeric (octal) and symbolic representations,
    special bits, and common usage patterns.

    The note is formatted for easy printing or inclusion in documentation.

    Returns
    -------
    str
        The permission notes.
    """
    notes = [
        "Unix File Permission Overview",
        "-----------------------------",
        "",
        "Each file has three sets of permission bits:",
        "  * Owner (user)   – what the file's owner can do",
        "  * Group          – what users in the file's group can do",
        "  * Others         – what everyone else can do",
        "",
        "For each set there are three possible actions:",
        "  * Read    (r) – permission to read the file or list a directory",
        "  * Write   (w) – permission to modify the file or create/delete entries",
        "  * Execute (x) – permission to run a file as a program or traverse a directory",
        "",
        "These nine bits are commonly expressed in two ways:",
        "",
        "1. Symbolic notation (as shown by ``ls -l``):",
        "   Example: rwxr-xr--",
        "   This string is built from the three groups in order:",
        "   owner  group  others",
        "",
        "2. Octal (numeric) notation:",
        "   Each group of three bits is interpreted as an octal digit (0‑7).",
        "   Example: 0o754",
        "",
        "Octal calculation:",
        "   read  = 4, write = 2, execute = 1",
        "   Sum the values for each group:",
        "     owner  = 4+2+1 = 7",
        "     group  = 4+0+1 = 5",
        "     others = 4+0+0 = 4",
        "",
        "Special permission bits (setuid, setgid, sticky):",
        "   * setuid (4xxx) – execute with the file owner's privileges",
        "   * setgid (2xxx) – execute with the file group's privileges",
        "   * sticky (1xxx) – restrict deletion within a directory",
        "",
        "Common commands:",
        "   chmod 755 file   – rwxr-xr-x (owner full, group/others read/execute)",
        "   chmod u+x file   – add execute permission for the owner",
        "   chmod g-w file   – remove write permission from the group",
        "   chmod 1777 /tmp  – drwxrwxrwt (sticky bit on /tmp)",
        "",
        "Programmatic access (Python example):",
        "   >>> import os, stat",
        "   >>> st = os.stat('some_file')",
        "   >>> mode = st.st_mode",
        "   >>> octal = _octal_permission_string(mode)",
        "   >>> symbolic = _symbolic_permission_string(mode)",
        "   >>> print(octal, symbolic)",
        "",
        "Understanding these representations helps when managing file security,",
        "debugging permission errors, and writing scripts that manipulate",
        "filesystem objects.",
    ]
    return "\n".join(notes)


__all__ = [
    "file_permissions_notes",
    "_octal_permission_string",
    "_symbolic_permission_string",
]