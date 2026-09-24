"""
Package Management Notes

This module provides a concise overview of Linux package management tools
and concepts. The content is intended for educational purposes and can be
imported by other parts of the project (e.g., the central ``notes`` module)
to display or process the notes programmatically.

The primary entry point is the :func:`get_notes` function, which returns the
entire notes text as a single string.
"""

__all__ = ["get_notes"]


def get_notes() -> str:
    """
    Return a formatted string containing notes on Linux package management.

    The notes cover:

    * **Package managers** – native system package managers (APT, YUM/DNF,
      Zypper, Pacman) and universal package formats (Snap, Flatpak, AppImage).
    * **Repositories** – how repositories are defined, enabled, and
      prioritized.
    * **Common commands** – installation, removal, upgrade, search, and
      query operations for each manager.
    * **Best practices** – keeping the system up‑to‑date, avoiding
      mixing incompatible sources, and verifying package authenticity.

    Returns
    -------
    str
        The complete notes text.
    """
    notes = """
# Linux Package Management

## Native Package Managers

| Distribution | Manager | Primary Commands |
|--------------|---------|------------------|
| Debian/Ubuntu | **APT** | `apt update`, `apt install <pkg>`, `apt remove <pkg>`, `apt upgrade` |
| RHEL/CentOS/Fedora | **YUM/DNF** | `yum check-update`, `yum install <pkg>`, `yum remove <pkg>`, `yum update`<br>`dnf check-update`, `dnf install <pkg>`, `dnf remove <pkg>`, `dnf upgrade` |
| openSUSE | **Zypper** | `zypper refresh`, `zypper install <pkg>`, `zypper remove <pkg>`, `zypper update` |
| Arch Linux | **Pacman** | `pacman -Sy`, `pacman -S <pkg>`, `pacman -R <pkg>`, `pacman -Syu` |

### APT Example Workflow
```bash
sudo apt update               # Refresh package index
sudo apt install vim         # Install a package
dpkg -L vim                   # List files installed by the package
apt list --installed | grep vim   # Verify installation
sudo apt remove vim          # Remove the package
sudo apt autoremove           # Clean up unused dependencies
```

### DNF Example Workflow
```bash
sudo dnf check-update
sudo dnf install git
rpm -ql git                  # List files from the RPM package
sudo dnf remove git
sudo dnf autoremove
```

## Universal Package Formats

| Format   | Tool      | Key Characteristics |
|----------|-----------|----------------------|
| **Snap** | `snap`    | Containerized, auto‑updates, works across many distros |
| **Flatpak** | `flatpak` | Sandbox isolation, runtime dependencies separate |
| **AppImage** | (no tool) | Single executable file, no installation required |

### Snap Commands
```bash
sudo snap install vlc          # Install from Snap Store
snap list                      # List installed snaps
sudo snap remove vlc           # Remove snap
snap refresh                   # Update all snaps
```

### Flatpak Commands
```bash
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub org.gimp.GIMP
flatpak list
flatpak uninstall org.gimp.GIMP
flatpak update
```

## Repositories

* **Sources list** – For APT, `/etc/apt/sources.list` and files under
  `/etc/apt/sources.list.d/`.
* **Repo files** – For YUM/DNF, files under `/etc/yum.repos.d/`.
* **Enabling/Disabling** – Comment out lines or set `enabled=0` in repo files.
* **Priorities** – Use `apt-pinning` or `yum-plugin-priorities` to control
  which repository provides a package when multiple sources contain it.

## Best Practices

1. **Keep the system updated** – Regularly run the upgrade command for the
   native manager (`apt upgrade`, `dnf upgrade`, etc.).
2. **Avoid mixing package sources** – Do not install the same software from
   both the native manager and a universal format unless you understand the
   implications.
3. **Verify signatures** – Ensure repository GPG keys are trusted; avoid
   disabling signature verification.
4. **Clean up** – Use `autoremove` (APT) or `dnf autoremove` to purge orphaned
   dependencies.
5. **Read documentation** – Each manager provides a man page (`man apt`,
   `man dnf`, `man snap`, etc.) with detailed options.

--- 

These notes serve as a quick reference for common package management tasks
across major Linux distributions.
"""
    return notes.strip()