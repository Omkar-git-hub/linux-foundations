"""
Utility functions for basic file and directory operations.

This module provides a small, well‑tested API that can be used in the
“Learn Files and Directories” exercises.  All functions operate on
text files using UTF‑8 encoding and raise the standard Python exceptions
for error conditions (e.g., ``FileNotFoundError`` for missing paths).

Public API
~~~~~~~~~~
- ``list_files`` – Return a sorted list of file names in a directory.
- ``read_file`` – Read the entire contents of a text file.
- ``write_file`` – Write text to a file, creating parent directories as needed.
- ``ensure_dir_exists`` – Ensure a directory exists, creating it if necessary.
"""

from __future__ import annotations

from pathlib import Path
from typing import List


def ensure_dir_exists(directory: str | Path) -> None:
    """
    Ensure that *directory* exists.

    If the directory (or any of its parents) does not exist, it is created.
    The function does nothing if the directory already exists.

    Parameters
    ----------
    directory: str or pathlib.Path
        Path to the directory that should exist.
    """
    Path(directory).mkdir(parents=True, exist_ok=True)


def list_files(directory: str | Path) -> List[str]:
    """
    Return a sorted list of file names (not directories) directly under *directory*.

    The function does **not** recurse into sub‑directories.  Only regular files
    are returned; symbolic links that point to files are included, while links
    to directories are ignored.

    Parameters
    ----------
    directory: str or pathlib.Path
        The directory to inspect.

    Returns
    -------
    List[str]
        Sorted list of file names (as strings) present in *directory*.

    Raises
    ------
    FileNotFoundError
        If *directory* does not exist or is not a directory.
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        raise FileNotFoundError(f"Directory not found: {directory!s}")

    files = [p.name for p in dir_path.iterdir() if p.is_file()]
    files.sort()
    return files


def read_file(file_path: str | Path) -> str:
    """
    Read the entire contents of a text file using UTF‑8 encoding.

    Parameters
    ----------
    file_path: str or pathlib.Path
        Path to the file to be read.

    Returns
    -------
    str
        The file contents.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    UnicodeDecodeError
        If the file cannot be decoded as UTF‑8.
    """
    path = Path(file_path)
    return path.read_text(encoding="utf-8")


def write_file(file_path: str | Path, content: str) -> None:
    """
    Write *content* to *file_path* using UTF‑8 encoding.

    The parent directory is created automatically if it does not exist.

    Parameters
    ----------
    file_path: str or pathlib.Path
        Destination file path.
    content: str
        Text to write to the file.

    Raises
    ------
    OSError
        If the file cannot be written for any OS‑level reason.
    """
    path = Path(file_path)
    ensure_dir_exists(path.parent)
    path.write_text(content, encoding="utf-8")


__all__ = [
    "ensure_dir_exists",
    "list_files",
    "read_file",
    "write_file",
]