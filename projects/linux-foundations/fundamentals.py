"""
Linux Fundamentals utilities.

This module provides simple helper functions that expose basic Linux
knowledge such as common command names and their short descriptions.
The functions are deliberately lightweight and rely only on the Python
standard library so they can be used in educational contexts or unit
tests without external dependencies.
"""

from __future__ import annotations

from typing import Dict, List, Optional

# Mapping of a few essential Linux commands to a short description.
_COMMAND_DESCRIPTIONS: Dict[str, str] = {
    "ls": "List directory contents",
    "cd": "Change the current directory",
    "pwd": "Print the current working directory",
    "mkdir": "Create a new directory",
    "rm": "Remove files or directories",
    "cp": "Copy files and directories",
    "mv": "Move/rename files and directories",
    "cat": "Concatenate and display file contents",
    "echo": "Display a line of text",
    "chmod": "Change file mode (permissions)",
    "chown": "Change file owner and group",
    "grep": "Search text using patterns",
    "find": "Search for files in a directory hierarchy",
    "tar": "Archive files",
    "ssh": "Secure Shell remote login",
    "sudo": "Execute a command as another user, typically root",
    "apt": "Advanced Package Tool (Debian/Ubuntu package manager)",
    "yum": "Yellowdog Updater, Modified (RHEL/CentOS package manager)",
    "systemctl": "Control the systemd system and service manager",
    "ps": "Report a snapshot of current processes",
    "top": "Display Linux tasks",
    "kill": "Send signals to processes",
    "df": "Report file system disk space usage",
    "du": "Estimate file space usage",
    "whoami": "Print effective user ID",
    "uname": "Print system information",
    "date": "Display or set the system date and time",
    "uptime": "Show how long the system has been running",
    "ifconfig": "Configure network interfaces (deprecated in favor of ip)",
    "ip": "Show/manipulate routing, devices, policy routing and tunnels",
    "ping": "Send ICMP ECHO_REQUEST to network hosts",
    "wget": "Retrieve files from the web",
    "curl": "Transfer data from or to a server",
    "nano": "Simple text editor",
    "vim": "Vi IMproved, a powerful text editor",
    "git": "Distributed version control system",
}


def list_basic_commands() -> List[str]:
    """
    Return a sorted list of basic Linux command names that are covered by
    this module.

    Returns
    -------
    List[str]
        Alphabetically sorted command names.
    """
    return sorted(_COMMAND_DESCRIPTIONS.keys())


def command_description(command: str) -> Optional[str]:
    """
    Retrieve a short description for a given Linux command.

    Parameters
    ----------
    command : str
        The command name (e.g., ``'ls'``). Case‑sensitive; the keys in the
        internal dictionary are lower‑case.

    Returns
    -------
    Optional[str]
        The description if the command is known, otherwise ``None``.
    """
    return _COMMAND_DESCRIPTIONS.get(command)


def is_absolute_path(path: str) -> bool:
    """
    Determine whether a given path string is an absolute Linux path.

    An absolute path in Linux starts with the forward slash ``'/'``.
    This function does not perform any filesystem checks; it only
    analyses the string format.

    Parameters
    ----------
    path : str
        Path string to evaluate.

    Returns
    -------
    bool
        ``True`` if the path is absolute, ``False`` otherwise.
    """
    return isinstance(path, str) and path.startswith("/")


__all__ = [
    "list_basic_commands",
    "command_description",
    "is_absolute_path",
]