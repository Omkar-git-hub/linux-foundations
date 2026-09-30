"""
Linux Logs utilities.

This module provides helper functions for reading and filtering typical
Linux syslog files (e.g., /var/log/syslog, /var/log/auth.log).  The
implementation is deliberately lightweight and relies only on the Python
standard library.

Public API
----------

- ``read_log(path)`` – Return a list of raw log lines.
- ``tail_log(path, n=10)`` – Return the last *n* lines of a log file.
- ``parse_syslog_line(line)`` – Parse a single syslog line into a dictionary.
- ``filter_by_level(lines, level)`` – Keep only lines that contain the given
  log level (e.g., ``\"ERROR\"`` or ``\"WARNING\"``).
- ``filter_by_time_range(lines, start, end)`` – Keep only lines whose timestamps
  fall between *start* and *end* (both ``datetime`` objects, inclusive).
- ``get_entries_by_level(path, level)`` – Convenience wrapper that reads a file
  and returns entries matching *level*.
- ``get_entries_by_time_range(path, start, end)`` – Convenience wrapper that
  reads a file and returns entries whose timestamps are within the given range.
"""

from __future__ import annotations

import datetime
import re
from pathlib import Path
from typing import Iterable, List, Mapping, Optional

__all__ = [
    "read_log",
    "tail_log",
    "parse_syslog_line",
    "filter_by_level",
    "filter_by_time_range",
    "get_entries_by_level",
    "get_entries_by_time_range",
]

# Regular expression for a typical syslog line:
#   "Oct 11 22:14:15 hostname process[pid]: message"
_SYSLOG_REGEX = re.compile(
    r"""^(?P<month>\w{3})\s+               # Month abbreviation
        (?P<day>\d{1,2})\s+                # Day of month
        (?P<time>\d{2}:\d{2}:\d{2})\s+     # HH:MM:SS
        (?P<host>\S+)\s+                   # Hostname
        (?P<proc>[\w\-/]+)(?:\[(?P<pid>\d+)\])?:\s   # Process name and optional pid
        (?P<msg>.*)$""",
    re.VERBOSE,
)

_MONTH_MAP = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}


def read_log(path: str | Path) -> List[str]:
    """
    Read a log file and return a list of its lines (including the trailing newline).

    Parameters
    ----------
    path: str or Path
        Path to the log file.

    Returns
    -------
    List[str]
        All lines from the file.
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"Log file not found: {path}")
    return p.read_text(encoding="utf-8").splitlines(keepends=True)


def tail_log(path: str | Path, n: int = 10) -> List[str]:
    """
    Return the last *n* lines of a log file.

    Parameters
    ----------
    path: str or Path
        Path to the log file.
    n: int, default 10
        Number of lines to return.

    Returns
    -------
    List[str]
        The last *n* lines (including newline characters).
    """
    lines = read_log(path)
    return lines[-n:] if n > 0 else []


def _build_timestamp(month: str, day: str, time_str: str) -> datetime.datetime:
    """
    Build a ``datetime`` object from month, day and HH:MM:SS components.
    The year is assumed to be the current year; if the resulting timestamp
    is in the future (possible for logs from Dec 31 crossing New Year),
    the year is rolled back by one.
    """
    now = datetime.datetime.now()
    month_num = _MONTH_MAP[month]
    hour, minute, second = map(int, time_str.split(":"))
    dt = datetime.datetime(
        year=now.year,
        month=month_num,
        day=int(day),
        hour=hour,
        minute=minute,
        second=second,
    )
    # Adjust for year rollover
    if dt > now:
        dt = dt.replace(year=now.year - 1)
    return dt


def parse_syslog_line(line: str) -> Optional[Mapping[str, object]]:
    """
    Parse a single syslog line.

    The function extracts the timestamp, hostname, process name, optional pid,
    and the raw message.  If the line does not match the expected format,
    ``None`` is returned.

    Parameters
    ----------
    line: str
        A raw line from a syslog file (newline stripped is fine).

    Returns
    -------
    dict or None
        Mapping with keys ``timestamp`` (datetime), ``host``, ``process``,
        ``pid`` (int or None), ``message`` (str).  Returns ``None`` for unparsable
        lines.
    """
    match = _SYSLOG_REGEX.match(line.rstrip("\n"))
    if not match:
        return None

    month = match.group("month")
    day = match.group("day")
    time_str = match.group("time")
    timestamp = _build_timestamp(month, day, time_str)

    host = match.group("host")
    process = match.group("proc")
    pid_str = match.group("pid")
    pid = int(pid_str) if pid_str else None
    message = match.group("msg")

    return {
        "timestamp": timestamp,
        "host": host,
        "process": process,
        "pid": pid,
        "message": message,
    }


def filter_by_level(lines: Iterable[str], level: str) -> List[str]:
    """
    Filter log lines that contain a specific log level.

    The check is case‑insensitive and looks for the level as a whole word
    (e.g., ``\"ERROR\"`` matches ``\"ERROR:\"`` or ``\"[ERROR]\"``).

    Parameters
    ----------
    lines: iterable of str
        Log lines to filter.
    level: str
        Desired log level (e.g., ``\"ERROR\"``).

    Returns
    -------
    List[str]
        Lines that contain the requested level.
    """
    pattern = re.compile(rf"\b{re.escape(level)}\b", re.IGNORECASE)
    return [ln for ln in lines if pattern.search(ln)]


def filter_by_time_range(
    lines: Iterable[str],
    start: datetime.datetime,
    end: datetime.datetime,
) -> List[str]:
    """
    Keep only lines whose timestamps fall within the inclusive range
    ``[start, end]``.

    Lines that cannot be parsed are ignored.

    Parameters
    ----------
    lines: iterable of str
        Log lines to filter.
    start: datetime
        Start of the interval (inclusive).
    end: datetime
        End of the interval (inclusive).

    Returns
    -------
    List[str]
        Lines whose timestamps are within the range.
    """
    filtered: List[str] = []
    for ln in lines:
        parsed = parse_syslog_line(ln)
        if not parsed:
            continue
        ts: datetime.datetime = parsed["timestamp"]  # type: ignore[assignment]
        if start <= ts <= end:
            filtered.append(ln)
    return filtered


def get_entries_by_level(path: str | Path, level: str) -> List[str]:
    """
    Convenience wrapper that reads a log file and returns entries matching *level*.

    Parameters
    ----------
    path: str or Path
        Path to the log file.
    level: str
        Desired log level.

    Returns
    -------
    List[str]
        Matching log lines.
    """
    return filter_by_level(read_log(path), level)


def get_entries_by_time_range(
    path: str | Path,
    start: datetime.datetime,
    end: datetime.datetime,
) -> List[str]:
    """
    Convenience wrapper that reads a log file and returns entries whose timestamps
    lie within the given range.

    Parameters
    ----------
    path: str or Path
        Path to the log file.
    start: datetime
        Start datetime (inclusive).
    end: datetime
        End datetime (inclusive).

    Returns
    -------
    List[str]
        Matching log lines.
    """
    return filter_by_time_range(read_log(path), start, end)