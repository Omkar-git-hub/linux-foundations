"""
Standard I/O utilities for educational notes.

This module provides thin wrappers around the three primary streams
``sys.stdin``, ``sys.stdout`` and ``sys.stderr``.  The functions are
intentionally simple – they merely demonstrate how to interact with the
streams without adding extra behaviour such as logging or colourised
output.

Typical usage::

    from projects.linux_foundations.notes import std_io

    # Read a line from the user
    name = std_io.read_input("Enter your name: ")

    # Write a normal message
    std_io.write_output(f"Hello, {name}!")

    # Write an error message
    std_io.write_error("Something went wrong")
"""

from __future__ import annotations

import sys
from typing import Any


def read_input(prompt: str | None = None) -> str:
    """
    Read a line from ``sys.stdin``.

    Parameters
    ----------
    prompt:
        Optional text displayed to the user before reading.  If ``None`` the
        prompt is omitted.  The prompt is written to ``sys.stdout`` and
        flushed so that it appears before the user can type.

    Returns
    -------
    str
        The line entered by the user, **without** the trailing newline.
    """
    if prompt is not None:
        # ``print`` writes to ``sys.stdout`` by default; we use it for the
        # prompt to keep behaviour consistent with the built‑in ``input``.
        print(prompt, end="", flush=True)
    # ``sys.stdin.readline`` returns the line including the newline.
    line = sys.stdin.readline()
    # Strip only the trailing newline; other whitespace is preserved.
    return line.rstrip("\n")


def write_output(message: Any, *, end: str = "\n", flush: bool = False) -> None:
    """
    Write *message* to ``sys.stdout``.

    Parameters
    ----------
    message:
        Anything that can be converted to ``str`` – the same contract as
        ``print``.
    end:
        String appended after the message.  Defaults to a newline.
    flush:
        If ``True`` the stream is flushed immediately.
    """
    print(message, end=end, file=sys.stdout, flush=flush)


def write_error(message: Any, *, end: str = "\n", flush: bool = False) -> None:
    """
    Write *message* to ``sys.stderr``.

    Parameters
    ----------
    message:
        Anything that can be converted to ``str``.
    end:
        String appended after the message.  Defaults to a newline.
    flush:
        If ``True`` the stream is flushed immediately.
    """
    print(message, end=end, file=sys.stderr, flush=flush)


__all__ = [
    "read_input",
    "write_output",
    "write_error",
]