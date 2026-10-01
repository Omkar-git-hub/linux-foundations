"""
Linux Security Utilities.

This module provides a small collection of helper functions that can be used
to perform basic security‑related checks on a Linux system. The functions are
implemented using only the Python standard library and are safe to import on
any platform (they gracefully handle missing modules on non‑POSIX systems).

Typical usage::

    from projects.linux_foundations.security import (
        is_root_user,
        get_user_groups,
        check_ssh_root_login,
        list_world_writable_files,
        get_suid_binaries,
    )

    if is_root_user():
        print("Running as root!")

    groups = get_user_groups()
    print("Current groups:", groups)

    if check_ssh_root_login():
        print("Root login via SSH is permitted – consider disabling it.")
"""

from __future__ import annotations

import os
import stat
from pathlib import Path
from typing import List

__all__ = [
    "is_root_user",
    "get_user_groups",
    "check_ssh_root_login",
    "list_world_writable_files",
    "get_suid_binaries",
]


def is_root_user() -> bool:
    """
    Return ``True`` if the current process is running with UID 0 (root).

    On non‑POSIX platforms where ``os.geteuid`` is unavailable, the function
    falls back to checking ``os.name`` and returns ``False``.
    """
    try:
        return os.geteuid() == 0  # type: ignore[attr-defined]
    except AttributeError:
        # ``os.geteuid`` is not available on Windows; root concept does not apply.
        return False


def get_user_groups(user: str | None = None) -> List[str]:
    """
    Return a list of group names the specified *user* belongs to.

    If *user* is ``None`` the current effective user is used.  The function
    works on POSIX systems that provide the :pymod:`grp` module.  On platforms
    where ``grp`` is unavailable (e.g., Windows) an empty list is returned.

    Parameters
    ----------
    user: str | None
        Username to query.  ``None`` means the current user.

    Returns
    -------
    List[str]
        Group names.
    """
    try:
        import grp
        import pwd

        if user is None:
            uid = os.geteuid()  # type: ignore[attr-defined]
            user = pwd.getpwuid(uid).pw_name

        groups = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]

        # Primary group is not always listed in ``gr_mem``; add it explicitly.
        primary_gid = pwd.getpwnam(user).pw_gid
        primary_group = grp.getgrgid(primary_gid).gr_name
        if primary_group not in groups:
            groups.append(primary_group)

        return groups
    except Exception:
        # ``grp`` or ``pwd`` not available, or user lookup failed.
        return []


def check_ssh_root_login(ssh_config_path: str | os.PathLike = "/etc/ssh/sshd_config") -> bool:
    """
    Inspect an OpenSSH server configuration file and return ``True`` if
    ``PermitRootLogin`` is set to ``yes`` (case‑insensitive).  If the directive
    is absent or set to ``no``/``prohibit-password``/``without-password``/``forced-commands-only``,
    the function returns ``False``.

    Parameters
    ----------
    ssh_config_path: path‑like
        Path to the ``sshd_config`` file.

    Returns
    -------
    bool
        ``True`` when root login via SSH is permitted.
    """
    path = Path(ssh_config_path)
    if not path.is_file():
        return False

    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                stripped = line.strip()
                # Skip comments and empty lines
                if not stripped or stripped.startswith("#"):
                    continue
                if stripped.lower().startswith("permitrootlogin"):
                    # Split on whitespace and optional '='
                    parts = stripped.split()
                    if len(parts) >= 2:
                        value = parts[1].strip().lower()
                        # Some configs use "PermitRootLogin yes" or "PermitRootLogin=yes"
                        if value.startswith("="):
                            value = value[1:].strip()
                        return value == "yes"
        return False
    except Exception:
        return False


def list_world_writable_files(start_path: str | os.PathLike = ".") -> List[Path]:
    """
    Recursively walk *start_path* and return a list of :class:`pathlib.Path`
    objects that are world‑writable (i.e., the ``others`` write permission bit is set).

    Symbolic links are ignored to avoid following them unintentionally.

    Parameters
    ----------
    start_path: path‑like
        Directory from which the search begins.

    Returns
    -------
    List[Path]
        Paths of world‑writable regular files.
    """
    start = Path(start_path)
    if not start.is_dir():
        return []

    world_writable: List[Path] = []
    for root, dirs, files in os.walk(start, followlinks=False):
        for name in files:
            file_path = Path(root) / name
            try:
                mode = file_path.stat().st_mode
                if stat.S_ISREG(mode) and (mode & stat.S_IWOTH):
                    world_writable.append(file_path)
            except Exception:
                continue
    return world_writable


def get_suid_binaries(start_path: str | os.PathLike = "/") -> List[Path]:
    """
    Find all executable files with the set‑uid bit set under *start_path*.

    The function walks the directory tree without following symbolic links.
    Only regular files that are executable and have the ``S_ISUID`` flag are
    returned.

    Parameters
    ----------
    start_path: path‑like
        Root directory for the search.

    Returns
    -------
    List[Path]
        Paths to set‑uid binaries.
    """
    start = Path(start_path)
    if not start.is_dir():
        return []

    suid_files: List[Path] = []
    for root, dirs, files in os.walk(start, followlinks=False):
        for name in files:
            file_path = Path(root) / name
            try:
                st = file_path.stat()
                if stat.S_ISREG(st.st_mode) and (st.st_mode & stat.S_ISUID):
                    suid_files.append(file_path)
            except Exception:
                continue
    return suid_files