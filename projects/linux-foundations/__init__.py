"""
Top‑level package for the *linux‑foundations* project.

The public API re‑exports the most commonly used helpers so that they can
be imported directly from ``linux_foundations``.
"""

from .archives import (
    create_tar,
    extract_tar,
    create_zip,
    extract_zip,
    compress_gzip,
    decompress_gzip,
    compress_bzip2,
    decompress_bzip2,
)

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