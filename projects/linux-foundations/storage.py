"""
Disk and Storage Management utilities.

This module provides a small set of helpers for common storage‑related
tasks on Linux systems, such as retrieving disk usage statistics and
listing mounted filesystems.  The implementation relies only on the
Python standard library and therefore works without any third‑party
dependencies.

Typical usage::

    from projects.linux_foundations.storage import get_disk_usage, list_mounted_filesystems

    usage = get_disk_usage("/")          # shutil.disk_usage tuple
    mounts = list_mounted_filesystems()  # list of dicts
"""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class MountInfo:
    """Representation of a single mount entry from ``/proc/mounts``."""
    device: str
    mount_point: str
    fs_type: str
    options: str
    dump: int
    pass_num: int

    @classmethod
    def from_line(cls, line: str) -> "MountInfo":
        """
        Parse a line from ``/proc/mounts`` and return a :class:`MountInfo` instance.

        The format of each line is:
            device mount_point fs_type options dump pass

        Fields are space‑separated, but device and mount_point may contain
        escaped spaces (e.g. ``\\040``).  ``shlex.split`` correctly handles
        these escape sequences.
        """
        parts = shlex.split(line)
        if len(parts) != 6:
            raise ValueError(f"Unexpected /proc/mounts line format: {line!r}")
        device, mount_point, fs_type, options, dump, pass_num = parts
        return cls(
            device=device,
            mount_point=mount_point,
            fs_type=fs_type,
            options=options,
            dump=int(dump),
            pass_num=int(pass_num),
        )

    def as_dict(self) -> dict:
        """Return a dictionary representation suitable for JSON serialisation."""
        return {
            "device": self.device,
            "mount_point": self.mount_point,
            "fs_type": self.fs_type,
            "options": self.options,
            "dump": self.dump,
            "pass_num": self.pass_num,
        }


def get_disk_usage(path: str = "/") -> shutil.disk_usage:
    """
    Return disk usage statistics about the given *path*.

    The result is a ``shutil.disk_usage`` named tuple with attributes
    ``total``, ``used`` and ``free`` expressed in bytes.

    Parameters
    ----------
    path:
        Path to the filesystem for which statistics are required.
        Defaults to the root filesystem (``"/"``).

    Raises
    ------
    FileNotFoundError
        If *path* does not exist.
    PermissionError
        If the current user cannot access *path*.
    """
    return shutil.disk_usage(path)


def _run_command(command: List[str]) -> str:
    """
    Execute *command* and return its stdout as a string.

    The function raises ``subprocess.CalledProcessError`` if the command
    exits with a non‑zero status.
    """
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        text=True,
    )
    return result.stdout


def list_mounted_filesystems() -> List[MountInfo]:
    """
    Parse ``/proc/mounts`` and return a list of :class:`MountInfo` objects.

    This works on Linux systems where ``/proc/mounts`` is present.  On
    non‑Linux platforms an empty list is returned.
    """
    proc_mounts = "/proc/mounts"
    if not os.path.exists(proc_mounts):
        return []

    mounts: List[MountInfo] = []
    with open(proc_mounts, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                mounts.append(MountInfo.from_line(line))
            except ValueError:
                # Skip malformed lines but continue processing the rest.
                continue
    return mounts


def get_filesystem_usage(device: str) -> Tuple[int, int, int]:
    """
    Return the total, used and free space (in bytes) for the filesystem
    identified by *device*.

    The implementation uses the ``df`` command because the standard
    library does not expose a direct way to query a device without a
    mount point.  The function extracts the first line of output that
    matches the given device.

    Parameters
    ----------
    device:
        The block device name as it appears in ``/proc/mounts`` (e.g.
        ``/dev/sda1``).

    Returns
    -------
    tuple
        ``(total_bytes, used_bytes, free_bytes)``

    Raises
    ------
    RuntimeError
        If the device cannot be found in the ``df`` output.
    subprocess.CalledProcessError
        Propagated if the ``df`` command fails.
    """
    # ``df -B1`` reports sizes in bytes.
    output = _run_command(["df", "-B1", device])
    lines = output.strip().splitlines()
    if len(lines) < 2:
        raise RuntimeError(f"Unable to retrieve usage for device {device!r}")

    # The second line contains the data for the requested device.
    # Expected columns: Filesystem 1B-blocks Used Available Use% Mounted on
    parts = lines[1].split()
    if len(parts) < 6:
        raise RuntimeError(f"Unexpected df output format for device {device!r}")

    total, used, available = map(int, parts[1:4])
    return total, used, available


__all__ = [
    "MountInfo",
    "get_disk_usage",
    "list_mounted_filesystems",
    "get_filesystem_usage",
]