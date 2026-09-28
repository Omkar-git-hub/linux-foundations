"""
Utilities for interacting with systemd services via ``systemctl``.

The functions provided are thin wrappers around the ``systemctl`` command
and return the command output as Python objects.  They are intended for
educational purposes and simple scripting; for production‑grade
interaction consider using a dedicated library such as ``dbus`` or
``pydbus``.
"""

from __future__ import annotations

import subprocess
from typing import List, Tuple, Optional


def _run_systemctl(*args: str, capture_output: bool = True) -> subprocess.CompletedProcess:
    """
    Execute ``systemctl`` with the supplied arguments.

    Parameters
    ----------
    *args:
        Arguments passed directly to ``systemctl``.
    capture_output:
        If ``True`` (default) the standard output and error are captured
        and returned in the ``CompletedProcess`` instance.

    Returns
    -------
    subprocess.CompletedProcess
        The result of the command execution.

    Raises
    ------
    RuntimeError
        If the ``systemctl`` executable cannot be found or the command
        fails to start.
    """
    cmd = ["systemctl", *args]
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("systemctl not found on this system") from exc
    return result


def list_services(active_only: bool = True) -> List[Tuple[str, str]]:
    """
    List systemd services.

    Parameters
    ----------
    active_only:
        When ``True`` (default) only services in the ``active`` state are
        returned.  When ``False`` all loaded services are listed.

    Returns
    -------
    List[Tuple[str, str]]
        A list of ``(service_name, load_state)`` tuples.
    """
    args = ["list-units", "--type=service", "--no-legend", "--no-pager"]
    if active_only:
        args.append("--state=active")
    result = _run_systemctl(*args)

    services: List[Tuple[str, str]] = []
    for line in result.stdout.strip().splitlines():
        if not line:
            continue
        # Expected format: UNIT LOAD ACTIVE SUB DESCRIPTION
        parts = line.split()
        if parts:
            unit = parts[0]
            load_state = parts[1] if len(parts) > 1 else ""
            services.append((unit, load_state))
    return services


def get_service_status(service: str) -> str:
    """
    Retrieve the detailed status of a service.

    Parameters
    ----------
    service:
        The name of the service unit (e.g. ``ssh.service``).

    Returns
    -------
    str
        The raw output of ``systemctl status`` for the given service.

    Raises
    ------
    RuntimeError
        If the service does not exist or ``systemctl`` returns a non‑zero
        exit code.
    """
    result = _run_systemctl("status", service)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to get status for {service}: {result.stderr.strip()}")
    return result.stdout


def start_service(service: str) -> None:
    """
    Start a systemd service.

    Parameters
    ----------
    service:
        The name of the service unit to start.

    Raises
    ------
    RuntimeError
        If the service cannot be started.
    """
    result = _run_systemctl("start", service, capture_output=False)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to start {service}")


def stop_service(service: str) -> None:
    """
    Stop a systemd service.

    Parameters
    ----------
    service:
        The name of the service unit to stop.

    Raises
    ------
    RuntimeError
        If the service cannot be stopped.
    """
    result = _run_systemctl("stop", service, capture_output=False)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to stop {service}")


def restart_service(service: str) -> None:
    """
    Restart a systemd service.

    Parameters
    ----------
    service:
        The name of the service unit to restart.

    Raises
    ------
    RuntimeError
        If the service cannot be restarted.
    """
    result = _run_systemctl("restart", service, capture_output=False)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to restart {service}")


def enable_service(service: str) -> None:
    """
    Enable a service to start at boot.

    Parameters
    ----------
    service:
        The name of the service unit to enable.

    Raises
    ------
    RuntimeError
        If the service cannot be enabled.
    """
    result = _run_systemctl("enable", service, capture_output=False)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to enable {service}")


def disable_service(service: str) -> None:
    """
    Disable a service from starting at boot.

    Parameters
    ----------
    service:
        The name of the service unit to disable.

    Raises
    ------
    RuntimeError
        If the service cannot be disabled.
    """
    result = _run_systemctl("disable", service, capture_output=False)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to disable {service}")


__all__ = [
    "list_services",
    "get_service_status",
    "start_service",
    "stop_service",
    "restart_service",
    "enable_service",
    "disable_service",
]