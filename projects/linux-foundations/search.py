"""
Utility functions for searching files and text within files.

This module provides simple helpers to:
- Recursively locate files matching a glob pattern.
- Search for regular‑expression matches inside a single file.
- Combine both operations to search across a directory tree.

All functions operate on ``pathlib.Path`` objects and return standard
Python collections, making them easy to use in scripts or notebooks.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


def find_files(root: Path | str, pattern: str) -> List[Path]:
    """
    Recursively find files under *root* that match the given glob *pattern*.

    Parameters
    ----------
    root: Path | str
        The directory from which the search starts.
    pattern: str
        A glob pattern understood by :meth:`Path.rglob`, e.g. ``"*.txt"`` or
        ``"**/*.log"``.

    Returns
    -------
    List[Path]
        A list of absolute ``Path`` objects matching the pattern. The list is
        sorted alphabetically for reproducibility.
    """
    root_path = Path(root).expanduser().resolve()
    if not root_path.is_dir():
        raise NotADirectoryError(f"The root path '{root_path}' is not a directory.")
    matches = list(root_path.rglob(pattern))
    matches = [p.resolve() for p in matches if p.is_file()]
    matches.sort()
    return matches


def grep_in_file(
    file_path: Path | str,
    regex: str,
    *,
    ignore_case: bool = False,
    multiline: bool = False,
) -> List[str]:
    """
    Return all lines from *file_path* that match the regular expression *regex*.

    Parameters
    ----------
    file_path: Path | str
        Path to the file to be searched.
    regex: str
        Regular expression pattern.
    ignore_case: bool, default ``False``
        If ``True``, perform a case‑insensitive match.
    multiline: bool, default ``False``
        If ``True``, ``^`` and ``$`` match the start and end of each line
        (the default ``re.MULTILINE`` behaviour). When ``False`` the pattern
        is applied to each line individually, which is equivalent for most
        use‑cases.

    Returns
    -------
    List[str]
        A list of the matching lines **including** their original newline
        characters.
    """
    path = Path(file_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"The file '{path}' does not exist.")
    flags = 0
    if ignore_case:
        flags |= re.IGNORECASE
    if multiline:
        flags |= re.MULTILINE

    pattern = re.compile(regex, flags)

    matches: List[str] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if pattern.search(line):
                matches.append(line)
    return matches


def grep_in_dir(
    root: Path | str,
    file_pattern: str,
    regex: str,
    *,
    ignore_case: bool = False,
    multiline: bool = False,
) -> Dict[Path, List[str]]:
    """
    Search for *regex* inside all files under *root* that match *file_pattern*.

    Parameters
    ----------
    root: Path | str
        Directory to start the search.
    file_pattern: str
        Glob pattern for files to be inspected (e.g. ``"*.py"``).
    regex: str
        Regular expression to look for inside each file.
    ignore_case: bool, default ``False``
        Forwarded to :func:`grep_in_file`.
    multiline: bool, default ``False``
        Forwarded to :func:`grep_in_file`.

    Returns
    -------
    Dict[Path, List[str]]
        Mapping from each file that contains at least one match to the list of
        matching lines from that file.
    """
    result: Dict[Path, List[str]] = {}
    for file_path in find_files(root, file_pattern):
        matches = grep_in_file(
            file_path,
            regex,
            ignore_case=ignore_case,
            multiline=multiline,
        )
        if matches:
            result[file_path] = matches
    return result


__all__: Sequence[str] = ("find_files", "grep_in_file", "grep_in_dir")