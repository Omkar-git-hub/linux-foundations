"""
Utility functions for advanced file I/O operations using low‑level file descriptors.

This module provides a thin wrapper around the :pymod:`os` module to work with
file descriptors directly.  The functions are deliberately small and focused
so they can be used in teaching examples and unit tests without pulling in
external dependencies.

Typical usage::

    from projects.linux_foundations.files import (
        open_file_descriptor,
        read_from_fd,
        write_to_fd,
        close_fd,
        duplicate_fd,
        fd_open,
    )

    # Write some data
    with fd_open('example.txt', 'w') as fd:
        write_to_fd(fd, b'Hello, world!')

    # Read it back
    with fd_open('example.txt', 'r') as fd:
        content = read_from_fd(fd).decode()
        assert content == 'Hello, world!'
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Generator, Iterable, Union

__all__ = [
    "open_file_descriptor",
    "read_from_fd",
    "write_to_fd",
    "close_fd",
    "duplicate_fd",
    "fd_open",
]


# Mapping of mode strings to os flags.
_MODE_FLAGS = {
    "r": os.O_RDONLY,
    "rb": os.O_RDONLY,
    "w": os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
    "wb": os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
    "a": os.O_WRONLY | os.O_CREAT | os.O_APPEND,
    "ab": os.O_WRONLY | os.O_CREAT | os.O_APPEND,
    "r+": os.O_RDWR,
    "rb+": os.O_RDWR,
    "r+b": os.O_RDWR,
    "w+": os.O_RDWR | os.O_CREAT | os.O_TRUNC,
    "wb+": os.O_RDWR | os.O_CREAT | os.O_TRUNC,
    "w+b": os.O_RDWR | os.O_CREAT | os.O_TRUNC,
    "a+": os.O_RDWR | os.O_CREAT | os.O_APPEND,
    "ab+": os.O_RDWR | os.O_CREAT | os.O_APPEND,
    "a+b": os.O_RDWR | os.O_CREAT | os.O_APPEND,
}


def open_file_descriptor(
    path: str,
    mode: str = "r",
    *,
    permissions: int = 0o666,
) -> int:
    """
    Open *path* using low‑level ``os.open`` and return the resulting file descriptor.

    Parameters
    ----------
    path: str
        Path to the file to open.
    mode: str, optional
        A string compatible with the built‑in ``open`` function (e.g. ``'r'``,
        ``'w'``, ``'a+'``).  Binary/text distinction does not affect the low‑level
        operation; the caller is responsible for encoding/decoding when needed.
    permissions: int, optional
        Permission bits used when the file is created (default ``0o666``).

    Returns
    -------
    int
        The file descriptor for the opened file.

    Raises
    ------
    ValueError
        If *mode* is not recognised.
    OSError
        Propagated from :func:`os.open` if the operation fails.
    """
    if mode not in _MODE_FLAGS:
        raise ValueError(f"Unsupported mode '{mode}'. Supported modes: {sorted(_MODE_FLAGS)}")
    flags = _MODE_FLAGS[mode]
    fd = os.open(path, flags, permissions)
    return fd


def read_from_fd(fd: int, size: int = -1) -> bytes:
    """
    Read up to *size* bytes from *fd*.

    If *size* is ``-1`` (the default) the function reads until EOF, returning
    all data as a single ``bytes`` object.

    Parameters
    ----------
    fd: int
        File descriptor to read from.
    size: int, optional
        Maximum number of bytes to read; ``-1`` means read until EOF.

    Returns
    -------
    bytes
        The data read from the descriptor.
    """
    if size == 0:
        return b""
    chunks: list[bytes] = []
    remaining = size
    while True:
        to_read = 8192 if remaining == -1 else min(8192, remaining)
        data = os.read(fd, to_read)
        if not data:
            break
        chunks.append(data)
        if remaining != -1:
            remaining -= len(data)
            if remaining <= 0:
                break
    return b"".join(chunks)


def write_to_fd(fd: int, data: Union[bytes, bytearray, memoryview]) -> int:
    """
    Write *data* to *fd*, ensuring that all bytes are written.

    Parameters
    ----------
    fd: int
        File descriptor to write to.
    data: bytes‑like
        The data to write.

    Returns
    -------
    int
        Total number of bytes written.

    Raises
    ------
    OSError
        If the underlying ``os.write`` fails.
    """
    view = memoryview(data)
    total_written = 0
    while total_written < len(view):
        written = os.write(fd, view[total_written:])
        if written == 0:
            raise OSError("os.write returned 0 bytes written, unable to continue")
        total_written += written
    return total_written


def close_fd(fd: int) -> None:
    """
    Close the file descriptor *fd* safely.

    Parameters
    ----------
    fd: int
        The descriptor to close.
    """
    try:
        os.close(fd)
    except OSError:
        # Silently ignore errors on close – this mirrors the behaviour of
        # ``file.close()`` which never raises on a second close.
        pass


def duplicate_fd(fd: int, inheritable: bool = False) -> int:
    """
    Duplicate *fd* using :func:`os.dup` and optionally set the inheritable flag.

    Parameters
    ----------
    fd: int
        File descriptor to duplicate.
    inheritable: bool, optional
        If ``True``, the duplicated descriptor will be marked as inheritable
        by child processes (default ``False``).

    Returns
    -------
    int
        The new file