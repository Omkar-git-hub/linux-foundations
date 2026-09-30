"""
CPU and Memory monitoring utilities for Linux systems.

This module provides simple functions to retrieve CPU usage percentage and
memory statistics by parsing the ``/proc`` pseudo‑filesystem.  The implementation
relies only on the Python standard library and therefore works without any
external dependencies.

Typical usage::

    from projects.linux_foundations.monitoring import cpu_percent, memory_info

    # Get instantaneous CPU usage over a short interval
    usage = cpu_percent(interval=0.2)

    # Get memory statistics
    mem = memory_info()
    print(f"Total: {mem.total} kB, Used: {mem.used} kB, Free: {mem.free} kB, "
          f"Usage: {mem.percent:.2f}%")
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

_PROC_STAT = Path("/proc/stat")
_PROC_MEMINFO = Path("/proc/meminfo")


@dataclass(frozen=True)
class CpuTimes:
    """Snapshot of CPU time counters."""

    user: int
    nice: int
    system: int
    idle: int
    iowait: int
    irq: int
    softirq: int
    steal: int
    guest: int
    guest_nice: int

    @property
    def idle_all(self) -> int:
        """Total idle time (idle + iowait)."""
        return self.idle + self.iowait

    @property
    def non_idle(self) -> int:
        """Total non‑idle time."""
        return (
            self.user
            + self.nice
            + self.system
            + self.irq
            + self.softirq
            + self.steal
            + self.guest
            + self.guest_nice
        )

    @property
    def total(self) -> int:
        """Total time (idle + non‑idle)."""
        return self.idle_all + self.non_idle


def _read_cpu_times() -> CpuTimes:
    """
    Parse the first line of ``/proc/stat`` and return a :class:`CpuTimes` object.

    The function raises ``FileNotFoundError`` if the file does not exist,
    which is appropriate for non‑Linux platforms.
    """
    line = _PROC_STAT.read_text().splitlines()[0]
    parts = line.split()
    if parts[0] != "cpu":
        raise ValueError("Unexpected format in /proc/stat")
    # Convert the remaining fields to integers; missing fields default to 0.
    values = [int(v) for v in parts[1:]]
    # Pad the list to ensure we have exactly 10 entries.
    values += [0] * (10 - len(values))
    return CpuTimes(*values[:10])


def cpu_percent(interval: float = 0.1) -> float:
    """
    Return the CPU usage percentage over *interval* seconds.

    The calculation follows the algorithm used by ``top`` and ``psutil``:
    it measures the change in total and idle CPU time between two snapshots.

    Parameters
    ----------
    interval:
        Number of seconds to wait between the two measurements.  The default
        of ``0.1`` provides a quick, reasonably accurate estimate.

    Returns
    -------
    float
        CPU usage as a percentage of total time.
    """
    start = _read_cpu_times()
    time.sleep(interval)
    end = _read_cpu_times()

    total_diff = end.total - start.total
    idle_diff = end.idle_all - start.idle_all

    if total_diff == 0:
        return 0.0
    usage = (total_diff - idle_diff) / total_diff * 100.0
    return usage


@dataclass(frozen=True)
class MemoryInfo:
    """Memory statistics in kilobytes."""

    total: int
    free: int
    available: int
    used: int
    percent: float


def _parse_meminfo() -> dict[str, int]:
    """
    Parse ``/proc/meminfo`` into a dictionary mapping keys to integer values (kB).

    Only lines that contain a numeric value followed by ``kB`` are considered.
    """
    info: dict[str, int] = {}
    for line in _PROC_MEMINFO.read_text().splitlines():
        if ":" not in line:
            continue
        key, rest = line.split(":", 1)
        parts = rest.strip().split()
        if not parts:
            continue
        try:
            value = int(parts[0])
        except ValueError:
            continue
        info[key] = value
    return info


def memory_info() -> MemoryInfo:
    """
    Retrieve memory usage statistics.

    Returns
    -------
    MemoryInfo
        An immutable dataclass containing total, free, available, used memory
        (all in kilobytes) and the usage percentage.
    """
    mem = _parse_meminfo()
    total = mem.get("MemTotal", 0)
    free = mem.get("MemFree", 0)
    available = mem.get("MemAvailable", total - free)  # fallback if missing
    used = total - available
    percent = (used / total * 100.0) if total else 0.0
    return MemoryInfo(total=total, free=free, available=available, used=used, percent=percent)