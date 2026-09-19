"""
Notes about Linux Users, Groups, and sudo.

This module provides ready‑to‑use textual notes that can be displayed,
written to files, or used in documentation generators. The notes cover
the basics of user management, group management, and sudo configuration
on a typical Linux system.
"""

# User management notes
USERS_NOTE = """\
## Linux Users

- **User ID (UID)**: A numeric identifier for each user. UID 0 is the
  superuser (root). Regular users typically have UID ≥ 1000.
- **Home directory**: Usually `/home/<username>`. Stores user‑specific
  configuration and files.
- **Shell**: The command interpreter started after login, e.g. `/bin/bash`.

### Common commands
- `id <user>` – Show UID, GID and group memberships.
- `useradd -m <user>` – Create a new user with a home directory.
- `passwd <user>` – Set or change the user’s password.
- `usermod -aG <group> <user>` – Add an existing user to an additional group.
- `deluser <user>` – Remove a user (Debian/Ubuntu) or `userdel` on other distros.
"""

# Group management notes
GROUPS_NOTE = """\
## Linux Groups

- **Group ID (GID)**: Numeric identifier for a group. GID 0 is the root group.
- **Primary group**: Assigned to a user at login; stored in `/etc/passwd`.
- **Supplementary groups**: Additional groups a user belongs to; listed in `/etc/group`.

### Common commands
- `groupadd <group>` – Create a new group.
- `groupdel <group>` – Delete a group.
- `gpasswd -a <user> <group>` – Add a user to a group (alternative to `usermod -aG`).
- `gpasswd -d <user> <group>` – Remove a user from a group.
- `getent group <group>` – Display group information.
"""

# sudo configuration notes
SUDO_NOTE = """\
## sudo – Execute commands as another user (usually root)

- **sudoers file**: Located at `/etc/sudoers`. Should be edited with `visudo`
  to prevent syntax errors.
- **User specification**: Defines which users can run which commands.

### Typical sudoers entries
```
# Allow members of the “wheel” group to run any command
%wheel ALL=(ALL:ALL) ALL

# Allow a specific user to run all commands without a password
alice ALL=(ALL) NOPASSWD: ALL

# Allow a user to run only specific commands
bob ALL=(root) /usr/bin/systemctl restart httpd, /usr/bin/journalctl -u httpd
```

### Common commands
- `sudo <command>` – Run a single command as root (or another user).
- `sudo -i` – Open an interactive root shell.
- `sudo -u <user> <command>` – Run a command as a specified user.
- `visudo` – Safely edit the sudoers file.
"""

def get_all_notes():
    """
    Return a dictionary containing all notes defined in this module.

    Returns
    -------
    dict
        Mapping keys ``'users'``, ``'groups'`` and ``'sudo'`` to their
        respective note strings.
    """
    return {
        "users": USERS_NOTE,
        "groups": GROUPS_NOTE,
        "sudo": SUDO_NOTE,
    }

__all__ = [
    "USERS_NOTE",
    "GROUPS_NOTE",
    "SUDO_NOTE",
    "get_all_notes",
]