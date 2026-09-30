"""
Linux Links Notes
=================

Utility functions for working with symbolic and hard links on Linux (and
POSIX‑compatible systems).  The functions are deliberately thin wrappers
around the :pymod:`os` and :pymod:`pathlib` modules so that they can be
re‑used in the documentation notebooks and in the test‑suite.

The public API mirrors the most common operations one would perform when
learning about links:

* :func:`is_symlink` – check whether a path is a symbolic link.
* :func:`is_hardlink` – check whether a path is a hard link (i.e. a regular
  file with a link count greater than one and that is **not** a symbolic
  link).
* :func:`create_symlink` – create a symbolic link.
* :func:`create_hardlink` – create a hard link.
* :func:`readlink` – return the target of a symbolic link.
* :func:`resolve_path` – resolve a path, following symbolic links.
* :func:`list_symlinks` – list all symbolic links in a directory (non‑recursive).

All functions raise the standard :class:`OSError` exceptions that the
underlying ``os`` calls raise; the test suite validates the happy path
behaviour.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


def is_symlink(path: str | os.PathLike) -> bool:
    """
    Return ``True`` if *path* exists and is a symbolic link.

    Parameters
    ----------
    path:
        Path to test.

    Returns
    -------
    bool
        ``True`` if *path* is a symbolic link, otherwise ``False``.
    """
    return Path(path).is_symlink()


def is_hardlink(path: str | os.PathLike) -> bool:
    """
    Return ``True`` if *path* exists, is a regular file, and has a link count
    greater than one (i.e. there is at least one other hard link to the same
    inode).  Symbolic links are **not** considered hard links.

    Parameters
    ----------
    path:
        Path to test.

    Returns
    -------
    bool
        ``True`` if *path* is a hard link, otherwise ``False``.
    """
    p = Path(path)
    if not p.is_file():
        return False
    # ``is_symlink`` must be False – a symlink can also be a file, but we
    # explicitly exclude it.
    if p.is_symlink():
        return False
    try:
        return p.stat().st_nlink > 1
    except OSError:
        return False


def create_symlink(target: str | os.PathLike, link_name: str | os.PathLike) -> None:
    """
    Create a symbolic link named *link_name* pointing to *target*.

    The function mirrors ``os.symlink`` but raises a clearer error message
    when the operation fails.

    Parameters
    ----------
    target:
        The path the symbolic link should point to.
    link_name:
        The name of the symbolic link to create.

    Raises
    ------
    OSError
        If the link cannot be created (e.g., permission denied or the link
        already exists).
    """
    os.symlink(str(target), str(link_name))


def create_hardlink(source: str | os.PathLike, link_name: str | os.PathLike) -> None:
    """
    Create a hard link named *link_name* pointing to *source*.

    Parameters
    ----------
    source:
        Existing file to link to.
    link_name:
        Name of the new hard link.

    Raises
    ------
    OSError
        If the hard link cannot be created.
    """
    os.link(str(source), str(link_name))


def readlink(link_path: str | os.PathLike) -> str:
    """
    Return the path to which the symbolic link *link_path* points.

    Parameters
    ----------
    link_path:
        Path to a symbolic link.

    Returns
    -------
    str
        The target of the symbolic link.

    Raises
    ------
    OSError
        If *link_path* is not a symbolic link or cannot be read.
    """
    return os.readlink(str(link_path))


def resolve_path(path: str | os.PathLike) -> str:
    """
    Resolve *path* to its absolute, canonical form, following symbolic links.

    This is a thin wrapper around :pymeth:`pathlib.Path.resolve`.

    Parameters
    ----------
    path:
        Path to resolve.

    Returns
    -------
    str
        The resolved absolute path.
    """
    return str(Path(path).resolve())


def list_symlinks(directory: str | os.PathLike) -> List[Tuple[str, str]]:
    """
    Return a list of ``(link, target)`` tuples for all symbolic links in
    *directory* (non‑recursive).

    Parameters
    ----------
    directory:
        Directory to scan.

    Returns
    -------
    list[tuple[str, str]]
        List of symbolic links and their targets.
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        raise NotADirectoryError(f"{directory!r} is not a directory")
    result: List[Tuple[str, str]] = []
    for entry in dir_path.iterdir():
        if entry.is_symlink():
            try:
                target = os.readlink(str(entry))
            except OSError:
                target = ""
            result.append((str(entry), target))
    return result


__all__: Iterable[str] = (
    "is_symlink",
    "is_hardlink",
    "create_symlink",
    "create_hardlink",
    "readlink",
    "resolve_path",
    "list_symlinks",
)