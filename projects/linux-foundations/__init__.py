"""
Top‑level package for the *linux‑foundations* project.

Exports a curated public API for convenience.
"""

from .links import (
    create_symlink,
    create_hardlink,
    is_symlink,
    is_hardlink,
    get_link_target,
    get_hardlink_count,
)

__all__ = [
    "create_symlink",
    "create_hardlink",
    "is_symlink",
    "is_hardlink",
    "get_link_target",
    "get_hardlink_count",
]