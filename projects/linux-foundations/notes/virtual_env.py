"""
Virtual Environment Notes

This module provides a helper to retrieve concise notes on creating,
activating, and managing Python virtual environments using the standard
`venv` module as well as brief mentions of alternative tools.
"""

from __future__ import annotations

__all__: list[str] = ["get_notes"]


def get_notes() -> str:
    """
    Return a formatted string containing practical notes on Python virtual
    environments.

    The notes cover:

    * Creating a virtual environment with the built‑in ``venv`` module.
    * Activating the environment on different shells.
    * Installing packages inside the environment.
    * Common pitfalls and best practices.
    * Brief overview of alternative tools (``virtualenv``, ``pipenv``,
      ``poetry``).

    Returns
    -------
    str
        Multi‑line string with the virtual‑environment guidance.
    """
    return """\
# Python Virtual Environment (venv) Notes

## Creating a virtual environment
```bash
# Create a new environment in the directory 'venv'
python3 -m venv venv
```
* Uses the interpreter that runs the command.
* The created directory contains a copy of the interpreter and a
  ``site-packages`` directory isolated from the global Python install.

## Activating the environment
### Bash / Zsh / sh
```bash
source venv/bin/activate
```
### Fish
```fish
source venv/bin/activate.fish
```
### Csh / Tcsh
```csh
source venv/bin/activate.csh
```
### PowerShell
```powershell
.\venv\Scripts\Activate.ps1
```

After activation, your shell prompt usually changes to indicate the
environment name, and ``python``/``pip`` refer to the isolated copies.

## Installing packages
```bash
pip install <package>
```
* Packages are installed into ``venv/lib/pythonX.Y/site-packages``.
* Use ``pip freeze > requirements.txt`` to record exact versions.
* Re‑install later with ``pip install -r requirements.txt``.

## Deactivating
```bash
deactivate
```
Restores the original ``PATH`` and interpreter.

## Common pitfalls
* **Do not** commit the ``venv`` directory to version control; add it to
  ``.gitignore``.
* If you see ``ImportError: No module named pip``, ensure the environment
  was created with the ``--with-pip`` flag (default for recent Python
  versions) or reinstall pip via ``python -m ensurepip``.
* When using IDEs, point the interpreter setting to
  ``venv/bin/python`` (or ``venv\\Scripts\\python.exe`` on Windows).

## Alternatives (quick overview)

| Tool          | Description                                 | When to use |
|---------------|---------------------------------------------|-------------|
| **virtualenv**| Back‑port of ``venv`` with extra features.  | Need Python < 3.3 or custom interpreter handling. |
| **pipenv**    | Combines virtualenv + Pipfile management.   | Preference for deterministic Pipfile.lock workflow. |
| **poetry**    | Full‑featured dependency & packaging tool.  | Modern projects requiring publishing to PyPI. |

For most simple projects, the built‑in ``venv`` module is sufficient
and keeps the workflow lightweight.

---"""