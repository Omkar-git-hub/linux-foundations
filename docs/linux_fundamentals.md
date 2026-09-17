# Linux Fundamentals

## 1. Introduction
Linux is a family of open‑source Unix‑like operating systems based on the Linux kernel. It is widely used for servers, desktops, embedded systems, and more.

## 2. Core Concepts

| Concept | Description |
|---------|-------------|
| **Kernel** | The core of the OS that manages hardware, memory, processes, and system calls. |
| **Shell** | Command‑line interpreter (e.g., `bash`, `zsh`) that lets users interact with the system. |
| **Filesystem Hierarchy** | Standard directory layout (`/`, `/bin`, `/etc`, `/home`, `/var`, `/tmp`, etc.). |
| **Processes** | Running instances of programs, each with a unique PID. |
| **Permissions** | Access control using read (`r`), write (`w`), execute (`x`) bits for user, group, others. |
| **Package Management** | Tools (`apt`, `yum`, `dnf`, `pacman`) to install, update, and remove software. |

## 3. Basic Commands

| Command | Purpose |
|---------|---------|
| `pwd` | Print current working directory. |
| `ls` | List directory contents. |
| `cd` | Change directory. |
| `mkdir` | Create a new directory. |
| `rm` | Remove files or directories (`-r` for recursive). |
| `cp` | Copy files or directories (`-r` for recursive). |
| `mv` | Move/rename files or directories. |
| `cat` | Concatenate and display file contents. |
| `grep` | Search text using patterns. |
| `chmod` | Change file permissions. |
| `chown` | Change file owner/group. |
| `ps` | Show running processes. |
| `top` / `htop` | Interactive process viewer. |
| `kill` | Send signals to processes (e.g., terminate). |
| `sudo` | Execute a command with superuser privileges. |
| `apt update && apt upgrade` | Update package lists and upgrade installed packages (Debian/Ubuntu). |

## 4. Filesystem Navigation

```bash
# Show absolute path
pwd

# List all files, including hidden ones, with details
ls -la

# Change to home directory
cd ~

# Go up one level
cd ..

# Create nested directories
mkdir -p projects/python/scripts
```

## 5. Text Editing

- **nano** – Simple terminal editor.
- **vim** – Powerful modal editor.
- **gedit**, **code**, **sublime** – GUI editors.

## 6. Process Management

```bash
# List processes owned by current user
ps -u $USER

# Find process ID by name
pgrep python

# Terminate a process gracefully
kill <PID>

# Force kill
kill -9 <PID>
```

## 7. Permissions & Ownership

```bash
# Change mode to rwxr-xr--
chmod 754 script.sh

# Change owner to user 'alice' and group 'developers'
chown alice:developers file.txt
```

## 8. Package Management (Debian/Ubuntu)

```bash
# Update package index
sudo apt update

# Install a package
sudo apt install git

# Remove a package
sudo apt remove git

# Search for a package
apt search nginx
```

## 9. System Monitoring

- `df -h` – Disk space usage.
- `du -sh *` – Directory size summary.
- `free -h` – Memory usage.
- `uptime` – System load and uptime.

## 10. Networking Basics

| Command | Description |
|---------|-------------|
| `ifconfig` / `ip addr` | Show network interfaces and IP addresses. |
| `ping <host>` | Test connectivity to a host. |
| `netstat -tulnp` | List listening ports and associated programs. |
| `ssh user@host` | Secure remote login. |
| `scp file user@host:/path` | Secure copy files over SSH. |
| `curl` / `wget` | Retrieve content from URLs. |

## 11. Shell Scripting Essentials

```bash
#!/usr/bin/env bash
# Simple backup script

SOURCE="/home/$USER/Documents"
DEST="/backup/$USER/documents_$(date +%F).tar.gz"

tar -czf "$DEST" "$SOURCE"
echo "Backup saved to $DEST"
```

- Make script executable: `chmod +x backup.sh`
- Run: `./backup.sh`

## 12. Useful Tips

- Use **tab completion** to speed up typing.
- Press **Ctrl+R** for reverse search in command history.
- Combine commands with `&&` (run next only if previous succeeds) or `;` (run sequentially).
- Redirect output: `command > file.txt` (overwrite) or `command >> file.txt` (append).
- Pipe output: `ls -l | grep "^d"` (list only directories).

## 13. Further Learning Resources

- **The Linux Command Line** by William Shotts (free PDF).
- **Linux Documentation Project** – https://tldp.org/
- **man pages** – `man <command>` for detailed command reference.
- Online tutorials: Linux Journey, Codecademy, freeCodeCamp.

--- 

*This document provides a concise overview of essential Linux concepts and commands for beginners.*