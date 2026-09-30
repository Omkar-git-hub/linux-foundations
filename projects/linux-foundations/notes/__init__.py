"""
Initialization for the notes package.

Exports the most commonly used note‑retrieval functions so that they
can be imported directly from `projects.linux_foundations.notes`.
"""

from .cron import get_cron_notes
from .scheduled_jobs import get_scheduled_jobs_notes

__all__: list[str] = [
    "get_cron_notes",
    "get_scheduled_jobs_notes",
]