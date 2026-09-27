"""
Shell control utilities for handling command line parsing and quoting.

This module provides two primary helpers:

* ``split_command`` – Split a shell command string into a list of arguments,
  respecting POSIX quoting rules. It is a thin wrapper around :func:`shlex.split`
  with ``posix=True`` and ``punctuation_chars=False`` to ensure consistent
  behaviour across Python versions.

* ``quote_argument`` – Return a shell‑escaped version of a single argument.
  It uses :func:`shlex.quote` which adds single quotes when necessary and
  escapes existing single quotes safely.

Both helpers are deliberately small and have no external dependencies,
making them suitable for inclusion in the public API of the
``linux_foundations`` package.
"""

from __future__ import annotations

import shlex
from typing import List


def split_command(command: str) -> List[str]:
    """
    Split a command line string into a list of arguments using POSIX rules.

    Parameters
    ----------
    command: str
        The raw command line as entered in a shell.

    Returns
    -------
    List[str]
        A list of arguments with quoting and escaping processed.

    Examples
    --------
    >>> split_command('git commit -m "Initial commit"')
    ['git', 'commit', '-m', 'Initial commit']

    >>> split_command("echo 'It\\'s a test'")
    ['echo', "It's a test"]
    """
    # ``shlex.split`` already implements the required behaviour.
    # ``posix=True`` enables POSIX‑compatible parsing (default).
    # ``punctuation_chars=False`` disables treating punctuation as separate tokens,
    # matching typical shell behaviour.
    return shlex.split(command, posix=True, punctuation_chars=False)


def quote_argument(arg: str) -> str:
    """
    Return a shell‑escaped version of *arg* suitable for inclusion in a command line.

    Parameters
    ----------
    arg: str
        The argument to be quoted.

    Returns
    -------
    str
        The quoted argument.

    Examples
    --------
    >>> quote_argument('simple')
    'simple'
    >>> quote_argument('needs quoting')
    "'needs quoting'"
    >>> quote_argument("it's tricky")
    "'it'\"'\"'s tricky'"
    """
    return shlex.quote(arg)