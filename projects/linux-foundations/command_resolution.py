"""
Utility functions for resolving executable commands using the system ``PATH`` variable.

The module provides a small, pure‑Python implementation that mirrors the behaviour
of the Unix ``which`` command.  It is deliberately lightweight and does not depend
on external packages – only the Python standard library.

Typical usage
-------------

>>> from projects.linux_foundations.command_resolution import resolve_command
>>> resolve_command("python")  # doctest: +SKIP
PosixPath('/usr/bin/python')
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import List, Optional

__all__ = [
    "get_path_dirs",
    "is_executable",
    "resolve_command",
]


def get_path_dirs() -> List[Path]:
    """
    Return a list of directories from the ``PATH`` environment variable.

    The function splits the ``PATH`` variable using ``os.pathsep`` (``:`` on
    POSIX, ``;`` on Windows) and returns each entry as a :class:`~pathlib.Path`
    object. Empty entries are ignored.

    Returns
    -------
    List[Path]
        Ordered list of directories that constitute the search path.
    """
    raw_path = os.getenv("PATH", "")
    dirs = [Path(p) for p in raw_path.split(os.pathsep) if p]
    return dirs


def is_executable(file_path: Path) -> bool:
    """
    Determine whether *file_path* points to an executable file.

    The check is performed using ``os.access`` with the ``X_OK`` flag.  On
    Windows the function also checks the file suffix against the list of
    PATHEXT extensions.

    Parameters
    ----------
    file_path : Path
        Path to the candidate file.

    Returns
    -------
    bool
        ``True`` if the file exists and is executable, ``False`` otherwise.
    """
    if not file_path.is_file():
        return False

    if os.name == "nt":
        # Windows uses PATHEXT to decide what is executable.
        pathext = os.getenv("PATHEXT", ".COM;.EXE;.BAT;.CMD")
        executable_exts = {ext.lower() for ext in pathext.split(os.pathsep)}
        return file_path.suffix.lower() in executable_exts
    else:
        return os.access(str(file_path), os.X_OK)


def resolve_command(command: str) -> Optional[Path]:
    """
    Resolve *command* to an absolute path of an executable using the ``PATH`` variable.

    The resolution follows the same rules as the Unix ``which`` command:

    * If *command* contains a directory separator (``/`` on POSIX, ``\\`` on
      Windows), it is treated as a direct path.  The function checks whether the
      path points to an executable file and returns it if so.
    * Otherwise the function iterates over each directory listed in ``PATH`` and
      returns the first matching executable.

    Parameters
    ----------
    command : str
        Name of the command or a relative/absolute path.

    Returns
    -------
    Optional[Path]
        Absolute :class:`~pathlib.Path` to the executable if found, otherwise ``None``.
    """
    # Direct path supplied?
    candidate = Path(command)
    if os.sep in command or (os.altsep and os.altsep in command):
        if is_executable(candidate):
            return candidate.resolve()
        return None

    # Search through PATH directories.
    for directory in get_path_dirs():
        potential = directory / command
        if is_executable(potential):
            return potential.resolve()

    # Fallback to shutil.which for edge‑cases (e.g., Windows PATHEXT handling).
    which_result = shutil.which(command)
    if which_result:
        return Path(which_result).resolve()

    return None