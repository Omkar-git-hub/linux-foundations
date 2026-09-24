"""
Notes on Linux package management.

This file contains plain‑text style notes that complement the
programmatic helpers in ``package_management.py``.  The content is
intended for human readers and can be imported for quick reference
or displayed via a CLI if desired.
"""

PACKAGE_MANAGERS = {
    "apt": {
        "description": "Debian/Ubuntu based systems",
        "install": "sudo apt-get install <package>",
        "remove": "sudo apt-get remove <package>",
        "list": "dpkg-query -W -f='${Package}\\n'",
        "search": "apt-cache search <term>",
    },
    "dnf": {
        "description": "Fedora, RHEL 8+",
        "install": "sudo dnf install <package>",
        "remove": "sudo dnf remove <package>",
        "list": "dnf list installed",
        "search": "dnf search <term>",
    },
    "yum": {
        "description": "RHEL/CentOS 7 and older",
        "install": "sudo yum install <package>",
        "remove": "sudo yum remove <package>",
        "list": "yum list installed",
        "search": "yum search <term>",
    },
    "pacman": {
        "description": "Arch Linux and derivatives",
        "install": "sudo pacman -S <package>",
        "remove": "sudo pacman -R <package>",
        "list": "pacman -Q",
        "search": "pacman -Ss <term>",
    },
    "zypper": {
        "description": "openSUSE and SUSE Linux Enterprise",
        "install": "sudo zypper install <package>",
        "remove": "sudo zypper remove <package>",
        "list": "zypper search --installed-only",
        "search": "zypper search <term>",
    },
}

def get_notes(manager: str) -> str:
    """
    Return a formatted string with the most common commands for the
    given package manager.  If the manager is unknown, an empty string
    is returned.
    """
    info = PACKAGE_MANAGERS.get(manager)
    if not info:
        return ""
    lines = [
        f"Package manager: {manager} ({info['description']})",
        f"Install:   {info['install']}",
        f"Remove:    {info['remove']}",
        f"List:      {info['list']}",
        f"Search:    {info['search']}",
    ]
    return "\n".join(lines)