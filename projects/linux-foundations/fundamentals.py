"""
Linux Fundamentals Notes Module.

This module provides a concise collection of notes covering essential
Linux concepts. The notes are stored as a dictionary mapping a topic
title to a short description. Helper functions are provided to retrieve
the notes programmatically or to display them in a readable format.
"""

from __future__ import annotations

from typing import Dict


def get_fundamentals() -> Dict[str, str]:
    """
    Return a dictionary of Linux fundamental topics and their brief notes.

    Returns
    -------
    Dict[str, str]
        Mapping where the key is the topic title and the value is a short
        description of that topic.
    """
    return {
        "Kernel": (
            "The core of the operating system, managing hardware, processes, "
            "memory, and system calls."
        ),
        "Shell": (
            "Command‑line interface that interprets user commands; common shells "
            "include bash, zsh, and fish."
        ),
        "File System Hierarchy": (
            "Standard directory layout defined by the Filesystem Hierarchy Standard "
            "(FHS), e.g., /, /bin, /etc, /home, /var, /tmp, /usr."
        ),
        "Permissions": (
            "Read (r), write (w), execute (x) bits for user, group, and others; "
            "managed with chmod, chown, and chgrp."
        ),
        "Process Management": (
            "Processes identified by PID; commands like ps, top, kill, nice, "
            "renice, and systemd for services."
        ),
        "Package Management": (
            "Tools to install, update, and remove software; apt (Debian/Ubuntu), "
            "yum/dnf (RHEL/Fedora), pacman (Arch)."
        ),
        "Networking": (
            "Configuration via ifconfig/ip, netplan, systemd‑networkd; utilities "
            "such as ping, traceroute, ssh, and netstat."
        ),
        "System Logging": (
            "Logs stored in /var/log; managed by syslog or journald; view with "
            "journalctl."
        ),
        "Boot Process": (
            "BIOS/UEFI → bootloader (GRUB) → kernel → init system (systemd) → "
            "services."
        ),
        "Users and Groups": (
            "User accounts in /etc/passwd, groups in /etc/group; manage with "
            "useradd, groupadd, and passwd."
        ),
    }


def format_fundamentals() -> str:
    """
    Produce a formatted multi‑line string of all Linux fundamentals notes.

    Returns
    -------
    str
        Human‑readable representation of the notes, suitable for printing.
    """
    notes = get_fundamentals()
    lines = ["Linux Fundamentals:\n"]
    for title, content in notes.items():
        lines.append(f"{title}:\n    {content}\n")
    return "\n".join(lines)


def print_fundamentals() -> None:
    """
    Print the formatted Linux fundamentals notes to standard output.
    """
    print(format_fundamentals())