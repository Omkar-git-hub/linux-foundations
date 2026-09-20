"""
Utility functions for demonstrating Unix pipes and command chaining using the
standard library ``subprocess`` module.

The functions are intentionally simple and are meant for educational purposes
in the *Day 7 – Learn Pipes and Command Chaining* lesson.
"""

from __future__ import annotations

import subprocess
from typing import List


def run_pipeline(commands: List[List[str]], capture_stderr: bool = False) -> str:
    """
    Execute a series of commands connected by Unix pipes.

    Parameters
    ----------
    commands:
        A list where each element is a command represented as a list of strings,
        e.g. ``[['echo', 'hello'], ['grep', 'h']]``.
    capture_stderr:
        If ``True`` the standard error of the *last* command is appended to the
        returned output. Errors from intermediate commands are ignored for
        simplicity.

    Returns
    -------
    str
        The decoded standard output of the final command in the pipeline.

    Raises
    ------
    ValueError
        If ``commands`` is empty.
    subprocess.CalledProcessError
        If the final command exits with a non‑zero status and ``check=True`` is
        desired.  The implementation currently does not raise on intermediate
        failures; they are allowed to propagate naturally.
    """
    if not commands:
        raise ValueError("At least one command must be supplied to run_pipeline")

    processes: List[subprocess.Popen] = []
    previous_proc: subprocess.Popen | None = None

    for i, cmd in enumerate(commands):
        # The stdin of the current process is the stdout of the previous one,
        # unless this is the first command.
        stdin = previous_proc.stdout if previous_proc else None

        # For the last command we may want to capture stderr based on the flag.
        stderr = subprocess.PIPE if (i == len(commands) - 1 and capture_stderr) else subprocess.DEVNULL

        proc = subprocess.Popen(
            cmd,
            stdin=stdin,
            stdout=subprocess.PIPE,
            stderr=stderr,
            text=True,
        )

        # Close the stdout of the previous process in the parent so that the
        # pipe is properly broken when the child finishes.
        if previous_proc:
            previous_proc.stdout.close()  # type: ignore[assignment]

        processes.append(proc)
        previous_proc = proc

    # ``communicate`` on the last process retrieves its output (and optional stderr).
    final_stdout, final_stderr = processes[-1].communicate()

    # Ensure all earlier processes have terminated.
    for proc in processes[:-1]:
        proc.wait()

    if capture_stderr and final_stderr:
        return final_stdout + final_stderr
    return final_stdout


def chain_commands(commands: List[str], shell: bool = False) -> str:
    """
    Execute a list of commands sequentially, concatenating their standard output.

    This mimics simple command chaining (e.g. ``cmd1 && cmd2 && cmd3``) without
    involving the shell's ``&&`` or ``;`` operators.  Each command is executed
    independently; if any command fails (non‑zero return code) a
    ``subprocess.CalledProcessError`` is raised.

    Parameters
    ----------
    commands:
        A list of command strings.  When ``shell=False`` each string is split
        using ``shlex.split`` to obtain the argument list.
    shell:
        Whether to execute each command through the system shell.  When ``True``,
        the command strings are passed directly to ``subprocess.run`` with
        ``shell=True``.

    Returns
    -------
    str
        The concatenated standard output of all commands.
    """
    import shlex

    combined_output: List[str] = []

    for cmd in commands:
        if shell:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                check=True,
            )
        else:
            args = shlex.split(cmd)
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                check=True,
            )
        combined_output.append(result.stdout)

    return "".join(combined_output)


__all__ = ["run_pipeline", "chain_commands"]