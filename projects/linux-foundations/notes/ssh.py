"""
SSH Notes Module
================

This module provides helpful documentation and utility functions related to
using the OpenSSH client (`ssh`).  The notes are written as a plain‑text
string that can be displayed in a terminal or used by other parts of the
project (for example, in CLI help output).

Utility Functions
-----------------

* :func:`generate_ssh_command` – Build an ``ssh`` command line from
  parameters such as host, user, port, identity file and additional options.

* :func:`get_ssh_notes` – Return the multi‑line notes string.

The implementation purposefully avoids any external dependencies and relies
solely on the Python standard library.
"""

from __future__ import annotations

from shlex import quote
from typing import Mapping, Sequence

__all__: Sequence[str] = ("SSH_NOTES", "generate_ssh_command", "get_ssh_notes")


SSH_NOTES: str = """\
SSH (Secure Shell) is a protocol for securely accessing remote systems.
Below are common usage patterns and tips.

1. Basic connection
   $ ssh user@host

2. Specify a non‑default port
   $ ssh -p 2222 user@host

3. Use a specific private key
   $ ssh -i /path/to/key.pem user@host

4. Disable strict host key checking (useful for scripts)
   $ ssh -o StrictHostKeyChecking=no user@host

5. Forward a local port to the remote host
   $ ssh -L 8080:localhost:80 user@host

6. Remote command execution
   $ ssh user@host 'ls -l /var/www'

7. SSH config file (~/.ssh/config) can store host aliases:
   Host myserver
       HostName example.com
       User alice
       Port 2222
       IdentityFile ~/.ssh/id_rsa_myserver

Tips
----
* Keep your private keys protected (chmod 600).
* Use ssh-agent to cache passphrases.
* For automation, consider using key‑based auth and disabling
  ``StrictHostKeyChecking`` only when you trust the target host.
"""


def generate_ssh_command(
    host: str,
    *,
    user: str | None = None,
    port: int | None = None,
    identity_file: str | None = None,
    options: Mapping[str, str] | None = None,
) -> str:
    """
    Build an ``ssh`` command line string from the supplied arguments.

    Parameters
    ----------
    host: str
        The remote hostname or IP address.
    user: str, optional
        Username for the remote login. If omitted, the current system user
        is used by the ``ssh`` client.
    port: int, optional
        Remote SSH port. If omitted, the default port 22 is used.
    identity_file: str, optional
        Path to a private key file (passed to ``-i``).
    options: Mapping[str, str], optional
        Additional ``-o`` options. Keys are option names, values are the
        corresponding values (both will be quoted as needed).

    Returns
    -------
    str
        A ready‑to‑execute command line that can be passed to ``subprocess``
        or printed to the console.

    Examples
    --------
    >>> generate_ssh_command('example.com', user='bob')
    "ssh bob@example.com"
    >>> generate_ssh_command('example.com', port=2222, identity_file='~/.ssh/key')
    "ssh -p 2222 -i ~/.ssh/key example.com"
    """
    parts: list[str] = ["ssh"]

    if port is not None:
        parts.extend(["-p", str(port)])

    if identity_file is not None:
        parts.extend(["-i", quote(identity_file)])

    if options:
        for opt_name, opt_value in options.items():
            # Quote the whole option string to protect spaces or special chars
            opt_str = f"{opt_name}={opt_value}"
            parts.extend(["-o", quote(opt_str)])

    # Build the user@host part
    destination = f"{user}@{host}" if user else host
    parts.append(destination)

    return " ".join(parts)


def get_ssh_notes() -> str:
    """
    Return the SSH notes documentation.

    Returns
    -------
    str
        The multi‑line string stored in :data:`SSH_NOTES`.
    """
    return SSH_NOTES