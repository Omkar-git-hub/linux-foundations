"""
Notes on Linux process management.

This module provides a concise reference for common process‑related
commands and concepts that are useful when working with Linux systems.
It is intended to be imported by the higher‑level ``notes`` module or
used directly in educational scripts.

The notes cover:

* Process identifiers (PID, PPID)
* Foreground vs background jobs
* Job control signals (SIGSTOP, SIGCONT, SIGTERM, SIGKILL)
* Common utilities: ``ps``, ``top``, ``htop``, ``kill``, ``pkill``,
  ``pgrep``, ``nice``, ``renice``, ``nohup``, ``screen``, ``tmux``
* The ``/proc`` filesystem for inspecting process details
* Creating and managing processes in Python via the ``subprocess`` module
"""

from __future__ import annotations

from typing import List


def _format_command(name: str, description: str) -> str:
    """Return a formatted one‑line description for a command."""
    return f"{name:<12} – {description}"


def get_processes_notes() -> str:
    """
    Return a formatted string containing the process notes.

    The function assembles the notes into a human‑readable block that can be
    printed to the console or written to a file.

    Returns
    -------
    str
        Multi‑line string with process management notes.
    """
    sections: List[str] = []

    # Basic identifiers
    sections.append("Identifiers")
    sections.append("- PID  : Process ID (unique per running process)")
    sections.append("- PPID : Parent Process ID")
    sections.append("- PGID : Process Group ID")
    sections.append("- SID  : Session ID")
    sections.append("")

    # Job control
    sections.append("Job Control")
    sections.append(_format_command("bg", "Resume a stopped job in the background"))
    sections.append(_format_command("fg", "Bring a background job to the foreground"))
    sections.append(_format_command("jobs", "List current jobs with their status"))
    sections.append("")

    # Signals
    sections.append("Signals")
    sections.append(_format_command("SIGSTOP", "Stop (pause) a process"))
    sections.append(_format_command("SIGCONT", "Continue a stopped process"))
    sections.append(_format_command("SIGTERM", "Graceful termination request"))
    sections.append(_format_command("SIGKILL", "Forceful termination (cannot be caught)"))
    sections.append("")

    # Common utilities
    sections.append("Common Utilities")
    utilities = [
        ("ps", "Report a snapshot of current processes"),
        ("top", "Interactive real‑time process monitor"),
        ("htop", "Improved interactive process viewer"),
        ("kill", "Send a signal to a process by PID"),
        ("pkill", "Send a signal to processes matching a name pattern"),
        ("pgrep", "Search for processes by name and return their PIDs"),
        ("nice", "Run a command with modified scheduling priority"),
        ("renice", "Change priority of an existing process"),
        ("nohup", "Run a command immune to hangups, with output to nohup.out"),
        ("screen", "Terminal multiplexer for detachable sessions"),
        ("tmux", "Another terminal multiplexer, modern alternative to screen"),
    ]
    for cmd, desc in utilities:
        sections.append(_format_command(cmd, desc))
    sections.append("")

    # /proc filesystem
    sections.append("/proc Filesystem")
    sections.append("- /proc/<pid>/cmdline : Command line arguments")
    sections.append("- /proc/<pid>/status  : Human‑readable status information")
    sections.append("- /proc/<pid>/fd/*    : Open file descriptors")
    sections.append("- /proc/<pid>/maps   : Memory mappings")
    sections.append("")

    # Python subprocess basics
    sections.append("Python subprocess")
    sections.append("- subprocess.run([...]) : Run a command and wait")
    sections.append("- subprocess.Popen([...]) : Launch a process without waiting")
    sections.append("- capture_output=True   : Capture stdout/stderr")
    sections.append("- check=True            : Raise CalledProcessError on non‑zero exit")
    sections.append("")

    return "\n".join(sections)


if __name__ == "__main__":
    # When executed directly, print the notes to stdout.
    print(get_processes_notes())