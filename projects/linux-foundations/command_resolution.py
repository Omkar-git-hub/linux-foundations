"""
Utility for resolving a command name to an absolute executable path using the
system ``PATH`` environment variable.

The implementation mirrors the behaviour of the Unix ``which`` command:
the first matching executable found in the directories listed in ``PATH`` is
returned. If no executable is found, ``None`` is returned.

Typical usage::

    from projects.linux_foundations.command_resolution import resolve_command

    path = resolve_command("python")
    if path:
        print(f"Executable found at: {path}")
    else:
        print("Command not found in PATH")
"""

from __future__ import annotations

import os
from typing import Optional


def resolve_command(command: str) -> Optional[str]:
    """
    Resolve *command* to an absolute path of an executable found in ``PATH``.

    Parameters
    ----------
    command:
        The name of the command to resolve. It may be a simple filename
        (e.g. ``"ls"``) or a relative/absolute path. If *command* already
        contains a directory separator, it is treated as a direct path and
        validated for executability.

    Returns
    -------
    Optional[str]
        The absolute path to the executable if found, otherwise ``None``.
    """
    if not command:
        return None

    # If the command already contains a path separator, treat it as a direct path.
    if os.path.sep in command or (os.path.altsep and os.path.altsep in command):
        abs_path = os.path.abspath(command)
        if os.path.isfile(abs_path) and os.access(abs_path, os.X_OK):
            return abs_path
        return None

    path_env = os.environ.get("PATH", "")
    for directory in path_env.split(os.pathsep):
        if not directory:
            continue
        candidate = os.path.join(directory, command)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return os.path.abspath(candidate)

    return None


__all__ = ["resolve_command"]