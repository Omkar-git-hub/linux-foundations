"""
Notes on using Python virtual environments on Linux.

This file is intended as a quick reference for developers learning how to
manage virtual environments from the command line and programmatically via
the :pymod:`projects.linux_foundations.virtual_env` module.

Key points
----------

1. **Creating an environment**
   ``python3 -m venv /path/to/env`` creates a directory containing a copy of
   the interpreter and a ``bin`` folder with ``activate`` scripts.

2. **Activating**
   In a POSIX shell: ``source /path/to/env/bin/activate``.
   The ``activate`` script modifies ``$PATH`` and sets ``VIRTUAL_ENV``.

3. **Installing packages**
   Once activated, ``pip install <package>`` installs into the environment.
   Without activation you can call the environment's pip directly:
   ``/path/to/env/bin/pip install <package>``.

4. **Deactivating**
   ``deactivate`` (available after activation) restores the original shell
   environment.

5. **Programmatic management**
   The :pymod:`projects.linux_foundations.virtual_env` module wraps the
   standard library ``venv`` module and common ``pip`` commands, allowing
   creation, activation command generation, package installation, and
   listing of installed packages from Python code.

Example usage
-------------

>>> from projects.linux_foundations.virtual_env import create_env, install_package, list_installed
>>> env = create_env("/tmp/myenv")
>>> install_package(env, "requests")
>>> "requests=="+list_installed(env)[0].split("==")[1]  # doctest: +SKIP
"""

# The notes module does not expose any runtime functionality; it exists for
# documentation purposes only.  Keeping the file importable allows tools such
# as ``pydoc`` to display its contents.