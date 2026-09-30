"""
Scheduled Jobs Notes

Provides a high‑level overview of different scheduling mechanisms
available on Linux, including `cron`, `systemd timers`, and `at`.
The module supplies a helper function that returns the documentation
as a formatted string.
"""

from __future__ import annotations

__all__: list[str] = ["get_scheduled_jobs_notes"]


def get_scheduled_jobs_notes() -> str:
    """
    Return a formatted string that summarises various Linux scheduling
    utilities beyond traditional cron.

    Returns
    -------
    str
        Multi‑line notes covering `at`, `systemd timers`, and best‑practice
        recommendations for choosing the appropriate scheduler.
    """
    notes = """# Scheduled Jobs Overview

Linux offers several tools to run tasks automatically:

## 1. cron
- Time‑based, minute‑level granularity.
- Simple syntax, widely supported.
- Ideal for recurring jobs.

## 2. at
- One‑off execution at a specific future time.
- Syntax: `echo "command" | at 14:30` or `at now + 2 hours`.
- Good for ad‑hoc tasks.

## 3. systemd timers
- Integrated with `systemd` service manager.
- Supports calendar events, monotonic timers, and boot‑time triggers.
- Provides richer dependency handling and logging via `journalctl`.

### Example systemd timer
```
# /etc/systemd/system/backup.timer
[Unit]
Description=Run backup daily

[Timer]
OnCalendar=*-*-* 02:30:00
Persistent=true

[Install]
WantedBy=timers.target
```

Corresponding service (`backup.service`) runs the actual script.

## Choosing the Right Scheduler
| Use‑case                     | Recommended tool |
|------------------------------|------------------|
| Simple recurring jobs       | cron |
| One‑off delayed execution   | at |
| Complex dependencies, logging, or need for start‑stop semantics | systemd timer |
| Need to run after boot but before user login | `@reboot` in cron or `OnBootSec=` in systemd timer |

## Managing Systemd Timers
- Enable & start: `systemctl enable --now backup.timer`
- List timers: `systemctl list-timers`
- View logs: `journalctl -u backup.service`

## Best Practices
- Prefer absolute paths.
- Keep scripts idempotent.
- Use `systemd` for services that already have a unit file.
- Document each timer in `/etc/systemd/system/` with a clear description.

"""
    return notes