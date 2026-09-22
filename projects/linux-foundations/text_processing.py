"""
Utility functions that demonstrate common Linux text‑processing commands
implemented in pure Python.

The functions are intentionally simple and focus on illustrating the
behaviour of tools such as ``wc``, ``grep``, ``sed``/``tr``, ``cut`` and
``sort``.  They operate on strings (the contents of a text file) and
return new strings or simple counts, making them easy to test and reuse
in other modules of the repository.
"""

from __future__ import annotations

import re
from typing import List, Sequence, Iterable


def count_lines(text: str) -> int:
    """
    Return the number of lines in *text*.

    An empty string is considered to have zero lines.  The function
    counts the number of newline characters (``\\n``) and adds one if the
    text does not end with a newline, mirroring the behaviour of ``wc -l``.
    """
    if not text:
        return 0
    # ``splitlines`` discards the trailing newline, so we count manually.
    line_breaks = text.count("\n")
    # If the text ends with a newline, the number of lines equals the
    # number of line breaks; otherwise add one for the final line.
    return line_breaks if text.endswith("\n") else line_breaks + 1


def count_words(text: str) -> int:
    """
    Return the number of whitespace‑separated words in *text*.

    Words are identified by the regular expression ``\\S+`` which matches
    any run of non‑whitespace characters, similar to the default behaviour
    of ``wc -w``.
    """
    return len(re.findall(r"\S+", text))


def count_characters(text: str, include_spaces: bool = True) -> int:
    """
    Return the number of characters in *text*.

    Parameters
    ----------
    text:
        The input string.
    include_spaces:
        If ``False`` whitespace characters (space, tab, newline, etc.) are
        excluded from the count.  The default mirrors ``wc -m`` which
        includes every byte.
    """
    if include_spaces:
        return len(text)
    # Remove all Unicode whitespace characters.
    return len(re.sub(r"\s+", "", text))


def grep(
    pattern: str,
    text: str,
    ignore_case: bool = False,
    whole_line: bool = False,
) -> List[str]:
    """
    Return a list of lines from *text* that match *pattern*.

    Parameters
    ----------
    pattern:
        Regular expression pattern.
    text:
        Multiline string to search.
    ignore_case:
        Perform a case‑insensitive match when ``True``.
    whole_line:
        When ``True`` the pattern must match the entire line (behaviour of
        ``grep -x``).

    Returns
    -------
    List[str]
        Matching lines **without** trailing newline characters.
    """
    flags = re.MULTILINE
    if ignore_case:
        flags |= re.IGNORECASE

    compiled = re.compile(pattern, flags)

    matches: List[str] = []
    for line in text.splitlines():
        if whole_line:
            if compiled.fullmatch(line):
                matches.append(line)
        else:
            if compiled.search(line):
                matches.append(line)
    return matches


def replace(
    text: str,
    old: str,
    new: str,
    count: int = -1,
    ignore_case: bool = False,
) -> str:
    """
    Replace occurrences of *old* with *new* in *text*.

    Parameters
    ----------
    text:
        Original string.
    old:
        Substring or regular‑expression pattern to replace.
    new:
        Replacement string.
    count:
        Maximum number of replacements; ``-1`` means replace all.
    ignore_case:
        If ``True`` treat *old* as a case‑insensitive regular expression.

    Returns
    -------
    str
        The resulting string.
    """
    if ignore_case:
        # ``re.sub`` handles the ``count`` argument directly.
        return re.sub(old, new, text, count=count, flags=re.IGNORECASE)
    else:
        # Use the built‑in ``str.replace`` which is faster for literal text.
        return text.replace(old, new, count)


def cut_columns(
    text: str,
    delimiter: str = "\t",
    fields: Sequence[int] | None = None,
    preserve_delimiter: bool = True,
) -> str:
    """
    Extract specific columns from each line of *text*.

    Parameters
    ----------
    text:
        Multiline input.
    delimiter:
        Column delimiter (default is a tab, matching the typical ``cut -d``).
    fields:
        1‑based column numbers to keep.  If ``None`` the original text is
        returned unchanged.
    preserve_delimiter:
        When ``True`` the output columns are joined using *delimiter*.
        When ``False`` columns are concatenated directly (useful for fixed‑width
        output).

    Returns
    -------
    str
        Text containing only the selected columns.
    """
    if fields is None:
        return text

    # Convert to zero‑based indices for Python list access.
    indices = [i - 1 for i in fields]

    output_lines: List[str] = []
    for line in text.splitlines():
        parts = line.split(delimiter)
        selected = [parts[i] for i in indices if i < len(parts)]
        if preserve_delimiter:
            output_lines.append(delimiter.join(selected))
        else:
            output_lines.append("".join(selected))
    return "\n".join(output_lines)


def sort_lines(
    text: str,
    reverse: bool = False,
    key: Callable[[str], any] | None = None,
    ignore_case: bool = False,
) -> str:
    """
    Return *text* with its lines sorted.

    Parameters
    ----------
    text:
        Multiline string.
    reverse:
        Sort in descending order when ``True``.
    key:
        Optional key function passed to ``sorted``.
    ignore_case:
        Perform a case‑insensitive sort when ``True`` (overrides *key*).

    Returns
    -------
    str
        Sorted lines joined by a newline character.
    """
    lines = text.splitlines()
    if ignore_case:
        sort_key = lambda s: s.lower()
    else:
        sort_key = key
    sorted_lines = sorted(lines, key=sort_key, reverse=reverse)
    return "\n".join(sorted_lines)


__all__ = [
    "count_lines",
    "count_words",
    "count_characters",
    "grep",
    "replace",
    "cut_columns",
    "sort_lines",
]