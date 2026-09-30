"""
Services and ``systemctl`` Notes
================================

Systemd is the init system used by most modern Linux distributions.
It provides the ``systemctl`` command‑line tool for managing *units*,
which include services, sockets, timers, mounts, and more.

Key Concepts
------------

* **Unit** – A resource that systemd knows how to manage.  The most common
  type is a *service* (``*.service`` files located in ``/etc/systemd/system``
  or ``/usr/lib/systemd/system``).

* **systemctl** – The primary interface for interacting with systemd.
  It can start, stop, enable, disable, reload, and query units.

Common ``systemctl`` Commands
-----------------------------

``systemctl list-units --type=service``
    List all loaded service units, regardless of their state.

``systemctl status <unit>``
    Show detailed status information for a specific unit.

``systemctl is-active <unit>``
    Return ``active`` if the unit is running; otherwise returns a non‑zero
    exit status.

``systemctl start|stop|restart <unit>``
    Control the runtime state of a unit.

``systemctl enable|disable <unit>``
    Configure whether the unit should be started automatically at boot.

``systemctl daemon-reload``
    Reload systemd manager configuration after unit files have changed.

Programmatic Access
-------------------

The :pymod:`projects.linux_foundations.services` module wraps the most
frequently used ``systemctl`` operations in Python functions.  Example::

    from projects.linux_foundations.services import list_units, is_active, start

    # List all services
    services = list_units()

    # Ensure the SSH service is running
    if not is_active('ssh.service'):
        start('ssh.service')

These helpers raise :class:`subprocess.CalledProcessError` on failure,
allowing callers to handle errors explicitly.

Best Practices
--------------

* Prefer ``systemctl is-active`` over parsing ``systemctl status`` output.
* Use ``--no-pager`` and ``--no-legend`` when scripting to obtain clean,
  machine‑readable output.
* After installing or modifying unit files, always run
  ``systemctl daemon-reload`` before attempting to start the unit.

Further Reading
---------------

* ``man systemctl``
* ``man systemd.unit``
* The official systemd documentation: https://www.freedesktop.org/wiki/Software/systemd/
"""