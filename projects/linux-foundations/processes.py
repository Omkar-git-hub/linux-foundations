"""
Utility functions for inspecting Linux processes.

The module provides a small, pure‑standard‑library API to enumerate
processes on a Linux system by reading the ``/proc`` pseudo‑filesystem.
It deliberately avoids external dependencies (e.g. ``psutil``) to keep
the package lightweight and portable across typical Linux environments.

Typical usage
-------------

>>> from projects.linux-foundations.processes import list_processes
>>> procs = list_processes()
>>> len(procs)  # doctest: +SKIP
42
>>> procs[0]   # doctest: +SKIP
{'pid': 1, 'name': 'systemd', 'state': 'S'}

Only processes that the current user can read are returned; permission
errors are silently ignored.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Dict


def _read_first_line(path: Path) -> str | None:
    """Return the first line of *path* stripped of whitespace, or ``None`` on error."""
    try:
        with path.open("r", encoding="utf-8") as f:
            return f.readline().strip()
    except (OSError, PermissionError):
        return None


def _parse_status(state_line: str) -> str:
    """
    Extract the process state character from a line like ``State:\tS (sleeping)``.
    Returns the single‑letter state (e.g. ``S``). If parsing fails, returns an empty string.
    """
    parts = state_line.split()
    if len(parts) >= 2:
        return parts[1]
    return ""


def list_processes() -> List[Dict[str, str]]:
    """
    Enumerate processes visible through ``/proc``.

    Returns
    -------
    List[Dict[str, str]]
        A list where each element is a mapping with the keys:

        * ``pid``   – the process identifier as a string.
        * ``name``  – the executable name (from ``/proc/<pid>/comm``).
        * ``state`` – the single‑letter process state (e.g. ``R``, ``S``, ``Z``).

    The function skips entries that cannot be accessed due to permission
    restrictions or that do not conform to the expected ``/proc`` layout.
    """
    proc_root = Path("/proc")
    processes: List[Dict[str, str]] = []

    if not proc_root.is_dir():
        # Not a Linux environment; return empty list rather than raising.
        return processes

    for entry in proc_root.iterdir():
        if not entry.is_dir():
            continue
        if not entry.name.isdigit():
            continue

        pid = entry.name
        comm_path = entry / "comm"
        status_path = entry / "status"

        name = _read_first_line(comm_path)
        if name is None:
            continue

        state_line = _read_first_line(status_path)
        if state_line is None:
            continue
        state = _parse_status(state_line)

        processes.append({"pid": pid, "name": name, "state": state})

    return processes


__all__ = ["list_processes"]