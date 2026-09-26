"""
Linux Package Management utilities.

This module provides a thin abstraction over the most common
distribution package managers (apt, dnf, yum, pacman, zypper).
It can detect the available manager on the host system and
expose helper functions to list, install, remove and search
packages.

All operations are performed via ``subprocess.run`` and return
structured data (lists of package names or command output) rather
than printing directly.  The functions are deliberately safe:
they do not raise on non‑zero exit codes but instead return
``None`` or an empty list, allowing callers to handle errors
gracefully.

Typical usage::

    from projects.linux_foundations.package_management import (
        get_package_manager,
        list_installed_packages,
        install_package,
        remove_package,
        search_package,
    )

    manager = get_package_manager()
    if manager:
        print(list_installed_packages(manager))
"""

from __future__ import annotations

import shutil
import subprocess
from typing import List, Optional, Tuple

# Mapping of package manager name to the command used for detection
_DETECTION_COMMANDS = {
    "apt": "apt-get",
    "dnf": "dnf",
    "yum": "yum",
    "pacman": "pacman",
    "zypper": "zypper",
}


def get_package_manager() -> Optional[str]:
    """
    Detect the first available package manager on the host.

    Returns
    -------
    str or None
        The name of the detected package manager (e.g. ``'apt'``) or
        ``None`` if none of the known managers are found.
    """
    for manager, binary in _DETECTION_COMMANDS.items():
        if shutil.which(binary):
            return manager
    return None


def _run_command(
    command: List[str],
) -> Tuple[int, str, str]:
    """
    Execute a command and capture its output.

    Parameters
    ----------
    command : list[str]
        The command and its arguments.

    Returns
    -------
    tuple
        ``(returncode, stdout, stderr)`` where ``stdout`` and ``stderr``
        are decoded strings.
    """
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def list_installed_packages(manager: str) -> List[str]:
    """
    List installed packages for the given package manager.

    Parameters
    ----------
    manager : str
        One of ``'apt'``, ``'dnf'``, ``'yum'``, ``'pacman'`` or ``'zypper'``.

    Returns
    -------
    list[str]
        A list of package names. Returns an empty list if the command fails
        or the manager is unknown.
    """
    if manager == "apt":
        cmd = ["dpkg-query", "-W", "-f=${Package}\n"]
    elif manager in ("dnf", "yum"):
        cmd = [manager, "list", "installed"]
    elif manager == "pacman":
        cmd = ["pacman", "-Q"]
    elif manager == "zypper":
        cmd = ["zypper", "search", "--installed-only"]
    else:
        return []

    rc, out, _ = _run_command(cmd)
    if rc != 0:
        return []

    # Different managers have different output formats; we normalise them.
    packages: List[str] = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        if manager in ("dnf", "yum"):
            # Format: package_name.version arch
            parts = line.split()
            if parts and "." in parts[0]:
                pkg = parts[0].rsplit(".", 1)[0]
                packages.append(pkg)
        elif manager == "zypper":
            # Format: i | package_name | version | repository
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 2:
                packages.append(parts[1])
        else:
            # apt (dpkg) and pacman already output one package per line
            packages.append(line.split()[0])
    return packages


def install_package(manager: str, package: str, *, assume_yes: bool = True) -> bool:
    """
    Install a package using the specified manager.

    Parameters
    ----------
    manager : str
        Package manager name.
    package : str
        Name of the package to install.
    assume_yes : bool, optional
        If True, pass the flag to automatically answer yes to prompts
        (where supported). Default is True.

    Returns
    -------
    bool
        ``True`` if the command succeeded (return code 0), ``False`` otherwise.
    """
    if manager == "apt":
        cmd = ["sudo", "apt-get", "install"]
        if assume_yes:
            cmd.append("-y")
        cmd.append(package)
    elif manager == "dnf":
        cmd = ["sudo", "dnf", "install"]
        if assume_yes:
            cmd.append("-y")
        cmd.append(package)
    elif manager == "yum":
        cmd = ["sudo", "yum", "install"]
        if assume_yes:
            cmd.append("-y")
        cmd.append(package)
    elif manager == "pacman":
        cmd = ["sudo", "pacman", "-S"]
        if assume_yes:
            cmd.append("--noconfirm")
        cmd.append(package)
    elif manager == "zypper":
        cmd = ["sudo", "zypper", "install"]
        if assume_yes:
            cmd.append("-y")
        cmd.append(package)
    else:
        return False

    rc, _, _ = _run_command(cmd)
    return rc == 0


def remove_package(manager: str, package: str, *, assume_yes: bool = True) -> bool:
    """
    Remove a package using the specified manager.

    Parameters
    ----------
    manager : str
        Package manager name.
    package : str
        Name of the package to remove.
    assume_yes : bool, optional
        If True, automatically confirm removal where supported.

    Returns
    -------
    bool
        ``True`` if removal succeeded, ``False`` otherwise.
    """
    if manager == "apt":
        cmd = ["sudo", "apt-get", "remove"]
        if assume_yes:
            cmd.append("-y")
        cmd.append(package)
    elif manager == "dnf":
        cmd = ["sudo", "dnf", "remove"]
        if assume_yes:
            cmd.append("-y")
        cmd.append(package)
    elif manager == "yum":
        cmd = ["sudo", "yum", "remove"]
        if assume_yes:
            cmd.append("-y")
        cmd.append(package)
    elif manager == "pacman":
        cmd = ["sudo", "pacman", "-R"]
        if assume_yes:
            cmd.append("--noconfirm")
        cmd.append(package)
    elif manager == "zypper":
        cmd = ["sudo", "zypper", "remove"]
        if assume_yes:
            cmd.append("-y")
        cmd.append(package)
    else:
        return False

    rc, _, _ = _run_command(cmd)
    return rc == 0


def search_package(manager: str, query: str) -> List[str]:
    """
    Search for packages matching a query.

    Parameters
    ----------
    manager : str
        Package manager name.
    query : str
        Search term.

    Returns
    -------
    list[str]
        List of matching package names (may be empty).
    """
    if manager == "apt":
        cmd = ["apt-cache", "search", query]
    elif manager == "dnf":
        cmd = ["dnf", "search", query]
    elif manager == "yum":
        cmd = ["yum", "search", query]
    elif manager == "pacman":
        cmd = ["pacman", "-Ss", query]
    elif manager == "zypper":
        cmd = ["zypper", "search", query]
    else:
        return []

    rc, out, _ = _run_command(cmd)
    if rc != 0:
        return []

    results: List[str] = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        if manager == "apt":
            # Format: package - description
            pkg = line.split()[0]
            results.append(pkg)
        elif manager in ("dnf", "yum"):
            # Format: package_name.version arch : description
            parts = line.split()
            if parts:
                pkg = parts[0].rsplit(".", 1)[0]
                results.append(pkg)
        elif manager == "pacman":
            # Format: repo/package_name version (repo) description
            if '/' in line:
                pkg = line.split('/')[1].split()[0]
                results.append(pkg)
        elif manager == "zypper":
            # Format: i | package_name | version | repository
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 2:
                results.append(parts[1])
    return results


def package_manager_info() -> Tuple[Optional[str], List[str]]:
    """
    Convenience helper returning the detected manager and a short
    description of the supported commands.

    Returns
    -------
    tuple
        ``(manager_name, supported_operations)`` where
        ``supported_operations`` is a list such as
        ``['list', 'install', 'remove', 'search']``.
    """
    manager = get_package_manager()
    ops = ["list", "install", "remove", "search"] if manager else []
    return manager, ops