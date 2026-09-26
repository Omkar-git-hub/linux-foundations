"""
Notes on the ``PATH`` environment variable.

These notes complement the implementation in
``projects.linux_foundations.command_resolution`` and provide a concise
reference for developers learning about command lookup on Unix‑like systems
and Windows.
"""

from __future__ import annotations

import textwrap

NOTE = textwrap.dedent(
    """
    # ``PATH`` Environment Variable

    ``PATH`` tells the operating system where to look for executable programs.
    It is a single string containing a list of directory paths separated by a
    platform‑specific delimiter:

    * **POSIX** – colon (``:``)
    * **Windows** – semicolon (``;``)

    Example (POSIX)::

        $ echo $PATH
        /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

    Example (Windows)::

        > echo %PATH%
        C:\\Windows\\system32;C:\\Windows;C:\\Program Files\\Git\\cmd

    The order matters: the system searches the directories from left to right
    and stops at the first matching executable.  Modifying ``PATH`` can be used
    to prioritize custom tools or to make newly installed programs available
    without specifying their full path.

    ## Manipulating ``PATH`` in Python

    ```python
    import os

    # Append a directory to PATH
    os.environ["PATH"] += os.pathsep + "/opt/mytools/bin"

    # Prepend a directory (higher priority)
    os.environ["PATH"] = "/opt/mytools/bin" + os.pathsep + os.environ["PATH"]
    ```

    Remember that changes to ``os.environ`` affect only the current process
    and any child processes it spawns; they do not modify the user's shell
    configuration.
    """
).strip()