"""
Linux Foundations package.

Exports the public file‑handling utilities for convenient import:

    from projects.linux_foundations import list_files, read_file, write_file
"""

from .files import (
    ensure_dir_exists,
    list_files,
    read_file,
    write_file,
)

__all__ = [
    "ensure_dir_exists",
    "list_files",
    "read_file",
    "write_file",
]