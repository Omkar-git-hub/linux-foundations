"""
Special Permissions Notes

This module provides information about the special permission bits
available on Unix-like systems:

* Setuid (4xxx)
* Setgid (2xxx)
* Sticky (1xxx)

Each permission is represented by a :class:`SpecialPermission` data class
containing its symbolic name, octal mask and a short description.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class SpecialPermission:
    """Representation of a special permission bit."""

    name: str
    octal: int
    description: str


# Define the three classic special permission bits.
SETUID = SpecialPermission(
    name="setuid",
    octal=0o4000,
    description=(
        "When set on an executable, the process runs with the file owner's UID "
        "(usually root). This allows ordinary users to execute privileged programs."
    ),
)

SETGID = SpecialPermission(
    name="setgid",
    octal=0o2000,
    description=(
        "When set on an executable, the process runs with the file's GID. "
        "When set on a directory, newly created files inherit the directory's GID."
    ),
)

STICKY = SpecialPermission(
    name="sticky",
    octal=0o1000,
    description=(
        "When set on a directory, only the file's owner, the directory's owner, "
        "or root may delete or rename files within that directory. Commonly used on /tmp."
    ),
)

# Public collection of all special permissions.
SPECIAL_PERMISSIONS: List[SpecialPermission] = [SETUID, SETGID, STICKY]


def list_special_permissions() -> List[SpecialPermission]:
    """
    Return a list of all defined special permissions.

    Returns
    -------
    List[SpecialPermission]
        A shallow copy of the internal ``SPECIAL_PERMISSIONS`` list.
    """
    return list(SPECIAL_PERMISSIONS)


__all__ = [
    "SpecialPermission",
    "SETUID",
    "SETGID",
    "STICKY",
    "SPECIAL_PERMISSIONS",
    "list_special_permissions",
]