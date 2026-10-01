"""
Utility functions for working with filesystem links.

This module provides a small, cross‑platform API for creating and
inspecting symbolic and hard links.  The functions are deliberately
simple and raise clear exceptions when operations fail, which makes
them easy to use in scripts and unit tests.

Typical usage::

    from projects.linux_foundations.links import (
        create_symlink,
        create_hardlink,
        read_link,
        is_symlink,
    )

    src = Path("/tmp/example.txt")
    dst = Path("/tmp/example_link.txt")
    create_symlink(src, dst)
    assert is_symlink(dst)
    assert read_link(dst) == src
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Union

__all__ = [
    "create_symlink",
    "create_hardlink",
    "read_link",
    "is_symlink",
    "is_hardlink",
    "link_target",
]


PathLike = Union[str, os.PathLike, Path]


def _to_path(p: PathLike) -> Path:
    """Convert a path‑like object to a ``Path`` instance."""
    return p if isinstance(p, Path) else Path(p)


def create_symlink(source: PathLike, link_name: PathLike, *, target_is_directory: bool = False) -> Path:
    """
    Create a symbolic link.

    Parameters
    ----------
    source: PathLike
        The path that the symlink should point to.
    link_name: PathLike
        The location where the symlink will be created.
    target_is_directory: bool, optional
        If ``True`` the underlying target is a directory.  This flag is
        required on Windows when creating directory symlinks.

    Returns
    -------
    Path
        The ``Path`` object representing the created symlink.

    Raises
    ------
    FileExistsError
        If ``link_name`` already exists.
    FileNotFoundError
        If ``source`` does not exist.
    OSError
        For any other OS‑level error.
    """
    src = _to_path(source)
    dst = _to_path(link_name)

    if not src.exists():
        raise FileNotFoundError(f"Source path does not exist: {src}")

    if dst.exists() or dst.is_symlink():
        raise FileExistsError(f"Link destination already exists: {dst}")

    # Ensure the parent directory exists.
    dst.parent.mkdir(parents=True, exist_ok=True)

    dst.symlink_to(src, target_is_directory=target_is_directory)
    return dst


def create_hardlink(source: PathLike, link_name: PathLike) -> Path:
    """
    Create a hard link.

    Parameters
    ----------
    source: PathLike
        The existing file to link to.
    link_name: PathLike
        The new hard‑link path to create.

    Returns
    -------
    Path
        The ``Path`` object representing the created hard link.

    Raises
    ------
    FileExistsError
        If ``link_name`` already exists.
    FileNotFoundError
        If ``source`` does not exist or is not a regular file.
    OSError
        For any other OS‑level error.
    """
    src = _to_path(source)
    dst = _to_path(link_name)

    if not src.is_file():
        raise FileNotFoundError(f"Source file does not exist or is not a regular file: {src}")

    if dst.exists():
        raise FileExistsError(f"Link destination already exists: {dst}")

    dst.parent.mkdir(parents=True, exist_ok=True)

    os.link(src, dst)
    return dst


def read_link(link_path: PathLike) -> Path:
    """
    Return the target of a symbolic link.

    Parameters
    ----------
    link_path: PathLike
        Path to the symbolic link.

    Returns
    -------
    Path
        The resolved target path (as stored in the link, not the
        absolute resolved path).

    Raises
    ------
    ValueError
        If ``link_path`` is not a symbolic link.
    """
    p = _to_path(link_path)
    if not p.is_symlink():
        raise ValueError(f"The path is not a symbolic link: {p}")
    return p.readlink()


def is_symlink(path: PathLike) -> bool:
    """
    Return ``True`` if *path* is a symbolic link.

    This is a thin wrapper around :py:meth:`pathlib.Path.is_symlink`.
    """
    return _to_path(path).is_symlink()


def is_hardlink(path: PathLike) -> bool:
    """
    Return ``True`` if *path* is a hard link to an existing file.

    The function checks that the path exists, is a regular file, and
    that its link count is greater than one.  Note that the original
    file also satisfies this condition, so the function merely tells
    you whether the file participates in a hard‑link group.
    """
    p = _to_path(path)
    return p.is_file() and p.stat().st_nlink > 1


def link_target(path: PathLike) -> Path:
    """
    Convenience wrapper that returns the target of *path* if it is a
    symbolic link, otherwise returns the path itself.

    This mirrors the behaviour of the ``readlink -f`` command on Linux
    (without resolving the final target to an absolute path).
    """
    p = _to_path(path)
    return read_link(p) if p.is_symlink() else p