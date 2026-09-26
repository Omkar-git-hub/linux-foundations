"""
Notes on archives and compression for Linux Foundations.

This module does not provide executable code; it serves as documentation
that can be imported for reference in interactive sessions or notebooks.
"""

ARCHIVE_NOTES = """
Archives are containers that bundle multiple files and directories into a
single file. Common archive formats on Linux include:

* **tar** – Tape Archive. By itself it stores files without compression.
  It is often combined with a compressor:
    - ``tar -czf`` → gzip compression (``.tar.gz`` or ``.tgz``)
    - ``tar -cjf`` → bzip2 compression (``.tar.bz2``)
    - ``tar -cJf`` → xz compression (``.tar.xz``)

* **zip** – Provides both archiving and compression in one step.
  Widely used on Windows and supported natively on most Linux tools.

Key commands:

```
# Create a gzip‑compressed tarball of a directory
tar -czf archive.tar.gz /path/to/dir

# Extract a tarball
tar -xzf archive.tar.gz -C /target/dir

# Create a zip archive
zip -r archive.zip /path/to/dir

# Extract a zip archive
unzip archive.zip -d /target/dir
```

Python's standard library mirrors these utilities:

* :pymod:`tarfile` – read/write tar, tar.gz, tar.bz2, tar.xz.
* :pymod:`zipfile` – read/write zip archives.
* :pymod:`gzip`, :pymod:`bz2`, :pymod:`lzma` – stream‑oriented compressors.

When scripting, prefer the high‑level helpers in
``projects.linux_foundations.archives`` which wrap the stdlib modules
and provide a consistent ``Path``‑based API.
"""

def get_notes() -> str:
    """Return the archive and compression notes as a string."""
    return ARCHIVE_NOTES.strip()