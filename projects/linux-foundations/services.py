"""
Utility functions for interacting with systemd services via ``systemctl``.

This module provides a thin wrapper around the ``systemctl`` command-line
tool, exposing common operations such as listing services, checking their
status, and starting/stopping/restarting them.  The functions raise
``subprocess.CalledProcessError`` if the underlying ``systemctl`` call
fails, allowing callers to handle errors explicitly.

Typical usage::

    from projects.linux_foundations.services import list_units, is_active, start

    services = list_units()
    if not is_active('ssh.service'):
        start('ssh.service')
"""

from __future__ import annotations

import subprocess
from typing import List


__all__ = [
    "list_units",
    "is_active",
    "start",
    "stop",
    "restart",
    "enable",
    "disable",
]


def _run_systemctl(args: List[str]) -> subprocess.CompletedProcess:
    """
    Execute ``systemctl`` with the given arguments.

    Parameters
    ----------
    args :
        List of arguments to pass to ``systemctl`` (excluding the command itself).

    Returns
    -------
    subprocess.CompletedProcess
        The completed process object.

    Raises
    ------
    subprocess.CalledProcessError
        If ``systemctl`` exits with a non‑zero status.
    """
    cmd = ["systemctl"] + args
    return subprocess.run(
        cmd,
        check=True,
        capture_output=True,
        text=True,
    )


def list_units(filter_type: str = "service") -> List[str]:
    """
    List all systemd units of a given type.

    By default, this returns the names of all service units (``*.service``).

    Parameters
    ----------
    filter_type :
        The unit type to filter on (e.g., ``service``, ``socket``, ``timer``).

    Returns
    -------
    List[str]
        A list of unit names (e.g., ``['ssh.service', 'cron.service']``).

    Raises
    ------
    subprocess.CalledProcessError
        If the ``systemctl`` command fails.
    """
    result = _run_systemctl(
        [
            "list-units",
            f"--type={filter_type}",
            "--all",
            "--no-legend",
            "--no-pager",
        ]
    )
    units = []
    for line in result.stdout.strip().splitlines():
        if not line:
            continue
        # The first column is the unit name.
        unit_name = line.split()[0]
        units.append(unit_name)
    return units


def is_active(unit: str) -> bool:
    """
    Check whether a given unit is active.

    Parameters
    ----------
    unit :
        The full unit name (e.g., ``ssh.service``).

    Returns
    -------
    bool
        ``True`` if the unit is active, ``False`` otherwise.

    Raises
    ------
    subprocess.CalledProcessError
        If ``systemctl`` encounters an unexpected error.
    """
    try:
        result = _run_systemctl(["is-active", unit])
        return result.stdout.strip() == "active"
    except subprocess.CalledProcessError as exc:
        # ``systemctl is-active`` returns a non‑zero exit code for inactive units.
        # Treat that as ``False`` rather than propagating the exception.
        if exc.returncode == 3:  # inactive
            return False
        raise


def start(unit: str) -> None:
    """
    Start the specified unit.

    Parameters
    ----------
    unit :
        The full unit name (e.g., ``ssh.service``).

    Raises
    ------
    subprocess.CalledProcessError
        If the start operation fails.
    """
    _run_systemctl(["start", unit])


def stop(unit: str) -> None:
    """
    Stop the specified unit.

    Parameters
    ----------
    unit :
        The full unit name (e.g., ``ssh.service``).

    Raises
    ------
    subprocess.CalledProcessError
        If the stop operation fails.
    """
    _run_systemctl(["stop", unit])


def restart(unit: str) -> None:
    """
    Restart the specified unit.

    Parameters
    ----------
    unit :
        The full unit name (e.g., ``ssh.service``).

    Raises
    ------
    subprocess.CalledProcessError
        If the restart operation fails.
    """
    _run_systemctl(["restart", unit])


def enable(unit: str) -> None:
    """
    Enable the specified unit to start at boot.

    Parameters
    ----------
    unit :
        The full unit name (e.g., ``ssh.service``).

    Raises
    ------
    subprocess.CalledProcessError
        If the enable operation fails.
    """
    _run_systemctl(["enable", unit])


def disable(unit: str) -> None:
    """
    Disable the specified unit from starting at boot.

    Parameters
    ----------
    unit :
        The full unit name (e.g., ``ssh.service``).

    Raises
    ------
    subprocess.CalledProcessError
        If the disable operation fails.
    """
    _run_systemctl(["disable", unit])