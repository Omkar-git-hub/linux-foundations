"""
permissions.py

Utility functions for inspecting Linux users, groups, and sudo privileges.

This module provides a small, pure‑Python API built on the standard
library ``pwd`` and ``grp`` modules.  The functions are deliberately
simple and have no external side‑effects, making them easy to test.

Typical usage::

    from linux_foundations.permissions import (
        list_users,
        list_groups,
        get_user_groups,
        is_user_sudo,
    )

    all_users = list_users()
    admin_groups = get_user_groups('root')
    has_sudo = is_user_sudo('alice')
"""

from __future__ import annotations

import pwd
import grp
from typing import List


def list_users() -> List[str]:
    """
    Return a sorted list of all usernames present on the system.

    The function reads the password database via :mod:`pwd` and extracts the
    ``pw_name`` attribute from each entry.

    Returns
    -------
    List[str]
        Sorted usernames.
    """
    users = [entry.pw_name for entry in pwd.getpwall()]
    return sorted(users)


def list_groups() -> List[str]:
    """
    Return a sorted list of all group names present on the system.

    The function reads the group database via :mod:`grp` and extracts the
    ``gr_name`` attribute from each entry.

    Returns
    -------
    List[str]
        Sorted group names.
    """
    groups = [entry.gr_name for entry in grp.getgrall()]
    return sorted(groups)


def get_user_groups(username: str) -> List[str]:
    """
    Return a list of groups that *username* belongs to.

    The primary group (as defined by the user's ``pw_gid``) is always
    included, followed by any supplementary groups where the user appears
    in the group's member list.

    Parameters
    ----------
    username : str
        The login name to query.

    Returns
    -------
    List[str]
        Sorted group names for the user.

    Raises
    ------
    KeyError
        If *username* does not exist in the password database.
    """
    try:
        pw_entry = pwd.getpwnam(username)
    except KeyError as exc:
        raise KeyError(f"User '{username}' not found") from exc

    primary_gid = pw_entry.pw_gid
    groups = {grp.getgrgid(primary_gid).gr_name}

    for grp_entry in grp.getgrall():
        if username in grp_entry.gr_mem:
            groups.add(grp_entry.gr_name)

    return sorted(groups)


def is_user_sudo(username: str) -> bool:
    """
    Determine whether *username* has sudo privileges.

    The heuristic used is:

    1. The user is ``root`` (UID 0) – always has full privileges.
    2. The user belongs to a group named ``sudo`` or ``wheel`` – the
       conventional groups granting sudo rights on many distributions.

    The function does **not** invoke ``sudo`` or inspect the
    ``/etc/sudoers`` file; it only checks group membership, which is
    sufficient for the educational purposes of this repository.

    Parameters
    ----------
    username : str
        The login name to check.

    Returns
    -------
    bool
        ``True`` if the user is considered to have sudo rights, ``False`` otherwise.

    Raises
    ------
    KeyError
        If *username* does not exist.
    """
    try:
        pw_entry = pwd.getpwnam(username)
    except KeyError as exc:
        raise KeyError(f"User '{username}' not found") from exc

    if pw_entry.pw_uid == 0:
        return True

    user_groups = set(get_user_groups(username))
    return bool(user_groups.intersection({"sudo", "wheel"}))


__all__ = [
    "list_users",
    "list_groups",
    "get_user_groups",
    "is_user_sudo",
]