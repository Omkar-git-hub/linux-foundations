"""
Archive and compression utilities for the Linux Foundations project.

This module provides a small, well‑tested wrapper around the Python
standard‑library modules :pymod:`tarfile`, :pymod:`zipfile`,
:pymod:`gzip`, :pymod:`bz2` and :pymod:`shutil` to create and extract
archives as well as to compress and decompress single files.

All functions operate on ``str`` or :class:`pathlib.Path` objects and
raise the underlying exceptions (e.g. :class:`FileNotFoundError`,
:class:`OSError`) when something goes wrong – this mirrors the behaviour
of the standard library and keeps the API simple.
"""

from __future__ import annotations

import gzip
import bz2
import shutil
import tarfile
import zipfile
from pathlib import Path
from typing import Union

PathLike = Union[str, Path]

__all__ = [
    "create_tar",
    "extract_tar",
    "create_zip",
    "extract_zip",
    "compress_gzip",
    "decompress_gzip",
    "compress_bzip2",
    "decompress_bzip2",
]


def _to_path(p: PathLike) -> Path:
    """Convert a ``str`` or ``Path`` to a :class:`Path` instance."""
    return p if isinstance(p, Path) else Path(p)


def create_tar(source: PathLike, tar_path: PathLike, mode: str = "w:gz") -> None:
    """
    Create a tar (optionally compressed) archive from *source*.

    Parameters
    ----------
    source: PathLike
        File or directory to archive.
    tar_path: PathLike
        Destination tar file. The parent directory must exist.
    mode: str, optional
        Mode passed to :func:`tarfile.open`. Defaults to ``"w:gz"``
        (gzip‑compressed tar). Use ``"w:bz2"``, ``"w:xz"``, or ``"w"``
        for other compression types or no compression.
    """
    src_path = _to_path(source)
    tar_file = _to_path(tar_path)

    with tarfile.open(tar_file, mode) as tf:
        # ``arcname`` ensures that the archive does not contain absolute paths.
        tf.add(src_path, arcname=src_path.name)


def extract_tar(tar_path: PathLike, extract_path: PathLike) -> None:
    """
    Extract a tar archive to *extract_path*.

    Parameters
    ----------
    tar_path: PathLike
        Path to the tar (or tar.gz / tar.bz2 / tar.xz) file.
    extract_path: PathLike
        Directory where the archive will be extracted. It will be created
        if it does not already exist.
    """
    tar_file = _to_path(tar_path)
    dest = _to_path(extract_path)
    dest.mkdir(parents=True, exist_ok=True)

    with tarfile.open(tar_file, "r:*") as tf:
        tf.extractall(path=dest)


def create_zip(source: PathLike, zip_path: PathLike) -> None:
    """
    Create a zip archive from *source*.

    Parameters
    ----------
    source: PathLike
        File or directory to archive.
    zip_path: PathLike
        Destination ``.zip`` file. The parent directory must exist.
    """
    src_path = _to_path(source)
    zip_file = _to_path(zip_path)

    with zipfile.ZipFile(zip_file, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        if src_path.is_dir():
            for file_path in src_path.rglob("*"):
                if file_path.is_file():
                    # Store relative path inside the zip to avoid absolute paths.
                    zf.write(file_path, arcname=file_path.relative_to(src_path.parent))
        else:
            zf.write(src_path, arcname=src_path.name)


def extract_zip(zip_path: PathLike, extract_path: PathLike) -> None:
    """
    Extract a zip archive to *extract_path*.

    Parameters
    ----------
    zip_path: PathLike
        Path to the ``.zip`` file.
    extract_path: PathLike
        Directory where the archive will be extracted. It will be created
        if it does not already exist.
    """
    zip_file = _to_path(zip_path)
    dest = _to_path(extract_path)
    dest.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_file, mode="r") as zf:
        zf.extractall(path=dest)


def compress_gzip(source: PathLike, dest: PathLike) -> None:
    """
    Compress a single file using gzip.

    Parameters
    ----------
    source: PathLike
        File to compress.
    dest: PathLike
        Destination path for the ``.gz`` file. The parent directory must exist.
    """
    src_path = _to_path(source)
    dest_path = _to_path(dest)

    with src_path.open("rb") as f_in, gzip.open(dest_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)


def decompress_gzip(source: PathLike, dest: PathLike) -> None:
    """
    Decompress a gzip file.

    Parameters
    ----------
    source: PathLike
        ``.gz`` file to decompress.
    dest: PathLike
        Destination path for the decompressed file.
    """
    src_path = _to_path(source)
    dest_path = _to_path(dest)

    with gzip.open(src_path, "rb") as f_in, dest_path.open("wb") as f_out:
        shutil.copyfileobj(f_in, f_out)


def compress_bzip2(source: PathLike, dest: PathLike) -> None:
    """
    Compress a single file using bzip2.

    Parameters
    ----------
    source: PathLike
        File to compress.
    dest: PathLike
        Destination path for the ``.bz2`` file.
    """
    src_path = _to_path(source)
    dest_path = _to_path(dest)

    with src_path.open("rb") as f_in, bz2.open(dest_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)


def decompress_bzip2(source: PathLike, dest: PathLike) -> None:
    """
    Decompress a bzip2 file.

    Parameters
    ----------
    source: PathLike
        ``.bz2`` file to decompress.
    dest: PathLike
        Destination path for the decompressed file.
    """
    src_path = _to_path(source)
    dest_path = _to_path(dest)

    with bz2.open(src_path, "rb") as f_in, dest_path.open("wb") as f_out:
        shutil.copyfileobj(f_in, f_out)