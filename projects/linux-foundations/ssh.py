"""
SSH utilities for common tasks such as key generation, connectivity testing,
command execution and file transfer.

The functions are thin wrappers around the OpenSSH client utilities
(`ssh`, `ssh-keygen`, `scp`). They rely on the presence of these binaries in
the system's PATH and are intended for use in scripts or interactive
sessions where a lightweight, dependency‑free approach is preferred.

All functions raise :class:`RuntimeError` when the underlying command fails.
"""

from __future__ import annotations

import shlex
import subprocess
from pathlib import Path
from typing import Iterable, List, Optional


def _run_command(
    cmd: List[str],
    capture_output: bool = False,
    check: bool = True,
    timeout: Optional[int] = None,
) -> subprocess.CompletedProcess:
    """
    Execute a command via :func:`subprocess.run` with sensible defaults.

    Parameters
    ----------
    cmd : list[str]
        Command and arguments to execute.
    capture_output : bool, optional
        If ``True`` the standard output and error are captured and returned.
        Defaults to ``False``.
    check : bool, optional
        If ``True`` (default) a non‑zero exit status raises
        :class:`subprocess.CalledProcessError`.
    timeout : int, optional
        Number of seconds to wait for command completion.

    Returns
    -------
    subprocess.CompletedProcess
        The result object from :func:`subprocess.run`.
    """
    return subprocess.run(
        cmd,
        capture_output=capture_output,
        text=True,
        check=check,
        timeout=timeout,
    )


def generate_ssh_key(
    key_path: str | Path,
    comment: str = "",
    passphrase: str = "",
    key_type: str = "rsa",
    bits: int = 4096,
) -> Path:
    """
    Generate an SSH key pair using ``ssh-keygen``.

    Parameters
    ----------
    key_path : str or pathlib.Path
        Destination file for the private key. The public key will be created
        alongside it with a ``.pub`` suffix.
    comment : str, optional
        Comment to embed in the public key (default: empty).
    passphrase : str, optional
        Passphrase for the private key. Empty string creates an unencrypted key.
    key_type : str, optional
        Type of key to generate (e.g., ``rsa``, ``ed25519``). Default is ``rsa``.
    bits : int, optional
        Number of bits for RSA keys. Ignored for key types that do not use a
        bit size (default: 4096).

    Returns
    -------
    pathlib.Path
        Path to the generated private key.

    Raises
    ------
    RuntimeError
        If ``ssh-keygen`` exits with a non‑zero status.
    """
    key_path = Path(key_path).expanduser().resolve()
    cmd = [
        "ssh-keygen",
        "-t",
        key_type,
        "-f",
        str(key_path),
        "-N",
        passphrase,
    ]

    if comment:
        cmd.extend(["-C", comment])

    if key_type == "rsa":
        cmd.extend(["-b", str(bits)])

    try:
        _run_command(cmd)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Failed to generate SSH key: {exc}") from exc

    return key_path


def test_ssh_connection(
    host: str,
    user: str,
    port: int = 22,
    timeout: int = 5,
    strict_host_key_checking: bool = False,
) -> bool:
    """
    Test whether an SSH connection can be established to a remote host.

    The function attempts a non‑interactive connection using ``ssh`` with the
    ``-o BatchMode=yes`` option, which disables password prompts. It returns
    ``True`` if the connection succeeds (exit status 0) and ``False`` otherwise.

    Parameters
    ----------
    host : str
        Remote hostname or IP address.
    user : str
        Username for the SSH login.
    port : int, optional
        SSH port number (default: 22).
    timeout : int, optional
        Connection timeout in seconds (default: 5).
    strict_host_key_checking : bool, optional
        If ``False`` (default) the ``StrictHostKeyChecking`` option is set to
        ``no`` to avoid interactive prompts on first connection.

    Returns
    -------
    bool
        ``True`` if the SSH handshake succeeds, ``False`` otherwise.
    """
    options = [
        "BatchMode=yes",
        f"ConnectTimeout={timeout}",
    ]
    if not strict_host_key_checking:
        options.append("StrictHostKeyChecking=no")

    cmd = [
        "ssh",
        "-p",
        str(port),
        "-o",
        ",".join(options),
        f"{user}@{host}",
        "echo",
        "connected",
    ]

    try:
        _run_command(cmd, capture_output=True, check=False, timeout=timeout + 2)
        return True
    except Exception:
        return False


def run_ssh_command(
    host: str,
    user: str,
    command: str | Iterable[str],
    port: int = 22,
    timeout: int = 10,
    strict_host_key_checking: bool = False,
) -> str:
    """
    Execute a remote command over SSH and return its standard output.

    Parameters
    ----------
    host : str
        Remote hostname or IP address.
    user : str
        Username for the SSH login.
    command : str or iterable of str
        Command to run on the remote host. If an iterable is provided it will be
        joined using spaces after proper quoting.
    port : int, optional
        SSH port number (default: 22).
    timeout : int, optional
        Execution timeout in seconds (default: 10).
    strict_host_key_checking : bool, optional
        Whether to enforce strict host key checking. Defaults to ``False`` for
        convenience in learning environments.

    Returns
    -------
    str
        The captured standard output from the remote command.

    Raises
    ------
    RuntimeError
        If the SSH command exits with a non‑zero status.
    """
    if isinstance(command, (list, tuple)):
        # Properly escape each argument
        command = " ".join(shlex.quote(str(part)) for part in command)

    options = [
        "BatchMode=yes",
        f"ConnectTimeout={timeout}",
    ]
    if not strict_host_key_checking:
        options.append("StrictHostKeyChecking=no")

    cmd = [
        "ssh",
        "-p",
        str(port),
        "-o",
        ",".join(options),
        f"{user}@{host}",
        command,
    ]

    try:
        result = _run_command(cmd, capture_output=True, timeout=timeout + 5)
        return result.stdout.strip()
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"Remote command failed (exit {exc.returncode}): {exc.stderr}"
        ) from exc


def copy_file_to_remote(
    local_path: str | Path,
    remote_path: str,
    host: str,
    user: str,
    port: int = 22,
    timeout: int = 30,
    strict_host_key_checking: bool = False,
) -> None:
    """
    Transfer a local file to a remote host using ``scp``.

    Parameters
    ----------
    local_path : str or pathlib.Path
        Path to the source file on the local machine.
    remote_path : str
        Destination path on the remote host. Can be absolute or relative to the
        remote user's home directory.
    host : str
        Remote hostname or IP address.
    user : str
        Username for the SSH login.
    port : int, optional
        SSH port number (default: 22).
    timeout : int, optional
        Transfer timeout in seconds (default: 30).
    strict_host_key_checking : bool, optional
        Whether to enforce strict host key checking. Defaults to ``False``.

    Raises
    ------
    RuntimeError
        If the ``scp`` command fails.
    """
    local_path = Path(local_path).expanduser().resolve()
    if not local_path.is_file():
        raise RuntimeError(f"Local path does not exist or is not a file: {local_path}")

    options = [
        f"-P {port}",
        "-o BatchMode=yes",
        f"-o ConnectTimeout={timeout}",
    ]
    if not strict_host_key_checking:
        options.append("-o StrictHostKeyChecking=no")

    cmd = [
        "scp",
        *options,
        str(local_path),
        f"{user}@{host}:{remote_path}",
    ]

    try:
        _run_command(cmd, capture_output=True, timeout=timeout + 5)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"SCP failed (exit {exc.returncode}): {exc.stderr}"
        ) from exc