"""
Cron and Scheduled Jobs Utilities.

This module provides simple helpers for constructing and parsing cron
schedule lines. The helpers are intentionally lightweight and avoid
external dependencies, making them suitable for inclusion in scripts
or educational material.

Typical usage::

    from projects.linux_foundations.notes.cron import build_cron_schedule, parse_cron_line

    # Build a cron line that runs a backup script every day at 2:30 AM
    line = build_cron_schedule(minute='30', hour='2',
                               day_of_month='*', month='*',
                               day_of_week='*',
                               command='/usr/local/bin/backup.sh')
    # line -> '30 2 * * * /usr/local/bin/backup.sh'

    # Parse an existing cron line
    info = parse_cron_line('0 0 * * 0 /usr/bin/weekly_report')
    # info -> {
    #     'minute': '0',
    #     'hour': '0',
    #     'day_of_month': '*',
    #     'month': '*',
    #     'day_of_week': '0',
    #     'command': '/usr/bin/weekly_report'
    # }
"""

from __future__ import annotations

from typing import Dict


def build_cron_schedule(
    minute: str = "*",
    hour: str = "*",
    day_of_month: str = "*",
    month: str = "*",
    day_of_week: str = "*",
    command: str = "",
) -> str:
    """
    Construct a cron schedule line from its components.

    Parameters
    ----------
    minute : str, optional
        Minute field (0‑59, ``*``, ``*/5`` etc.). Default ``"*"``
    hour : str, optional
        Hour field (0‑23). Default ``"*"``
    day_of_month : str, optional
        Day‑of‑month field (1‑31). Default ``"*"``
    month : str, optional
        Month field (1‑12). Default ``"*"``
    day_of_week : str, optional
        Day‑of‑week field (0‑7 where both 0 and 7 are Sunday). Default ``"*"``
    command : str, optional
        The command or script to execute. Empty string results in a schedule
        without a command.

    Returns
    -------
    str
        A single cron line suitable for inclusion in a crontab file.

    Notes
    -----
    The function does **not** perform exhaustive validation of the
    cron fields; it only ensures that each field is a non‑empty string.
    For production use, consider stricter validation.
    """
    # Basic sanity checks – ensure fields are provided as strings
    fields = [minute, hour, day_of_month, month, day_of_week]
    if not all(isinstance(f, str) and f for f in fields):
        raise ValueError("All time fields must be non‑empty strings.")
    if not isinstance(command, str):
        raise ValueError("Command must be a string.")

    schedule = " ".join(fields)
    if command:
        schedule = f"{schedule} {command}"
    return schedule


def parse_cron_line(line: str) -> Dict[str, str]:
    """
    Parse a single cron line into its constituent parts.

    Parameters
    ----------
    line : str
        A cron line as it would appear in a crontab file. The line may
        contain leading/trailing whitespace.

    Returns
    -------
    dict
        Mapping with keys ``minute``, ``hour``, ``day_of_month``,
        ``month``, ``day_of_week`` and ``command``. The ``command`` entry
        contains the remainder of the line after the five schedule fields,
        stripped of leading whitespace.

    Raises
    ------
    ValueError
        If the line does not contain at least six whitespace‑separated
        components (the five schedule fields plus a command).
    """
    if not isinstance(line, str):
        raise TypeError("Cron line must be a string.")
    parts = line.strip().split(None, 5)  # split on any whitespace, max 6 parts
    if len(parts) < 6:
        raise ValueError(
            "Cron line must contain at least five schedule fields and a command."
        )
    minute, hour, day_of_month, month, day_of_week, command = parts
    return {
        "minute": minute,
        "hour": hour,
        "day_of_month": day_of_month,
        "month": month,
        "day_of_week": day_of_week,
        "command": command,
    }