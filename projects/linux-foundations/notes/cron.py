"""
Cron and Scheduled Jobs Notes

This module provides a concise reference for using `cron` to schedule
recurring tasks on Unix-like systems. The notes are intended for quick
look‑ups and can be used by the documentation generation utilities in
the project.

Typical usage:

    from projects.linux_foundations.notes.cron import get_cron_notes

    print(get_cron_notes())
"""

from __future__ import annotations

__all__: list[str] = ["get_cron_notes"]


def get_cron_notes() -> str:
    """
    Return a formatted string containing essential information about
    cron syntax, common patterns, and best practices.

    The returned string can be printed directly or written to a markdown
    file for documentation purposes.

    Returns
    -------
    str
        Multi‑line notes describing cron fields, special strings, environment
        considerations, and example entries.
    """
    notes = """# Cron and Scheduled Jobs

## Overview
`cron` is a time‑based job scheduler in Unix‑like operating systems.
It allows you to run commands or scripts automatically at specified
times, dates, or intervals.

## Crontab Format
A typical crontab line consists of six fields:

```
┌───────────── minute (0 - 59)
│ ┌─────────── hour (0 - 23)
│ │ ┌───────── day of month (1 - 31)
│ │ │ ┌─────── month (1 - 12)
│ │ │ │ ┌───── day of week (0 - 6) (Sunday=0)
│ │ │ │ │
* * * * * command-to-execute
```

- Use `*` to match any value.
- Multiple values can be specified with commas (e.g., `1,15,30`).
- Ranges are expressed with a hyphen (e.g., `9-17`).
- Step values use a slash (e.g., `*/5` for every five units).

## Special Strings
| String | Meaning                              |
|--------|--------------------------------------|
| `@reboot` | Run once at system startup          |
| `@yearly` / `@annually` | Run once a year at midnight on Jan 1 |
| `@monthly` | Run once a month at midnight on the 1st |
| `@weekly` | Run once a week at midnight on Sunday |
| `@daily` / `@midnight` | Run once a day at midnight |
| `@hourly` | Run once an hour at the start of the hour |

## Environment
- The default shell is `/bin/sh`. Override with `SHELL=/bin/bash` at the top of the crontab.
- Define environment variables (e.g., `PATH`, `HOME`) before the schedule lines.
- Redirect output to avoid unwanted emails:
  ```sh
  * * * * * /path/to/script.sh >> /var/log/script.log 2>&1
  ```

## Common Examples
```
# Run a backup script every day at 02:30
30 2 * * * /usr/local/bin/backup.sh

# Clean /tmp every hour
0 * * * * /usr/bin/find /tmp -type f -atime +1 -delete

# Restart a service at reboot
@reboot /usr/sbin/service myservice start
```

## Tips & Best Practices
- Test commands manually before adding them to crontab.
- Use absolute paths for binaries and files.
- Keep crontab entries minimal; delegate complex logic to scripts.
- Check the system’s cron log (`/var/log/cron` or `journalctl -u cron`) for troubleshooting.

## Managing Crontabs
- Edit the current user's crontab: `crontab -e`
- List crontab entries: `crontab -l`
- Remove crontab: `crontab -r`
- System‑wide crontabs are located in `/etc/crontab` and `/etc/cron.d/`.

"""
    return notes