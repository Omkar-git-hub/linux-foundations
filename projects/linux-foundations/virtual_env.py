"""
Virtual Environment Utilities

This module provides higher‑level utilities that operate on Python
virtual environments. It is deliberately lightweight and relies only
on the standard library.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List, Sequence

__all__: list[str] = [
    "create_venv",
    "activate_script_path",
    "install_packages",
    "list_installed_packages",
]


def create_venv(path: str | os.PathLike, *, with_pip: bool = True) -> Path:
    """
    Create a Python virtual environment at ``path`` using the ``venv`` module.

    Parameters
    ----------
    path : str | os.PathLike
        Destination directory for the virtual environment.
    with_pip : bool, optional
        Ensure ``pip`` is installed in the new environment (default is ``True``).

    Returns
    -------
    pathlib.Path
        The absolute path to the created virtual environment.
    """
    venv_path = Path(path).expanduser().resolve()
    # ``python -m venv`` creates the environment; ``--without-pip`` disables pip.
    cmd: List[str] = [sys.executable, "-m", "venv"]
    if not with_pip:
        cmd.append("--without-pip")
    cmd.append(str(venv_path))
    subprocess.run(cmd, check=True)
    return venv_path


def activate_script_path(venv_path: str | os.PathLike, shell: str = "bash") -> Path:
    """
    Return the path to the activation script for a given shell.

    Parameters
    ----------
    venv_path : str | os.PathLike
        Path to the virtual environment directory.
    shell : str, optional
        Shell type (``bash``, ``fish``, ``csh``, ``powershell``). Defaults to ``bash``.

    Returns
    -------
    pathlib.Path
        Path to the appropriate activation script.
    """
    venv = Path(venv_path).expanduser().resolve()
    scripts = {
        "bash": venv / "bin" / "activate",
        "zsh": venv / "bin" / "activate",
        "sh": venv / "bin" / "activate",
        "fish": venv / "bin" / "activate.fish",
        "csh": venv / "bin" / "activate.csh",
        "tcsh": venv / "bin" / "activate.csh",
        "powershell": venv / "Scripts" / "Activate.ps1",
        "cmd": venv / "Scripts" / "activate.bat",
    }
    script = scripts.get(shell.lower())
    if script is None or not script.exists():
        raise FileNotFoundError(f"Activation script for shell '{shell}' not found.")
    return script


def install_packages(
    venv_path: str | os.PathLike,
    packages: Sequence[str],
    *,
    upgrade: bool = False,
    index_url: str | None = None,
) -> None:
    """
    Install one or more packages into the virtual environment using ``pip``.

    Parameters
    ----------
    venv_path : str | os.PathLike
        Path to the virtual environment.
    packages : Sequence[str]
        Iterable of package specifications (e.g., ``["requests", "flask==2.0"]``).
    upgrade : bool, optional
        Pass ``--upgrade`` to ``pip`` to upgrade already‑installed packages.
    index_url : str | None, optional
        Custom Python Package Index URL (e.g., a private repository).

    Raises
    ------
    subprocess.CalledProcessError
        If the ``pip`` command fails.
    """
    if not packages:
        return

    venv = Path(venv_path).expanduser().resolve()
    pip_executable = venv / ("Scripts" if os.name == "nt" else "bin") / "pip"
    cmd: List[str] = [str(pip_executable), "install"]
    if upgrade:
        cmd.append("--upgrade")
    if index_url:
        cmd.extend(["--index-url", index_url])
    cmd.extend(packages)
    subprocess.run(cmd, check=True)


def list_installed_packages(venv_path: str | os.PathLike) -> List[str]:
    """
    Return a list of installed packages (``pkg==version``) inside the virtual environment.

    Parameters
    ----------
    venv_path : str | os.PathLike
        Path to the virtual environment.

    Returns
    -------
    list[str]
        List of package specifications as reported by ``pip list --format=freeze``.
    """
    venv = Path(venv_path).expanduser().resolve()
    pip_executable = venv / ("Scripts" if os.name == "nt" else "bin") / "pip"
    result = subprocess.run(
        [str(pip_executable), "list", "--format=freeze"],
        check=True,
        capture_output=True,
        text=True,
    )
    lines = result.stdout.strip().splitlines()
    return [line for line in lines if line]