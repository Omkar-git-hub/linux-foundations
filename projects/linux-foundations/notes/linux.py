"""
Linux Notes

This module provides a collection of notes and best practices related to Linux
systems. The content is intended for reference and educational purposes.
"""

def get_notes() -> str:
    """
    Return a string containing Linux notes.

    Returns
    -------
    str
        Multiline string with Linux related notes.
    """
    notes = """
Linux Fundamentals
------------------
- The Linux kernel is the core component that manages hardware, processes,
  memory, and system resources.
- Filesystem hierarchy follows the Filesystem Hierarchy Standard (FHS):
  /, /bin, /sbin, /usr, /var, /etc, /home, /tmp, /opt, /dev, /proc, /sys.

Shell Basics
------------
- Bash is the most common shell; other shells include zsh, fish, and dash.
- Use `man <command>` to view manual pages.
- Command chaining: `&&` (run next if previous succeeds), `||` (run next if previous fails),
  `;` (run sequentially regardless of exit status).

Permissions
-----------
- Permissions are expressed as rwx for user, group, others.
- `chmod`, `chown`, and `chgrp` modify permissions and ownership.
- Setuid, setgid, and sticky bits provide special permission behavior.

Process Management
------------------
- `ps`, `top`, `htop` display running processes.
- `kill`, `pkill`, `killall` send signals to processes.
- `nice` and `renice` adjust scheduling priority.

Networking
----------
- `ifconfig` (deprecated) and `ip` manage network interfaces.
- `ss`, `netstat`, `lsof` inspect sockets and connections.
- `iptables`/`nftables` configure firewall rules.

Package Management
------------------
- Debian/Ubuntu: `apt`, `dpkg`.
- Red Hat/Fedora: `yum`, `dnf`, `rpm`.
- Arch: `pacman`.

System Monitoring
-----------------
- `journalctl` reads systemd journal logs.
- `systemctl` controls services and units.
- `dmesg` displays kernel ring buffer messages.

These notes are a concise reference; consult the official documentation
for detailed information.
"""
    return notes.strip()