"""
Notes on command resolution and the ``PATH`` environment variable.

The notes are intended for human readers and are also imported by the test
suite to verify that the explanatory text is present and correctly formatted.
"""

from __future__ import annotations

import textwrap

NOTE = textwrap.dedent(
    """
    # Command Resolution

    In Unix‑like systems the shell searches for an executable by consulting the
    ``PATH`` environment variable.  ``PATH`` is a colon‑separated list of
    directories.  When you type a command such as ``ls`` the shell looks for an
    executable file named ``ls`` in each directory, in order, and runs the
    first match it finds.

    The ``projects.linux_foundations.command_resolution`` module implements this
    behaviour in pure Python.  The key functions are:

    * ``get_path_dirs()`` – returns the list of directories from ``PATH``.
    * ``is_executable(path)`` – checks whether a given path points to an
      executable file.
    * ``resolve_command(name)`` – returns the absolute path to the executable
      that would be run by the shell, or ``None`` if no match is found.

    The implementation also works on Windows.  On Windows the ``PATH``
    separator is a semicolon (``;``) and executability is determined by the
    ``PATHEXT`` environment variable (e.g. ``.EXE``, ``.BAT``).

    ## Example

    ```python
    from projects.linux_foundations.command_resolution import resolve_command

    python_path = resolve_command("python")
    if python_path:
        print(f"Python interpreter found at: {python_path}")
    else:
        print("Python not found in PATH")
    ```

    The function mirrors the behaviour of the ``which`` command and can be
    safely used in scripts that need to locate external tools.
    """
).strip()