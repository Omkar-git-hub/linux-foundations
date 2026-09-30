"""
File Descriptors Notes
======================

This module provides small helper utilities and documentation related to
file descriptors on Unix‑like systems.  It is intended for educational
purposes and to be used by other parts of the *linux‑foundations* package.

Typical usage
-------------

>>> from linux_foundations.notes.file_descriptors import get_fd_limit, set_fd_limit
>>> soft, hard = get_fd_limit()
>>> # Increase the soft limit (if permitted)
>>> set_fd_limit(soft + 1024)

The implementation relies on the :pymod:`resource` standard library module,
which is available on POSIX platforms.  On non‑POSIX platforms the functions
raise :class:`NotImplementedError`.
"""

from __future__ import annotations

import sys
from typing import Tuple

if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
    import resource

    def _get_limits() -> Tuple[int, int]:
        """Return the current (soft, hard) file descriptor limits."""
        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        return soft, hard

    def _set_limits(soft: int | None = None, hard: int | None = None) -> Tuple[int, int]:
        """Set new limits and return the updated (soft, hard) values.

        Parameters
        ----------
        soft:
            Desired soft limit.  If ``None`` the current soft limit is kept.
        hard:
            Desired hard limit.  If ``None`` the current hard limit is kept.

        Returns
        -------
        tuple[int, int]
            The new (soft, hard) limits after the operation.
        """
        cur_soft, cur_hard = _get_limits()
        new_soft = soft if soft is not None else cur_soft
        new_hard = hard if hard is not None else cur_hard
        # The soft limit cannot exceed the hard limit.
        if new_soft > new_hard:
            raise ValueError("soft limit cannot be greater than hard limit")
        resource.setrlimit(resource.RLIMIT_NOFILE, (new_soft, new_hard))
        return _get_limits()
else:
    # Non‑POSIX platforms do not support the ``resource`` module.
    def _get_limits() -> Tuple[int, int]:
        raise NotImplementedError("File descriptor limits are not supported on this platform")

    def _set_limits(soft: int | None = None, hard: int | None = None) -> Tuple[int, int]:
        raise NotImplementedError("File descriptor limits are not supported on this platform")


def get_fd_limit() -> Tuple[int, int]:
    """
    Retrieve the current soft and hard limits for the number of open file
    descriptors for the running process.

    Returns
    -------
    tuple[int, int]
        ``(soft_limit, hard_limit)`` where both values are integers.

    Raises
    ------
    NotImplementedError
        If the underlying platform does not support querying file descriptor
        limits.
    """
    return _get_limits()


def set_fd_limit(soft: int | None = None, hard: int | None = None) -> Tuple[int, int]:
    """
    Set new limits for the number of open file descriptors.

    Parameters
    ----------
    soft :
        Desired soft limit.  If ``None`` the existing soft limit is retained.
    hard :
        Desired hard limit.  If ``None`` the existing hard limit is retained.

    Returns
    -------
    tuple[int, int]
        The updated ``(soft_limit, hard_limit)`` after applying the change.

    Raises
    ------
    ValueError
        If the requested soft limit exceeds the hard limit.
    NotImplementedError
        If the platform does not support modifying file descriptor limits.
    """
    return _set_limits(soft=soft, hard=hard)