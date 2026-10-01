"""
Utility functions for working with filesystem links.

This module provides a small, well‑tested API for common link operations
such as creating a symbolic link, checking whether a path is a symlink,
and enumerating all symlinks inside a directory.

All functions operate on ``str`` paths for convenience but internally use
``pathlib.Path`` to leverage the standard library's robust handling of
filesystem paths.
"""

from pathlib import Path
from typing import List, Iterable


def is_symlink(path: str) -> bool:
    """
    Return ``True`` if *path* exists and is a symbolic link.

    Parameters
    ----------
    path: str
        The filesystem path to inspect.

    Returns
    -------
    bool
        ``True`` if the path is a symbolic link, ``False`` otherwise.
    """
    return Path(path).is_symlink()


def create_symlink(target: str, link_name: str) -> Path:
    """
    Create a symbolic link named *link_name* pointing to *target*.

    If a file, directory or link already exists at *link_name*, a
    ``FileExistsError`` is raised – this mirrors the behaviour of the
    underlying ``Path.symlink_to`` call.

    Parameters
    ----------
    target: str
        The path that the new symlink should point to.  It may be absolute
        or relative; the function does not resolve it.
    link_name: str
        The path of the symlink to create.

    Returns
    -------
    pathlib.Path
        The ``Path`` object representing the newly created symlink.

    Raises
    ------
    FileExistsError
        If *link_name* already exists.
    OSError
        If the operating system reports an error while creating the link.
    """
    link_path = Path(link_name)
    # ``symlink_to`` will raise FileExistsError if the path already exists.
    link_path.symlink_to(target)
    return link_path


def list_symlinks(directory: str) -> List[Path]:
    """
    Return a list of all symbolic links directly under *directory*.

    The function does **not** recurse into sub‑directories; only entries
    that are immediate children of *directory* are examined.

    Parameters
    ----------
    directory: str
        The directory whose contents should be inspected.

    Returns
    -------
    List[pathlib.Path]
        A list of ``Path`` objects, each representing a symbolic link.
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        raise NotADirectoryError(f"{directory!r} is not a directory")
    return [entry for entry in dir_path.iterdir() if entry.is_symlink()]


def iter_symlinks(directory: str) -> Iterable[Path]:
    """
    Yield symbolic links directly under *directory* one by one.

    This generator is useful when the caller wants to process links lazily
    without constructing an intermediate list.

    Parameters
    ----------
    directory: str
        The directory to scan.

    Yields
    ------
    pathlib.Path
        Each symbolic link found in *directory*.
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        raise NotADirectoryError(f"{directory!r} is not a directory")
    for entry in dir_path.iterdir():
        if entry.is_symlink():
            yield entry


__all__ = [
    "is_symlink",
    "create_symlink",
    "list_symlinks",
    "iter_symlinks",
]