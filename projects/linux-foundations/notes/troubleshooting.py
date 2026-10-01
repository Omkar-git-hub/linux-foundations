"""
Linux Troubleshooting Notes.

This module provides a small collection of helper utilities that can be
used while troubleshooting a Linux system.  The functions are deliberately
light‑weight and rely only on the Python standard library, making them safe
to import in any environment.

Typical usage::

    from projects.linux_foundations.notes.troubleshooting import (
        check_service_status,
        get_last_boot_time,
        parse_dmesg_errors,
    )

    if not check_service_status("ssh"):
        print("SSH service is not running")

    print("Last boot:", get_last_boot_time())

    for line in parse_dmesg_errors():
        print("Kernel error:", line)

All helpers raise :class:`RuntimeError` when the underlying system command
cannot be executed.  The functions return plain Python data structures
(strings, ``datetime`` objects, or iterables) that are easy to test.
"""

from __future__ import annotations

import subprocess
import datetime
import shlex
from typing import Iterable, List


def _run_command(command: str) -> str:
    """
    Execute *command* in a subprocess and return its stdout as a string.

    The command is executed with ``shell=False`` for safety; the string is
    split using :func:`shlex.split`.  If the command exits with a non‑zero
    status, a :class:`RuntimeError` is raised containing the stderr output.

    Parameters
    ----------
    command:
        The command line to execute.

    Returns
    -------
    str
        The captured standard output.

    Raises
    ------
    RuntimeError
        If the command cannot be executed or returns a non‑zero exit code.
    """
    args = shlex.split(command)
    try:
        completed = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            text=True,
        )
    except OSError as exc:
        raise RuntimeError(f"Failed to execute command {command!r}: {exc}") from exc

    if completed.returncode != 0:
        raise RuntimeError(
            f"Command {command!r} failed with exit code {completed.returncode}: "
            f"{completed.stderr.strip()}"
        )
    return completed.stdout.strip()


def check_service_status(service_name: str) -> bool:
    """
    Return ``True`` if the given *service_name* is active according to
    ``systemctl is-active``; otherwise ``False``.

    The function does **not** raise an exception for a non‑running service;
    it only raises if the ``systemctl`` command itself cannot be executed.

    Parameters
    ----------
    service_name:
        Name of the systemd service (e.g. ``"ssh"`` or ``"nginx.service"``).

    Returns
    -------
    bool
        ``True`` if the service is active, ``False`` otherwise.
    """
    try:
        output = _run_command(f"systemctl is-active {service_name}")
        return output == "active"
    except RuntimeError as exc:
        # If systemctl reports "inactive" or "failed" it returns a non‑zero
        # exit code, which we translate to ``False``.
        if "inactive" in str(exc).lower() or "failed" in str(exc).lower():
            return False
        raise


def get_last_boot_time() -> datetime.datetime:
    """
    Retrieve the timestamp of the last system boot.

    The implementation uses the ``who -b`` command, parses the output and
    returns a timezone‑naive :class:`datetime.datetime` object representing
    the boot time in the local timezone.

    Returns
    -------
    datetime.datetime
        The datetime of the most recent boot.

    Raises
    ------
    RuntimeError
        If the ``who`` command cannot be executed or its output cannot be
        parsed.
    """
    output = _run_command("who -b")
    # Example output: "         system boot  2024-09-30 14:22"
    parts = output.split()
    if len(parts) < 4:
        raise RuntimeError(f"Unexpected output from 'who -b': {output!r}")

    date_str = parts[-2]
    time_str = parts[-1]
    try:
        boot_dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    except ValueError as exc:
        raise RuntimeError(f"Failed to parse boot time '{date_str} {time_str}': {exc}") from exc
    return boot_dt


def parse_dmesg_errors() -> List[str]:
    """
    Scan the kernel ring buffer (``dmesg``) for lines that contain the word
    ``error`` (case‑insensitive) and return them as a list.

    This helper is useful for quickly locating kernel‑level problems.

    Returns
    -------
    list[str]
        All matching lines from ``dmesg``.  The list may be empty if no
        error lines are found.

    Raises
    ------
    RuntimeError
        If the ``dmesg`` command cannot be executed.
    """
    output = _run_command("dmesg")
    error_lines: List[str] = [
        line for line in output.splitlines() if "error" in line.lower()
    ]
    return error_lines


def list_open_ports() -> List[int]:
    """
    Return a list of TCP ports that are currently listening on the host.

    The implementation uses ``ss -tln`` which is widely available on modern
    Linux distributions.  Each line is parsed to extract the local port
    number.

    Returns
    -------
    list[int]
        A list of listening TCP port numbers.  The list may be empty.

    Raises
    ------
    RuntimeError
        If the ``ss`` command cannot be executed or its output cannot be
        parsed.
    """
    output = _run_command("ss -tln")
    ports: List[int] = []
    for line in output.splitlines():
        # Skip the header line(s) that start with "State"
        if line.startswith("State") or line.startswith("Netid"):
            continue
        parts = line.split()
        if len(parts) < 5:
            continue
        # The local address column is usually the 4th element
        local_addr = parts[4]
        # Format can be "[::]:22" or "0.0.0.0:80"
        if ":" not in local_addr:
            continue
        try:
            port_str = local_addr.rsplit(":", 1)[1]
            ports.append(int(port_str))
        except ValueError:
            continue
    return ports


def recent_syslog_entries(lines: int = 20) -> List[str]:
    """
    Retrieve the most recent *lines* entries from the system log.

    The function prefers ``journalctl -n <lines>`` when available; if that
    fails it falls back to reading ``/var/log/syslog`` (or ``/var/log/messages``
    on distributions that use that file).

    Parameters
    ----------
    lines:
        Number of recent log lines to return.

    Returns
    -------
    list[str]
        The requested log lines, newest first.

    Raises
    ------
    RuntimeError
        If neither ``journalctl`` nor a syslog file can be accessed.
    """
    try:
        output = _run_command(f"journalctl -n {lines} --no-pager")
        return output.splitlines()
    except RuntimeError:
        # Fallback to plain text log files
        for path in ("/var/log/syslog", "/var/log/messages"):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    all_lines = f.readlines()
                return [ln.rstrip("\n") for ln in all_lines[-lines:]][::-1]
            except OSError:
                continue
        raise RuntimeError("Unable to retrieve recent syslog entries")


__all__ = [
    "check_service_status",
    "get_last_boot_time",
    "parse_dmesg_errors",
    "list_open_ports",
    "recent_syslog_entries",
]