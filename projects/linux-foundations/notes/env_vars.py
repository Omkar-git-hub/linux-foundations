"""
Environment Variables Notes

This module demonstrates common operations with environment variables
using the standard library ``os`` module. It provides a small, well‑
documented API that can be used in tutorials, scripts, or as reference
implementations in other parts of the project.

Functions
---------
- ``get_env_var(name, default=None)`` – Retrieve the value of an
  environment variable, optionally returning a default.
- ``set_env_var(name, value)`` – Set or update an environment variable.
- ``delete_env_var(name)`` – Remove an environment variable if it exists.
- ``list_env_vars()`` – Return a snapshot of the current environment as a
  dictionary.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional


def get_env_var(name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Return the value of the environment variable ``name``.

    Parameters
    ----------
    name: str
        The name of the environment variable to look up.
    default: Optional[str], default ``None``
        Value to return if the variable is not present.

    Returns
    -------
    Optional[str]
        The variable's value or ``default`` when the variable is missing.
    """
    return os.getenv(name, default)


def set_env_var(name: str, value: str) -> None:
    """
    Set or update the environment variable ``name`` with ``value``.

    This operation modifies the process's environment only; it does not
    persist changes to the parent shell.

    Parameters
    ----------
    name: str
        The environment variable name.
    value: str
        The value to assign.
    """
    os.environ[name] = value


def delete_env_var(name: str) -> None:
    """
    Remove the environment variable ``name`` if it exists.

    Parameters
    ----------
    name: str
        The name of the variable to delete.
    """
    os.environ.pop(name, None)


def list_env_vars() -> Dict[str, str]:
    """
    Return a copy of the current environment variables.

    Returns
    -------
    Dict[str, str]
        A dictionary mapping variable names to their string values.
    """
    # ``os.environ`` behaves like a mutable mapping; copying it prevents
    # accidental modifications to the live environment.
    return dict(os.environ)


__all__: list[str] = [
    "get_env_var",
    "set_env_var",
    "delete_env_var",
    "list_env_vars",
]