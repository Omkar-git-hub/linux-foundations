"""
Linux Foundations Notes package.

This package aggregates various note modules that provide concise
explanations and helper utilities for Linux concepts.
"""

# Re-export note modules for convenient import.
from .archives import *
from .bash_scripting import *
from .command_resolution import *
from .cron import *
from .curl_wget_ports_dns import *
from .env_vars import *
from .file_descriptors import *
from .git import *
from .links import *
from .logs import *
from .monitoring import *
from .networking import *
from .networking_tools import *
from .package_management import *
from .path import *
from .pipes import *
from .processes import *
from .quoting import *
from .scheduled_jobs import *
from .services import *
from .shell_control import *
from .ssh import *
from .std_io import *
from .storage import *
from .system_info import *
from .text_processing import *
from .users_groups_sudo import *
from .virtual_env import *
from .special_permissions import *

# Define the public API of the notes package.
__all__ = [
    # archives
    "ARCHIVES",
    # bash_scripting
    "BASH_SCRIPTING",
    # command_resolution
    "COMMAND_RESOLUTION",
    # cron
    "CRON",
    # curl_wget_ports_dns
    "CURL_WGET_PORTS_DNS",
    # env_vars
    "ENV_VARS",
    # file_descriptors
    "FILE_DESCRIPTORS",
    # git
    "GIT",
    # links
    "LINKS",
    # logs
    "LOGS",
    # monitoring
    "MONITORING",
    # networking
    "NETWORKING",
    # networking_tools
    "NETWORKING_TOOLS",
    # package_management
    "PACKAGE_MANAGEMENT",
    # path
    "PATH",
    # pipes
    "PIPES",
    # processes
    "PROCESSES",
    # quoting
    "QUOTING",
    # scheduled_jobs
    "SCHEDULED_JOBS",
    # services
    "SERVICES",
    # shell_control
    "SHELL_CONTROL",
    # ssh
    "SSH",
    # std_io
    "STD_IO",
    # storage
    "STORAGE",
    # system_info
    "SYSTEM_INFO",
    # text_processing
    "TEXT_PROCESSING",
    # users_groups_sudo
    "USERS_GROUPS_SUDO",
    # virtual_env
    "VIRTUAL_ENV",
    # special permissions
    "SpecialPermission",
    "SETUID",
    "SETGID",
    "STICKY",
    "SPECIAL_PERMISSIONS",
    "list_special_permissions",
]