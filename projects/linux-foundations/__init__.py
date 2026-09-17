"""
Linux Foundations Package

Provides utilities and information related to fundamental Linux concepts.
"""

from __future__ import annotations

__all__: list[str] = ["get_linux_fundamentals"]


def get_linux_fundamentals() -> list[str]:
    """
    Return a list of core Linux fundamentals topics.

    Returns
    -------
    list of str
        Topics that cover essential Linux knowledge.
    """
    return [
        "File system hierarchy",
        "Permissions and ownership",
        "Process management",
        "Package management",
        "Shell basics",
        "Networking basics",
        "User and group management",
        "System logging",
        "System services (systemd)",
        "Security basics",
    ]