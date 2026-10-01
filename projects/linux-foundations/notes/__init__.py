"""
Linux Foundations – Notes Package

This package aggregates various note modules for quick reference.
"""

# Export note functions for convenient import
from .archives import archives_notes  # noqa: F401
from .bash_scripting import bash_scripting_notes  # noqa: F401
from .command_resolution import command_resolution_notes  # noqa: F401
from .cron import cron_notes  # noqa: F401
from .curl_wget_ports_dns import curl_wget_ports_dns_notes  # noqa: F401
from .env_vars import env_vars_notes  # noqa: F401
from .file_descriptors import file_descriptors_notes  # noqa: F401
from .git import git_notes  # noqa: F401
from .links import links_notes  # noqa: F401
from .logs import logs_notes  # noqa: F401
from .monitoring import monitoring_notes  # noqa: F401
from .networking import networking_notes  # noqa: F401
from .networking_tools import networking_tools_notes  # noqa: F401
from .package_management import package_management_notes  # noqa: F401
from .path import path_notes  # noqa: F401
from .pipes import pipes_notes  # noqa: F401
from .processes import processes_notes  # noqa: F401
from .quoting import quoting_notes  # noqa: F401
from .scheduled_jobs import scheduled_jobs_notes  # noqa: F401
from .services import services_notes  # noqa: F401
from .shell_control import shell_control_notes  # noqa: F401
from .special_permissions import special_permissions_notes  # noqa: F401
from .ssh import ssh_notes  # noqa: F401
from .std_io import std_io_notes  # noqa: F401
from .storage import storage_notes  # noqa: F401
from .system_info import system_info_notes  # noqa: F401
from .text_processing import text_processing_notes  # noqa: F401
from .users_groups_sudo import users_groups_sudo_notes  # noqa: F401
from .virtual_env import virtual_env_notes  # noqa: F401
from .security import security_notes  # noqa: F401

__all__ = [
    "archives_notes",
    "bash_scripting_notes",
    "command_resolution_notes",
    "cron_notes",
    "curl_wget_ports_dns_notes",
    "env_vars_notes",
    "file_descriptors_notes",
    "git_notes",
    "links_notes",
    "logs_notes",
    "monitoring_notes",
    "networking_notes",
    "networking_tools_notes",
    "package_management_notes",
    "path_notes",
    "pipes_notes",
    "processes_notes",
    "quoting_notes",
    "scheduled_jobs_notes",
    "services_notes",
    "shell_control_notes",
    "special_permissions_notes",
    "ssh_notes",
    "std_io_notes",
    "storage_notes",
    "system_info_notes",
    "text_processing_notes",
    "users_groups_sudo_notes",
    "virtual_env_notes",
    "security_notes",
]