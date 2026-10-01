"""
Linux Foundations Notes Package

Exports note modules for easy access.
"""

from .linux import get_notes as linux_notes
from .github_actions import get_notes as github_actions_notes

__all__ = [
    "linux_notes",
    "github_actions_notes",
]