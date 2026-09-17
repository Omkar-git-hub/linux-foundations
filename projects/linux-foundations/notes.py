"""
Notes on working with files and directories.

This module provides a simple utility to retrieve a multi‑line string
containing best‑practice notes for common file and directory operations
in Python. The notes are intended for educational purposes and can be
used by other parts of the project or displayed in documentation tools.

Typical usage
-------------
>>> from projects.linux_foundations.notes import get_notes
>>> print(get_notes())
"""

from __future__ import annotations

__all__: list[str] = ["get_notes"]


def get_notes() -> str:
    """
    Return a formatted string with notes about handling files and directories.

    The notes cover:

    * Opening files with ``with`` statements to ensure proper closure.
    * Using ``pathlib.Path`` for path manipulations.
    * Creating directories safely with ``Path.mkdir(parents=True, exist_ok=True)``.
    * Reading and writing text versus binary data.
    * Common pitfalls such as forgetting to close files or handling
      ``FileNotFoundError`` and ``PermissionError``.
    * Using ``shutil`` for high‑level operations like copying or removing
      entire directory trees.

    Returns
    -------
    str
        The multi‑line notes string.
    """
    notes = """
File and Directory Handling Notes
=================================

1. Use ``pathlib`` over ``os.path``:
   - ``Path`` objects provide methods like ``read_text()``, ``write_text()``,
     ``iterdir()``, and ``glob()``.
   - Example:
     >>> from pathlib import Path
     >>> p = Path('example.txt')
     >>> p.write_text('Hello, world!')
     >>> content = p.read_text()

2. Always open files using a context manager:
   - Guarantees the file is closed even if an exception occurs.
   - Example:
     >>> with open('data.bin', 'rb') as f:
     ...     data = f.read()

3. Creating directories:
   - ``Path.mkdir(parents=True, exist_ok=True)`` creates all missing parents
     and does not raise an error if the directory already exists.
   - Example:
     >>> Path('logs/2024/09').mkdir(parents=True, exist_ok=True)

4. Deleting files and directories:
   - Use ``Path.unlink()`` for files.
   - Use ``shutil.rmtree()`` for directories with contents.
   - Example:
     >>> import shutil
     >>> shutil.rmtree('old_folder')

5. Copying files and directories:
   - ``shutil.copy2(src, dst)`` preserves metadata.
   - ``shutil.copytree(src, dst)`` copies an entire directory tree.
   - Example:
     >>> shutil.copy2('config.yaml', 'backup/config.yaml')

6. Handling errors:
   - Catch ``FileNotFoundError`` when a path may not exist.
   - Catch ``PermissionError`` when lacking access rights.
   - Example:
     >>> try:
     ...     Path('secret.txt').read_text()
     ... except FileNotFoundError:
     ...     print('File does not exist')
     ... except PermissionError:
     ...     print('Insufficient permissions')

7. Working with binary data:
   - Open files with ``'rb'`` or ``'wb'`` modes.
   - Use ``bytes`` objects for manipulation.
   - Example:
     >>> with open('image.png', 'rb') as img:
     ...     raw = img.read()

8. Temporary files and directories:
   - ``tempfile.NamedTemporaryFile`` and ``tempfile.TemporaryDirectory``
     provide safe, auto‑cleaned resources.
   - Example:
     >>> import tempfile
     >>> with tempfile.TemporaryDirectory() as tmpdir:
     ...     Path(tmpdir, 'temp.txt').write_text('temp data')
"""
    return notes.strip()