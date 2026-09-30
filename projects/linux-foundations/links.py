"""
Utility functions for working with symbolic and hard links.

This module provides a small, cross‑platform API to:

* Create symbolic and hard links.
* Query whether a path is a symbolic link.
* Determine if a path is a hard link (i.e. has more than one link count and
  is not a symbolic link).
* Retrieve the target of a symbolic link.
* Get the link count (number of hard links) for a path.

All functions accept ``str`` or :class:`pathlib.Path` objects and return
``pathlib.Path`` instances where appropriate.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Union

PathLike = Union[str, Path]

__all__ = [
    "create_symlink",
    "create_hardlink",
    "is_symlink",
    "is_hardlink",
    "get_link_target",
    "get_hardlink_count",
]


def _to_path(p: PathLike) -> Path:
    """Coerce *p* to a :class:`~pathlib.Path`."""
    return p if isinstance(p, Path) else Path(p)


def create_symlink(
    source: PathLike,
    link_name: PathLike,
    *,
    target_is_directory: bool = False,
) -> Path:
    """
    Create a symbolic link pointing to *source* named *link_name*.

    Parameters
    ----------
    source:
        The path the symlink should point to. It may be absolute or relative.
    link_name:
        The path of the symlink to create.
    target_is_directory:
        Set to ``True`` when the target is a directory. Required on Windows
        for correct link creation.

    Returns
    -------
    pathlib.Path
        The created symlink path.
    """
    src = _to_path(source)
    link = _to_path(link_name)

    # pathlib's `symlink_to` handles the `target_is_directory` flag.
    link.symlink_to(src, target_is_directory=target_is_directory)
    return link


def create_hardlink(source: PathLike, link_name: PathLike) -> Path:
    """
    Create a hard link pointing to *source* named *link_name*.

    Parameters
    ----------
    source:
        Existing file to link to. Must be a regular file (directories cannot be
        hard‑linked on most platforms).
    link_name:
        The path of the hard link to create.

    Returns
    -------
    pathlib.Path
        The created hard link path.
    """
    src = _to_path(source)
    link = _to_path(link_name)

    # pathlib's `hardlink_to` is only available from Python 3.10.
    # Fallback to os.link for earlier versions.
    if hasattr(link, "hardlink_to"):
        link.hardlink_to(src)
    else:
        os.link(src, link)
    return link


def is_symlink(path: PathLike) -> bool:
    """
    Return ``True`` if *path* is a symbolic link.

    This works for both files and directories.
    """
    p = _to_path(path)
    return p.is_symlink()


def is_hardlink(path: PathLike) -> bool:
    """
    Return ``True`` if *path* is a hard link.

    A path is considered a hard link when its link count (``st_nlink``) is
    greater than 1 and it is **not** a symbolic link.
    """
    p = _to_path(path)
    if p.is_symlink():
        return False
    try:
        return p.stat().st_nlink > 1
    except FileNotFoundError:
        return False


def get_link_target(path: PathLike) -> Path | None:
    """
    If *path* is a symbolic link, return the path it points to; otherwise ``None``.
    """
    p = _to_path(path)
    if p.is_symlink():
        return p.readlink()
    return None


def get_hardlink_count(path: PathLike) -> int:
    """
    Return the number of hard links pointing to *path*.

    For non‑existent paths a ``FileNotFoundError`` is raised.
    """
    p = _to_path(path)
    return p.stat().st_nlink