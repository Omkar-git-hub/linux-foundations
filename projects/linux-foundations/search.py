"""
Search utilities for the *linux‑foundations* project.

This module provides a small, pure‑Python API for locating files and
searching for text within those files.  The functions are deliberately
generic so they can be reused by the higher‑level modules that deal
with notes, permissions, processes, etc.

Typical usage
-------------

>>> from projects.linux_foundations.search import (
...     find_files_by_name,
...     grep_in_files,
... )
>>> files = find_files_by_name("/etc", "hosts")
>>> matches = grep_in_files("/etc", r"^127\.0\.0\.1")
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, List, Tuple

__all__ = [
    "iter_files",
    "find_files_by_name",
    "grep_in_files",
    "search_notes",
]


def iter_files(root: Path | str, *, follow_symlinks: bool = False) -> Iterable[Path]:
    """
    Recursively yield all regular files under *root*.

    Parameters
    ----------
    root:
        The directory to start the walk from.
    follow_symlinks:
        Whether to follow symbolic links that point to directories.
        The default is ``False`` to avoid infinite recursion.

    Yields
    ------
    pathlib.Path
        Paths to regular files.
    """
    root_path = Path(root)
    if not root_path.is_dir():
        raise ValueError(f"The supplied root '{root}' is not a directory.")
    for dirpath, dirnames, filenames in Path(root_path).walk():
        # ``Path.walk`` is not a built‑in method; we emulate it with ``rglob``.
        # Using ``rglob('*')`` gives us both files and directories; we filter.
        # The explicit loop keeps the implementation clear and testable.
        pass
    # The above placeholder is replaced by a concrete implementation below.
    for path in root_path.rglob("*"):
        if path.is_file():
            # ``follow_symlinks`` handling – ``Path.is_symlink`` tells us if the
            # entry itself is a symlink.  For directories we rely on ``rglob``
            # which already follows symlinks when ``follow_symlinks`` is True.
            if not follow_symlinks and path.is_symlink():
                continue
            yield path


def find_files_by_name(root: Path | str, query: str, *, case_insensitive: bool = True) -> List[Path]:
    """
    Return a list of files whose *basename* contains *query*.

    Parameters
    ----------
    root:
        Directory to start the search.
    query:
        Sub‑string to look for in file names.
    case_insensitive:
        Perform a case‑insensitive match when ``True`` (default).

    Returns
    -------
    list[pathlib.Path]
        Matching file paths, sorted alphabetically.
    """
    if not query:
        raise ValueError("Query string must not be empty.")
    matcher = query.lower() if case_insensitive else query
    matches: List[Path] = []
    for file_path in iter_files(root):
        name = file_path.name.lower() if case_insensitive else file_path.name
        if matcher in name:
            matches.append(file_path)
    matches.sort()
    return matches


def grep_in_files(
    root: Path | str,
    pattern: str,
    *,
    regex: bool = True,
    case_insensitive: bool = False,
) -> List[Tuple[Path, int, str]]:
    """
    Search for *pattern* inside all files under *root*.

    The function works similarly to the Unix ``grep`` command but returns
    a structured result instead of printing to stdout.

    Parameters
    ----------
    root:
        Directory to search.
    pattern:
        Text or regular expression to look for.
    regex:
        If ``True`` (default) treat *pattern* as a regular expression.
        If ``False`` perform a literal substring search.
    case_insensitive:
        Perform a case‑insensitive match when ``True``.

    Returns
    -------
    list[tuple[pathlib.Path, int, str]]
        A list of ``(file_path, line_number, line_text)`` tuples for each
        matching line.  ``line_number`` is 1‑based.
    """
    flags = re.IGNORECASE if case_insensitive else 0
    compiled: re.Pattern | None = None
    if regex:
        compiled = re.compile(pattern, flags)
    else:
        # For literal searches we still use ``re`` for consistent handling
        # of case‑insensitivity.
        escaped = re.escape(pattern)
        compiled = re.compile(escaped, flags)

    results: List[Tuple[Path, int, str]] = []
    for file_path in iter_files(root):
        try:
            with file_path.open("r", encoding="utf-8", errors="replace") as f:
                for lineno, line in enumerate(f, start=1):
                    if compiled.search(line):
                        results.append((file_path, lineno, line.rstrip("\n")))
        except (OSError, UnicodeDecodeError):
            # Skip files that cannot be read as text.
            continue
    return results


def _notes_directory() -> Path:
    """
    Resolve the absolute path to the ``notes`` package that lives next to this
    module.  The function is isolated to make unit‑testing easier.
    """
    return Path(__file__).resolve().parent / "notes"


def search_notes(keyword: str, *, case_insensitive: bool = True) -> List[Tuple[str, str]]:
    """
    Search for *keyword* inside the project's note files.

    The notes are stored as Python source files under
    ``projects/linux-foundations/notes``.  The function scans each file,
    extracts lines that contain the keyword and returns a concise summary.

    Parameters
    ----------
    keyword:
        Text to look for inside the note files.
    case_insensitive:
        Perform a case‑insensitive match when ``True`` (default).

    Returns
    -------
    list[tuple[str, str]]
        Each tuple contains ``(module_name, snippet)`` where *module_name*
        is the dotted module path (e.g. ``linux_foundations.notes.pipes``) and
        *snippet* is the first line that contains the keyword, stripped of
        surrounding whitespace.
    """
    if not keyword:
        raise ValueError("Keyword must not be empty.")
    notes_dir = _notes_directory()
    if not notes_dir.is_dir():
        raise FileNotFoundError(f"Notes directory not found: {notes_dir}")

    matcher = keyword.lower() if case_insensitive else keyword
    results: List[Tuple[str, str]] = []

    for py_file in notes_dir.glob("*.py"):
        try:
            with py_file.open("r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    haystack = line.lower() if case_insensitive else line
                    if matcher in haystack:
                        module_name = f"linux_foundations.notes.{py_file.stem}"
                        results.append((module_name, line.strip()))
                        break  # Only the first matching line per file.
        except OSError:
            continue
    results.sort()
    return results