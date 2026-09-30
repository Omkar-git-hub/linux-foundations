"""
Linux Logs Notes

This module provides a concise reference about Linux logging facilities,
including traditional log files, the systemd journal, and common tools for
viewing and managing logs.

The content is stored in the ``LOGS_NOTES`` constant as a multiline string,
so it can be easily imported and displayed by other parts of the package or
used in documentation generation.
"""

LOGS_NOTES = """\
# Linux Logging Overview

Linux systems generate a variety of logs that record system events,
application output, security information, and more. Understanding where
these logs are stored and how to access them is essential for troubleshooting
and system administration.

## Traditional Log Files

- **Location:** `/var/log/`
- **Common files:**
  - `syslog` – General system messages (Debian/Ubuntu).
  - `messages` – General system messages (RHEL/CentOS/Fedora).
  - `auth.log` – Authentication and security-related messages.
  - `kern.log` – Kernel messages.
  - `dmesg` – Kernel ring buffer (also accessible via the `dmesg` command).
  - `boot.log` – Boot process messages.
  - `apt/` – Package manager logs (Debian/Ubuntu).
  - `yum.log` – Package manager logs (RHEL/CentOS).

### Viewing Log Files

```bash
# Show the last 20 lines and follow new entries
tail -f /var/log/syslog

# Paginated view
less /var/log/auth.log

# Search for a pattern
grep -i "error" /var/log/kern.log
```

## Systemd Journal

Modern Linux distributions using `systemd` store logs in a binary journal
instead of plain text files.

- **Command:** `journalctl`
- **Location:** `/run/log/journal/` (volatile) or `/var/log/journal/` (persistent).

### Basic journalctl Usage

```bash
# Show all logs (paged)
journalctl

# Show logs from the current boot
journalctl -b

# Follow new log entries (like tail -f)
journalctl -f

# Filter by unit (service)
journalctl -u nginx.service

# Filter by priority (0..7, where 0 = emerg, 3 = err, 6 = info)
journalctl -p err

# Show logs for a specific time range
journalctl --since "2024-09-01 00:00:00" --until "2024-09-01 23:59:59"
```

### Managing the Journal

- **Disk usage:** `journalctl --disk-usage`
- **Vacuum old entries:** `journalctl --vacuum-time=2weeks`
- **Limit size:** `journalctl --vacuum-size=500M`

## Log Rotation

Traditional log files are rotated by `logrotate`, typically configured in
`/etc/logrotate.conf` and `/etc/logrotate.d/`. Rotation prevents logs from
growing indefinitely.

Key directives in a logrotate configuration:

- `weekly`, `daily`, `monthly` – Rotation frequency.
- `rotate N` – Keep the last N rotated logs.
- `compress` – Compress old logs (usually with gzip).
- `missingok` – Do not error if the log file is missing.
- `notifempty` – Skip rotation if the log is empty.
- `create mode owner group` – Create a new empty log file after rotation.

Example snippet (`/etc/logrotate.d/nginx`):

```
/var/log/nginx/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data adm
    sharedscripts
    postrotate
        [ -f /run/nginx.pid ] && kill -USR1 `cat /run/nginx.pid`
    endscript
}
```

## Common Log Analysis Tools

- **`grep`, `awk`, `sed`** – Text processing for traditional logs.
- **`journalctl`** – Powerful filtering for the systemd journal.
- **`logwatch`** – Summarizes log activity and sends daily reports.
- **`goaccess`** – Real‑time web log analyzer (e.g., for Apache/Nginx).
- **`rsyslog` / `syslog-ng`** – Centralized log collection and forwarding.

## Security Considerations

- Protect log files with appropriate permissions (usually `640` or `600`).
- Store logs on a separate partition or remote server to prevent tampering.
- Use `auditd` for detailed security auditing; logs are in `/var/log/audit/`.

## Quick Reference Cheat Sheet

| Task                              | Command |
|-----------------------------------|---------|
| View recent syslog entries        | `tail -f /var/log/syslog` |
| Follow systemd journal            | `journalctl -f` |
| Show logs from previous boot      | `journalctl -b -1` |
| Filter by service (e.g., sshd)    | `journalctl -u sshd` |
| Show only error‑level messages    | `journalctl -p err` |
| Rotate logs manually (logrotate)  | `logrotate -f /etc/logrotate.conf` |
| Check journal disk usage          | `journalctl --disk-usage` |
| Delete journal entries > 30 days  | `journalctl --vacuum-time=30d` |

These notes give a high‑level overview; consult the man pages (`man journalctl`,
`man logrotate`, `man rsyslog.conf`) for detailed options and configuration
examples.
"""

__all__ = ["LOGS_NOTES"]