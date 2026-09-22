"""
Top‑level package for the *linux‑foundations* educational modules.

The ``text_processing`` module provides simple, pure‑Python equivalents of
common Linux command‑line utilities.  It is imported here for convenient
access:

    from projects.linux_foundations import text_processing
"""

from . import text_processing  # noqa: F401

# Export the public symbols of the submodule at the package level for
# backward compatibility with earlier exercises.
from .text_processing import (
    count_lines,
    count_words,
    count_characters,
    grep,
    replace,
    cut_columns,
    sort_lines,
)

__all__ = [
    "count_lines",
    "count_words",
    "count_characters",
    "grep",
    "replace",
    "cut_columns",
    "sort_lines",
    "text_processing",
]