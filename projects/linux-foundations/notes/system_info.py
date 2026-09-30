"""
System Information Notes
========================

This module provides a quick reference for gathering system information on
Linux/Unix platforms. The notes are intended for human readers and can be
imported to keep the documentation close to the code base.

Common commands
---------------

* ``uname -a`` – Print all system information (kernel name, version, hostname,
  hardware platform, etc.).
* ``cat /proc/cpuinfo`` – Detailed CPU information.
* ``lscpu`` – Summarized CPU architecture information.
* ``cat /proc/meminfo`` – Detailed memory information.
* ``free -h`` – Human‑readable memory usage summary.
* ``df -h`` – Disk space usage for all mounted filesystems.
* ``lsblk`` – List block devices (disks, partitions) and their mount points.
* ``ip a`` or ``ifconfig`` – Network interface configuration.
* ``lsusb`` – List USB devices.
* ``lspci`` – List PCI devices.
* ``dmidecode`` – DMI/SMBIOS table contents (requires root).

Python helpers
--------------

The :pymod:`projects.linux_foundations.system_info` module contains utility
functions that wrap many of the above commands and expose the information as
Python data structures.  Typical usage::

    from projects.linux_foundations.system_info import (
        get_kernel_info,
        get_cpu_info,
        get_memory_info,
        get_disk_info,
        get_network_info,
    )

    print(get_kernel_info())
    print(get_cpu_info())
    print(get_memory_info())
    print(get_disk_info())
    print(get_network_info())

These helpers use the standard library (``subprocess``, ``json``, ``pathlib``)
and avoid external dependencies.

Reference
---------

* ``man uname``
* ``man proc``
* ``man lscpu``
* ``man free``
* ``man df``
* ``man lsblk``
* ``man ip``
* ``man ifconfig``
* ``man lsusb``
* ``man lspci``
* ``man dmidecode``
"""

# The module is intentionally lightweight; it only provides documentation.
# Importing the actual implementation from the sibling ``system_info`` module
# is optional and left to the consumer.

pass