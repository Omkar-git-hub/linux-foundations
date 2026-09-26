"""
Utility functions for creating and extracting archive files.

Supported formats:
- tar (optionally gzipped or bzipped)
- zip

The functions operate on pathlib.Path objects for convenience and type safety.
"""

from __future__ import annotations

import tarfile
import zipfile
from pathlib import Path
from typing import Iterable, Union

PathLike = Union[str, Path]


def _ensure_path(path: PathLike) -> Path:
    """Convert a path-like object to a pathlib.Path and expand user/home."""
    return Path(path).expanduser().resolve()


def create_tar(
    source: PathLike,
    output: PathLike,
    *,
    mode: str = "w:gz",
    include: Iterable[PathLike] | None = None,
) -> None:
    """
    Create a tar archive from ``source``.

    Parameters
    ----------
    source : PathLike
        Directory (or file) to archive.
    output : PathLike
        Destination tar file. The parent directory is created if it does not exist.
    mode : str, optional
        Mode passed to :class:`tarfile.TarFile`. Common values:
        ``"w"`` – uncompressed tar,
        ``"w:gz"`` – gzip compressed (default),
        ``"w:bz2"`` – bzip2 compressed,
        ``"w:xz"`` – lzma compressed.
    include : iterable of PathLike, optional
        If provided, only the specified paths (relative to ``source``) are added.
        Useful for selective archiving.

    Raises
    ------
    FileNotFoundError
        If ``source`` does not exist.
    """
    src_path = _ensure_path(source)
    out_path = _ensure_path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not src_path.exists():
        raise FileNotFoundError(f"Source path does not exist: {src_path}")

    with tarfile.open(out_path, mode) as tar:
        if include is None:
            tar.add(src_path, arcname=src_path.name)
        else:
            for rel in include:
                rel_path = src_path / rel
                if not rel_path.exists():
                    raise FileNotFoundError(f"Included path does not exist: {rel_path}")
                tar.add(rel_path, arcname=rel_path.relative_to(src_path.parent))


def extract_tar(archive: PathLike, destination: PathLike) -> None:
    """
    Extract a tar archive to ``destination``.

    Parameters
    ----------
    archive : PathLike
        Path to the tar (or compressed tar) file.
    destination : PathLike
        Directory where the archive will be extracted. It is created if missing.

    Raises
    ------
    FileNotFoundError
        If ``archive`` does not exist.
    tarfile.TarError
        If the archive cannot be read.
    """
    archive_path = _ensure_path(archive)
    dest_path = _ensure_path(destination)
    dest_path.mkdir(parents=True, exist_ok=True)

    if not archive_path.is_file():
        raise FileNotFoundError(f"Archive not found: {archive_path}")

    with tarfile.open(archive_path, "r:*") as tar:
        tar.extractall(path=dest_path)


def create_zip(
    source: PathLike,
    output: PathLike,
    *,
    include: Iterable[PathLike] | None = None,
    compression: int = zipfile.ZIP_DEFLATED,
) -> None:
    """
    Create a zip archive from ``source``.

    Parameters
    ----------
    source : PathLike
        Directory (or file) to archive.
    output : PathLike
        Destination zip file. Parent directories are created automatically.
    include : iterable of PathLike, optional
        If supplied, only these relative paths (to ``source``) are added.
    compression : int, optional
        Compression method; defaults to ``ZIP_DEFLATED`` (standard zip compression).

    Raises
    ------
    FileNotFoundError
        If ``source`` does not exist.
    """
    src_path = _ensure_path(source)
    out_path = _ensure_path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not src_path.exists():
        raise FileNotFoundError(f"Source path does not exist: {src_path}")

    with zipfile.ZipFile(out_path, mode="w", compression=compression) as zf:
        if include is None:
            if src_path.is_dir():
                for file_path in src_path.rglob("*"):
                    if file_path.is_file():
                        arcname = file_path.relative_to(src_path.parent)
                        zf.write(file_path, arcname)
            else:
                zf.write(src_path, src_path.name)
        else:
            for rel in include:
                rel_path = src_path / rel
                if not rel_path.exists():
                    raise FileNotFoundError(f"Included path does not exist: {rel_path}")
                arcname = rel_path.relative_to(src_path.parent)
                if rel_path.is_dir():
                    for file_path in rel_path.rglob("*"):
                        if file_path.is_file():
                            arcname = file_path.relative_to(src_path.parent)
                            zf.write(file_path, arcname)
                else:
                    zf.write(rel_path, arcname)


def extract_zip(archive: PathLike, destination: PathLike) -> None:
    """
    Extract a zip archive to ``destination``.

    Parameters
    ----------
    archive : PathLike
        Path to the zip file.
    destination : PathLike
        Directory where files will be extracted. Created if missing.

    Raises
    ------
    FileNotFoundError
        If ``archive`` does not exist.
    zipfile.BadZipFile
        If the archive is not a valid zip file.
    """
    archive_path = _ensure_path(archive)
    dest_path = _ensure_path(destination)
    dest_path.mkdir(parents=True, exist_ok=True)

    if not archive_path.is_file():
        raise FileNotFoundError(f"Archive not found: {archive_path}")

    with zipfile.ZipFile(archive_path, "r") as zf:
        zf.extractall(path=dest_path)


__all__ = [
    "create_tar",
    "extract_tar",
    "create_zip",
    "extract_zip",
]