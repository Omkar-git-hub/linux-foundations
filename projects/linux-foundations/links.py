"""
Utility functions for working with filesystem links.

This module provides a small, well‑tested API for common link operations
such as creating, listing, inspecting and removing symbolic links.
All functions accept either ``str`` or :class:`pathlib.Path` objects and
return :class:`pathlib.Path` instances where appropriate.

The implementation deliberately avoids external dependencies and relies
solely on the Python standard library, making it suitable for use in
restricted environments such as CI pipelines.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, List, Sequence

__all__: Sequence[str] = (
    "list_symlinks",
    "get_symlink_target",
    "is_broken_symlink",
    "create_symlink",
    "remove_symlink",
)


def _ensure_path(p: str | Path) -> Path:
    """Convert *p* to a :class:`Path` instance."""
    return p if isinstance(p, Path) else Path(p)


def list_symlinks(directory: str | Path) -> List[Path]:
    """
    Return a list of all symbolic links directly under *directory*.

    The search is **non‑recursive**; only entries that are immediate children
    of *directory* are considered.  The returned paths are absolute
    :class:`Path` objects.

    Parameters
    ----------
    directory:
        Path to the directory to scan.

    Returns
    -------
    list[Path]
        A list of symbolic‑link paths found in *directory*.
    """
    dir_path = _ensure_path(directory).expanduser().resolve()
    if not dir_path.is_dir():
        raise NotADirectoryError(f"{dir_path} is not a directory")
    return [entry.resolve(strict=False) for entry in dir_path.iterdir() if entry.is_symlink()]


def get_symlink_target(link_path: str | Path) -> Path:
    """
    Return the target of the symbolic link *link_path*.

    The function does **not** resolve the target; it simply returns the raw
    path stored in the link.  The returned value is a :class:`Path` object
    that may be relative to the link's location.

    Parameters
    ----------
    link_path:
        Path to the symbolic link.

    Returns
    -------
    Path
        The target path stored in the link.

    Raises
    ------
    ValueError
        If *link_path* is not a symbolic link.
    """
    link = _ensure_path(link_path).expanduser()
    if not link.is_symlink():
        raise ValueError(f"{link} is not a symbolic link")
    # readlink returns the raw target string; wrap it in Path for convenience
    target_str = os.readlink(str(link))
    return Path(target_str)


def is_broken_symlink(link_path: str | Path) -> bool:
    """
    Determine whether *link_path* is a broken symbolic link.

    A link is considered broken when it exists, is a symbolic link, and its
    target does not resolve to an existing filesystem entry.

    Parameters
    ----------
    link_path:
        Path to the symbolic link.

    Returns
    -------
    bool
        ``True`` if the link is broken, ``False`` otherwise.
    """
    link = _ensure_path(link_path).expanduser()
    if not link.is_symlink():
        return False
    try:
        # ``resolve`` with ``strict=True`` raises if the target does not exist.
        link.resolve(strict=True)
        return False
    except FileNotFoundError:
        return True


def create_symlink(
    source: str | Path,
    link_name: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    """
    Create a symbolic link named *link_name* pointing to *source*.

    Parameters
    ----------
    source:
        The path that the new link should point to.  It may be absolute or
        relative; the function does not modify the value.
    link_name:
        Desired location of the symbolic link.
    overwrite:
        If ``True`` and *link_name* already exists (as a file, directory,
        or link), it will be removed before creating the new link.
        If ``False`` and *link_name* exists, a :class:`FileExistsError` is raised.

    Returns
    -------
    Path
        The absolute path to the created symbolic link.

    Raises
    ------
    FileExistsError
        If *link_name* exists and ``overwrite`` is ``False``.
    """
    src = _ensure_path(source)
    link = _ensure_path(link_name).expanduser().resolve()
    if link.exists() or link.is_symlink():
        if not overwrite:
            raise FileExistsError(f"{link} already exists")
        # Remove whatever is there (file, dir, or link)
        if link.is_dir() and not link.is_symlink():
            # For directories we need to remove recursively
            import shutil

            shutil.rmtree(link)
        else:
            link.unlink()
    # Ensure parent directory exists
    link.parent.mkdir(parents=True, exist_ok=True)
    # Use pathlib's symlink_to; it creates a symlink with the given target.
    # ``target_is_directory`` is inferred from the source path.
    link.symlink_to(src, target_is_directory=src.is_dir())
    return link


def remove_symlink(link_path: str | Path) -> None:
    """
    Remove the symbolic link at *link_path*.

    The function only removes the link itself; it never follows the link
    to delete the target.  If *link_path* does not exist or is not a symbolic
    link, a :class:`FileNotFoundError` or :class:`ValueError` is raised
    respectively.

    Parameters
    ----------
    link_path:
        Path to the symbolic link to delete.
    """
    link = _ensure_path(link_path).expanduser()
    if not link.exists():
        raise FileNotFoundError(f"{link} does not exist")
    if not link.is_symlink():
        raise ValueError(f"{link} is not a symbolic link")
    link.unlink()