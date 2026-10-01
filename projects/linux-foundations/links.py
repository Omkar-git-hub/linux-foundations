"""
Utility functions for working with filesystem links and special permissions.

This module provides helpers to inspect symbolic links as well as to query
special permission bits (setuid, setgid, sticky) on any filesystem entry.
"""

import os
import stat
from typing import List

__all__ = [
    "is_symlink",
    "readlink",
    "has_setuid",
    "has_setgid",
    "has_sticky",
    "get_special_permissions",
]

def is_symlink(path: str) -> bool:
    """
    Return ``True`` if *path* refers to a symbolic link.
    """
    return os.path.islink(path)


def readlink(path: str) -> str:
    """
    Return the target of the symbolic link *path*.

    Raises ``OSError`` if *path* is not a symbolic link.
    """
    return os.readlink(path)


def _mode(path: str) -> int:
    """
    Return the mode bits of *path* using ``os.lstat`` (so that the link itself
    is examined, not the target).
    """
    return os.lstat(path).st_mode


def has_setuid(path: str) -> bool:
    """
    Return ``True`` if the set‑uid bit is set on *path*.
    """
    return bool(_mode(path) & stat.S_ISUID)


def has_setgid(path: str) -> bool:
    """
    Return ``True`` if the set‑gid bit is set on *path*.
    """
    return bool(_mode(path) & stat.S_ISGID)


def has_sticky(path: str) -> bool:
    """
    Return ``True`` if the sticky bit is set on *path*.
    """
    return bool(_mode(path) & stat.S_ISVTX)


def get_special_permissions(path: str) -> List[str]:
    """
    Return a list describing the special permission bits set on *path*.

    The list may contain any of the following strings, in this order:

    * ``"setuid"`` – set‑uid bit is set
    * ``"setgid"`` – set‑gid bit is set
    * ``"sticky"`` – sticky bit is set

    If no special bits are set, an empty list is returned.
    """
    perms = []
    if has_setuid(path):
        perms.append("setuid")
    if has_setgid(path):
        perms.append("setgid")
    if has_sticky(path):
        perms.append("sticky")
    return perms