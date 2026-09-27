"""
Top‑level package for the *linux_foundations* collection.

The package aggregates a variety of utilities that illustrate fundamental
Linux concepts.  Sub‑modules are imported lazily to keep import time low.
"""

# Export the most commonly used helpers at the package level for convenience.
from .shell_control import split_command, quote_argument

__all__ = [
    "split_command",
    "quote_argument",
]