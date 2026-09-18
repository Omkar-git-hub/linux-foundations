"""
Utility functions for inspecting Linux file permissions.

This module provides helpers to retrieve the symbolic and octal
representations of a file's permission bits using the standard
library ``os`` and ``stat`` modules.

Typical usage::

    from projects.linux_foundations.permissions import (
        get_permission_string,
        get_octal_permission,
    )

    perms = get_permission_string("/etc/passwd")   # e.g. "rw-r--r--"
    octal = get_octal_permission("/etc/passwd")   # e.g. "644"
"""

from __future__ import annotations

import os
import stat
from typing import Tuple

__all__: Tuple[str, ...] = (
    "get_permission_string",
    "get_octal_permission",
)


def _mode_to_symbols(mode: int) -> str:
    """
    Convert a permission ``mode`` (the lower 9 bits) to a symbolic string.

    The returned string is nine characters long, representing the
    user, group and others permissions in the order ``rwxrwxrwx``.
    If a permission bit is not set, the corresponding character is ``-``.
    """
    symbols = []
    # Owner permissions
    symbols.append("r" if mode & stat.S_IRUSR else "-")
    symbols.append("w" if mode & stat.S_IWUSR else "-")
    symbols.append("x" if mode & stat.S_IXUSR else "-")
    # Group permissions
    symbols.append("r" if mode & stat.S_IRGRP else "-")
    symbols.append("w" if mode & stat.S_IWGRP else "-")
    symbols.append("x" if mode & stat.S_IXGRP else "-")
    # Others permissions
    symbols.append("r" if mode & stat.S_IROTH else "-")
    symbols.append("w" if mode & stat.S_IWOTH else "-")
    symbols.append("x" if mode & stat.S_IXOTH else "-")
    return "".join(symbols)


def get_permission_string(path: str) -> str:
    """
    Return the symbolic permission string for *path*.

    The function follows symbolic links (i.e., it uses ``os.stat`` rather
    than ``os.lstat``).  If the file does not exist or cannot be accessed,
    ``OSError`` (or a subclass) will be raised, matching the behaviour of
    ``os.stat``.

    Example
    -------
    >>> get_permission_string("/tmp")
    'rwxrwxrwt'
    """
    st = os.stat(path)
    # Mask to the permission bits (lower 9 bits)
    mode = st.st_mode & 0o777
    return _mode_to_symbols(mode)


def get_octal_permission(path: str) -> str:
    """
    Return the octal permission representation for *path* as a zero‑padded
    three‑digit string (e.g., ``"644"``).

    This is a thin wrapper around :func:`get_permission_string` that extracts
    the numeric value from the file's mode.

    Example
    -------
    >>> get_octal_permission("/etc/passwd")
    '644'
    """
    st = os.stat(path)
    mode = st.st_mode & 0o777
    # Format as three octal digits, zero‑filled
    return f"{mode:o}".zfill(3)