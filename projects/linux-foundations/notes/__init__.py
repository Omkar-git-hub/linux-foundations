"""
Convenient imports for the ``projects.linux_foundations.notes`` package.
"""

from .troubleshooting import (
    check_service_status,
    get_last_boot_time,
    parse_dmesg_errors,
    list_open_ports,
    recent_syslog_entries,
)

__all__ = [
    "check_service_status",
    "get_last_boot_time",
    "parse_dmesg_errors",
    "list_open_ports",
    "recent_syslog_entries",
]