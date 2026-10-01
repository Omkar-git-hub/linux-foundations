"""
Linux Security Notes

This module provides a concise collection of notes covering essential
Linux security concepts, best practices, and common tools. The notes are
intended for quick reference and educational purposes.
"""

def security_notes() -> str:
    """
    Return a formatted string containing Linux security notes.

    The notes cover:

    * User and group management
    * File permissions and ACLs
    * sudo configuration
    * Security‑enhanced Linux (SELinux) basics
    * AppArmor basics
    * Firewall configuration with nftables/iptables
    * Auditing with auditd
    * Common hardening tools (fail2ban, lynis, etc.)
    * Kernel hardening parameters
    * System updates and vulnerability management

    Returns
    -------
    str
        Multiline string with the security notes.
    """
    return """\
# Linux Security Notes

## 1. User & Group Management
- Use least‑privilege principle: create dedicated users for services.
- Disable/lock the root account for remote logins (`passwd -l root`).
- Enforce strong password policies via `/etc/login.defs` and PAM
  (`pam_pwquality.so`).

## 2. File Permissions & ACLs
- Default permissions: `umask 027` for restrictive defaults.
- Use POSIX permissions (`chmod`, `chown`) and, when needed,
  POSIX ACLs (`setfacl`, `getfacl`) for fine‑grained control.
- Avoid world‑writable directories (`/tmp`, `/var/tmp`) unless required.

## 3. sudo Configuration
- Keep `/etc/sudoers` minimal; use `visudo` for syntax checking.
- Prefer `%admin ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart *`
  over blanket `NOPASSWD: ALL`.
- Log sudo usage (`Defaults logfile="/var/log/sudo.log"`).

## 4. SELinux (Security‑Enhanced Linux)
- Modes: `enforcing`, `permissive`, `disabled`.
- Check status: `sestatus`.
- Manage policies with `semanage`, `setsebool`, and `audit2allow`.
- Use targeted policy for most servers; consider MLS for high‑security
  environments.

## 5. AppArmor
- Profiles located in `/etc/apparmor.d/`.
- Load/disable profiles: `apparmor_parser -r /path/to/profile`.
- Use `aa-status` to view active profiles and `aa-complain`/`aa-enforce`
  to adjust enforcement.

## 6. Firewall (nftables / iptables)
- Prefer `nftables` (`nft`) on modern distributions.
- Example minimal nftables config:
    ```
    table inet filter {
        chain input {
            type filter hook input priority 0; policy drop;
            ct state established,related accept
            iif "lo" accept
            tcp dport { 22, 80, 443 } ct state new accept
        }
    }
    ```
- For legacy iptables, keep a default DROP policy and allow only needed
  ports.

## 7. Auditing (auditd)
- Install `auditd`; ensure service is enabled.
- Add rules via `/etc/audit/rules.d/` (e.g., watch `/etc/passwd`).
- Use `ausearch` and `aureport` to query logs.

## 8. Common Hardening Tools
- **fail2ban** – bans IPs after repeated failed login attempts.
- **lynis** – security audit tool (`lynis audit system`).
- **rkhunter**, **chkrootkit** – rootkit detection.
- **clamav** – antivirus for scanning files.

## 9. Kernel Hardening
- Enable sysctl hardening parameters, e.g.:
    ```
    net.ipv4.ip_forward = 0
    net.ipv4.conf.all.accept_source_route = 0
    kernel.randomize_va_space = 2
    fs.suid_dumpable = 0
    ```
- Apply via `/etc/sysctl.d/99-hardening.conf` and run `sysctl --system`.

## 10. System Updates & Vulnerability Management
- Enable automatic security updates (`unattended-upgrades` on Debian/Ubuntu,
  `dnf-automatic` on Fedora).
- Regularly run vulnerability scanners (e.g., `openscap`, `trivy`).
- Subscribe to distro security mailing lists or RSS feeds.

--- 

Keep these notes as a quick checklist when provisioning or auditing a Linux
system. Regularly review and adapt them to the specific security policies
of your organization.
"""