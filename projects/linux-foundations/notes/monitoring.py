"""
CPU and Memory Monitoring Notes

This module provides a concise reference for common Linux commands and
techniques used to monitor CPU and memory usage. The notes are intended
to be displayed as plain text, for example in a CLI help command or
documentation generator.
"""

from __future__ import annotations


def get_cpu_memory_notes() -> str:
    """
    Return a formatted string containing notes on CPU and memory monitoring.

    The string includes sections for CPU monitoring, memory monitoring,
    common one‑liners, and practical tips.

    Returns
    -------
    str
        Multiline notes ready for display.
    """
    notes = """
CPU Monitoring:
- top: Interactive process viewer showing CPU usage per process.
- htop: Enhanced version of top with color and mouse support (installable via package manager).
- mpstat (sysstat package): Per‑CPU statistics; e.g. ``mpstat -P ALL 1``.
- pidstat: Per‑process CPU usage; e.g. ``pidstat -u 1``.
- vmstat: System‑wide performance metrics, including CPU idle time.
- iostat: CPU utilization combined with I/O statistics.
- sar: Collects and reports historical CPU activity; configure via ``sar -u 1 3``.

Memory Monitoring:
- free: Quick overview of total, used, and free memory; ``free -h`` for human‑readable.
- vmstat: Shows memory, swap, and paging activity.
- top/htop: Displays memory usage per process alongside CPU.
- smem (optional): Reports memory usage with shared memory accounted.
- pmap <pid>: Detailed memory map of a specific process.
- cat /proc/meminfo: Raw kernel memory information.

Common One‑liners:
- Top CPU consumers: ``ps aux --sort=-%cpu | head``.
- Top memory consumers: ``ps aux --sort=-%mem | head``.
- Refresh memory info every second: ``watch -n 1 cat /proc/meminfo``.
- Combined CPU, disk, and network stats: ``dstat -c -d -n``.

Practical Tips:
- Adjust process priority with ``nice`` and ``renice`` to influence CPU scheduling.
- Use cgroups or systemd resource limits to cap CPU or memory for services.
- For long‑term monitoring, enable ``sar`` (sysstat) or tools like ``collectd``/``prometheus``.
- When troubleshooting, correlate CPU spikes with I/O wait (``iowait``) from vmstat or iostat.
"""
    return notes.strip()