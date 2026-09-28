"""
Utility functions for managing Python virtual environments on Linux.

This module provides a thin wrapper around the standard library :mod:`venv`
module and common ``pip`` commands to create, activate, and manage virtual
environments programmatically.

Typical usage::

    from projects.linux_foundations.virtual_env import (
        create_env,
        activate_env,
        install_package,
        list_installed,
    )

    env_path = create_env("/tmp/myenv")
    activation_cmd = activate_env(env_path)
    install_package(env_path, "requests")
    packages = list_installed(env_path)
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List

import venv

__all__ = [
    "create_env",
    "activate_env",
    "install_package",
    "list_installed",
]


def create_env(path: str | Path, *, python_executable: str = sys.executable) -> Path:
    """
    Create a new virtual environment at *path*.

    Parameters
    ----------
    path: str | Path
        Destination directory for the virtual environment.
    python_executable: str, optional
        Path to the Python interpreter to use for the environment.
        Defaults to the interpreter running this code.

    Returns
    -------
    pathlib.Path
        Absolute path to the created virtual environment directory.

    Raises
    ------
    subprocess.CalledProcessError
        If the underlying ``python -m venv`` command fails.
    """
    env_path = Path(path).expanduser().resolve()
    builder = venv.EnvBuilder(with_pip=True, clear=True, symlinks=True, upgrade_deps=True)
    # The EnvBuilder does not expose a direct way to specify a custom interpreter,
    # so we invoke the interpreter explicitly via subprocess.
    subprocess.run(
        [python_executable, "-m", "venv", str(env_path)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # Ensure pip is up‑to‑date
    pip_path = env_path / "bin" / "pip"
    subprocess.run([str(pip_path), "install", "--upgrade", "pip"], check=False)
    return env_path


def activate_env(env_path: str | Path) -> str:
    """
    Return the shell command required to activate the virtual environment.

    The function does **not** modify the current process environment; it simply
    provides the command that a user would type in a POSIX shell.

    Parameters
    ----------
    env_path: str | Path
        Path to the virtual environment directory.

    Returns
    -------
    str
        The command string, e.g. ``source /path/to/env/bin/activate``.
    """
    env_path = Path(env_path).expanduser().resolve()
    activate_script = env_path / "bin" / "activate"
    return f"source {activate_script}"


def _run_pip(env_path: Path, args: List[str]) -> subprocess.CompletedProcess:
    """
    Helper to invoke the environment's ``pip`` with the given arguments.
    """
    pip_executable = env_path / "bin" / "pip"
    return subprocess.run([str(pip_executable), *args], capture_output=True, text=True, check=False)


def install_package(env_path: str | Path, package: str, *, upgrade: bool = False) -> None:
    """
    Install *package* into the virtual environment.

    Parameters
    ----------
    env_path: str | Path
        Path to the virtual environment.
    package: str
        Name (or requirement specifier) of the package to install.
    upgrade: bool, default False
        If ``True``, pass ``--upgrade`` to ``pip install``.

    Raises
    ------
    subprocess.CalledProcessError
        If the installation fails.
    """
    env_path = Path(env_path).expanduser().resolve()
    args = ["install"]
    if upgrade:
        args.append("--upgrade")
    args.append(package)
    result = _run_pip(env_path, args)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, result.args, output=result.stdout, stderr=result.stderr
        )


def list_installed(env_path: str | Path) -> List[str]:
    """
    Return a list of installed packages in the virtual environment.

    The list contains strings in the form ``package==version`` as produced by
    ``pip list --format=freeze``.

    Parameters
    ----------
    env_path: str | Path
        Path to the virtual environment.

    Returns
    -------
    list[str]
        Installed packages.

    Raises
    ------
    subprocess.CalledProcessError
        If the ``pip list`` command fails.
    """
    env_path = Path(env_path).expanduser().resolve()
    result = _run_pip(env_path, ["list", "--format=freeze"])
    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, result.args, output=result.stdout, stderr=result.stderr
        )
    packages = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return packages