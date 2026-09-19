"""
Standard Input, Output, and Error utilities.

This module provides simple helper functions that demonstrate reading from
standard input and writing to standard output and standard error.  The
functions are deliberately small so they can be used in teaching examples
or unit tests without pulling in heavy dependencies.

Functions
---------
read_line(prompt: str = "") -> str
    Read a line from ``sys.stdin`` (using ``input``) and return it.

write_stdout(message: str, end: str = \"\\n\") -> None
    Write *message* to ``sys.stdout`` using the provided *end* string.

write_stderr(message: str, end: str = \"\\n\") -> None
    Write *message* to ``sys.stderr`` using the provided *end* string.

echo_input(prompt: str = \"\") -> None
    Read a line from standard input and immediately echo it to standard
    output.  This is a tiny wrapper around :func:`read_line` and
    :func:`write_stdout`.

error_on_empty(prompt: str = \"\") -> None
    Read a line from standard input; if the line is empty (after stripping
    whitespace) write an error message to standard error, otherwise write
    the line to standard output.
"""

from __future__ import annotations

import sys
from typing import Callable


def read_line(prompt: str = "") -> str:
    """
    Read a line from standard input.

    Parameters
    ----------
    prompt: str, optional
        Prompt displayed to the user.  Defaults to an empty string.

    Returns
    -------
    str
        The line entered by the user, without the trailing newline.
    """
    return input(prompt)


def write_stdout(message: str, end: str = "\n") -> None:
    """
    Write *message* to standard output.

    Parameters
    ----------
    message: str
        Text to write.
    end: str, optional
        String appended after the message.  Defaults to a newline.
    """
    sys.stdout.write(message + end)
    sys.stdout.flush()


def write_stderr(message: str, end: str = "\n") -> None:
    """
    Write *message* to standard error.

    Parameters
    ----------
    message: str
        Text to write.
    end: str, optional
        String appended after the message.  Defaults to a newline.
    """
    sys.stderr.write(message + end)
    sys.stderr.flush()


def _process_input(
    prompt: str,
    on_success: Callable[[str], None],
    on_failure: Callable[[str], None] | None = None,
) -> None:
    """
    Internal helper that reads a line and dispatches to callbacks.

    Parameters
    ----------
    prompt: str
        Prompt shown to the user.
    on_success: Callable[[str], None]
        Called with the stripped line when the line is non‑empty.
    on_failure: Callable[[str], None] | None, optional
        Called with the original line when the line is empty.  If ``None``,
        nothing is written.
    """
    line = read_line(prompt)
    stripped = line.strip()
    if stripped:
        on_success(stripped)
    elif on_failure is not None:
        on_failure(line)


def echo_input(prompt: str = "") -> None:
    """
    Read a line from standard input and echo it to standard output.

    Parameters
    ----------
    prompt: str, optional
        Prompt displayed to the user.
    """
    _process_input(prompt, on_success=lambda txt: write_stdout(txt))


def error_on_empty(prompt: str = "") -> None:
    """
    Read a line from standard input; if the line is empty, write an error
    message to standard error, otherwise echo the line to standard output.

    Parameters
    ----------
    prompt: str, optional
        Prompt displayed to the user.
    """
    _process_input(
        prompt,
        on_success=lambda txt: write_stdout(txt),
        on_failure=lambda _: write_stderr("Error: empty input"),
    )


__all__ = [
    "read_line",
    "write_stdout",
    "write_stderr",
    "echo_input",
    "error_on_empty",
]