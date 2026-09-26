"""
pipes.py – Utilities and notes for demonstrating Unix pipes and command chaining.

This module provides small helper functions that can be used in teaching
materials or interactive sessions to illustrate how pipelines work at the
process level.  The functions are deliberately lightweight and rely only on
the Python standard library.

Typical usage
-------------

>>> from projects.linux_foundations.notes.pipes import run_pipe, run_chain
>>> # Simple pipeline equivalent to: echo "hello" | tr a-z A-Z
>>> run_pipe([["echo", "hello"], ["tr", "a-z", "A-Z"]])
'HELLO\\n'

>>> # Command chaining (sequential execution, not piped)
>>> run_chain([["date"], ["whoami"]])
[(0, 'Mon Sep 30 12:34:56 UTC 2024\\n', ''), (0, 'alice\\n', '')]
"""

from __future__ import annotations

import subprocess
from typing import List, Sequence, Tuple


def _validate_commands(commands: Sequence[Sequence[str]]) -> None:
    """Validate that *commands* is a non‑empty sequence of non‑empty command lists.

    Raises
    ------
    ValueError
        If *commands* is empty or any individual command is empty.
    """
    if not commands:
        raise ValueError("At least one command must be provided.")
    for i, cmd in enumerate(commands):
        if not cmd:
            raise ValueError(f"Command at position {i} is empty.")


def run_pipe(commands: List[List[str]]) -> str:
    """Execute a series of commands connected by Unix pipes.

    The function creates a pipeline where the standard output of each command
    becomes the standard input of the next command.  The final command's
    standard output is captured and returned as a decoded string.

    Parameters
    ----------
    commands :
        A list where each element is a list of strings representing a command
        and its arguments, e.g. ``[["ls", "-l"], ["grep", "py"]]``.

    Returns
    -------
    str
        The decoded standard output of the last command in the pipeline.

    Raises
    ------
    subprocess.CalledProcessError
        If any command in the pipeline exits with a non‑zero status.
    ValueError
        If *commands* is empty or contains an empty command.
    """
    _validate_commands(commands)

    # Initialise the pipeline.  The first process reads from the default stdin.
    # Subsequent processes read from the previous process's stdout.
    processes: List[subprocess.Popen] = []
    prev_stdout = None

    for i, cmd in enumerate(commands):
        # For the last command we want to capture stdout.
        capture_stdout = i == len(commands) - 1
        proc = subprocess.Popen(
            cmd,
            stdin=prev_stdout,
            stdout=subprocess.PIPE if capture_stdout else subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        # Close the previous stdout in the parent to allow the child to receive EOF.
        if prev_stdout is not None:
            prev_stdout.close()
        prev_stdout = proc.stdout
        processes.append(proc)

    # At this point ``prev_stdout`` refers to the stdout pipe of the last process.
    # Retrieve its output and wait for all processes to finish.
    final_output, final_err = processes[-1].communicate()
    # Ensure earlier processes have terminated.
    for proc in processes[:-1]:
        proc.wait()

    # Propagate errors if any process failed.
    for proc in processes:
        if proc.returncode != 0:
            # Include stderr from the failing process for easier debugging.
            err_msg = proc.stderr.read() if proc.stderr else ""
            raise subprocess.CalledProcessError(
                proc.returncode, proc.args, output=final_output, stderr=err_msg
            )

    return final_output


def run_chain(commands: List[List[str]]) -> List[Tuple[int, str, str]]:
    """Execute a list of commands sequentially (no piping).

    Each command runs independently; its stdout and stderr are captured.
    The function returns a list of tuples containing the return code,
    stdout, and stderr for each command in the order they were executed.

    Parameters
    ----------
    commands :
        A list of command specifications, each being a list of strings.

    Returns
    -------
    list[tuple[int, str, str]]
        ``[(returncode, stdout, stderr), ...]`` for each command.
    """
    _validate_commands(commands)

    results: List[Tuple[int, str, str]] = []
    for cmd in commands:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )
        results.append((completed.returncode, completed.stdout, completed.stderr))
    return results


__all__ = ["run_pipe", "run_chain"]