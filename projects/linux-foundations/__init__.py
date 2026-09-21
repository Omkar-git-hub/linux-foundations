"""
Top‑level package for the *linux‑foundations* project.

Exports the public helpers for file searching and text grepping.
"""

from .search import find_files, grep_in_file, grep_in_dir

__all__ = ["find_files", "grep_in_file", "grep_in_dir"]