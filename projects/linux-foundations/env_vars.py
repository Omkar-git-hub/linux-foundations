"""
Utility functions for working with environment variables.

This module provides a small, well‑typed wrapper around ``os.environ`` that
makes common operations explicit and testable:

* ``get_env`` – Retrieve a variable with an optional default.
* ``set_env`` – Set or update a variable.
* ``delete_env`` – Remove a variable from the environment.
* ``list_env`` – Return a snapshot of the current environment mapping.

All functions operate on the process‑wide environment and therefore affect
sub‑processes spawned after the call.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

__all__ = [
    "get_env",
    "set_env",
    "delete_env",
    "list_env",
]


def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Return the value of the environment variable ``name`` if it exists,
    otherwise return ``default``.

    Parameters
    ----------
    name:
        The environment variable name.
    default:
        Value to return when ``name`` is not present. If omitted, ``None`` is
        returned.

    Returns
    -------
    Optional[str]
        The variable's value or ``default``.
    """
    return os.environ.get(name, default)


def set_env(name: str, value: str) -> None:
    """
    Set the environment variable ``name`` to ``value``.

    If the variable already exists its value is overwritten.

    Parameters
    ----------
    name:
        The environment variable name.
    value:
        The value to assign.
    """
    os.environ[name] = value


def delete_env(name: str) -> None:
    """
    Remove ``name`` from the environment.

    Raises
    ------
    KeyError
        If ``name`` is not present in the environment.
    """
    del os.environ[name]


def list_env() -> Dict[str, str]:
    """
    Return a shallow copy of the current environment mapping.

    The returned dictionary can be inspected or modified without affecting the
    actual process environment.

    Returns
    -------
    dict[str, str]
        A copy of ``os.environ``.
    """
    # ``os.environ`` behaves like a mutable mapping; converting it to ``dict``
    # gives us an independent snapshot.
    return dict(os.environ)