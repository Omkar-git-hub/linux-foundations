"""
Disk and Storage Notes

This module provides a concise reference for common disk‑related commands,
concepts, and best practices on Linux systems. The content is intended to be
used as quick documentation or as part of the larger notes collection in the
project.

Typical usage:

    from projects.linux_foundations.notes.storage import NOTES
    print(NOTES)
"""

# A multiline string containing the actual notes.
NOTES = """
=== Disk and Storage Overview ===

Linux treats storage devices as block devices. Each block device appears under
`/dev` (e.g., `/dev/sda`, `/dev/nvme0n1`). Partitions are represented as
suffixes (`/dev/sda1`, `/dev/sda2`, …). Modern systems also expose virtual
block devices such as loop devices (`/dev/loop0`) and RAM disks.

Key concepts:
- **Filesystem** – a data structure that organizes how files are stored on a
  block device (e.g., ext4, xfs, btrfs, vfat).
- **Mount point** – a directory where a filesystem is attached to the global
  namespace.
- **Swap** – a special partition or file used as virtual memory.

=== Common Commands ===

1. **df** – Report file system disk space usage.
   ```bash
   df -h               # Human‑readable output
   df -Th              # Show filesystem type
   df -i               # Show inode usage
   ```

2. **du** – Estimate file and directory space usage.
   ```bash
   du -sh /path        # Summary for a single path
   du -h --max-depth=1 /path   # One‑level summary
   ```

3. **lsblk** – List block devices.
   ```bash
   lsblk               # Tree view of devices and partitions
   lsblk -f            # Show filesystem type and UUID
   lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINT
   ```

4. **blkid** – Print block device attributes (UUID, TYPE, LABEL).
   ```bash
   blkid               # All detected devices
   blkid /dev/sda1     # Specific device
   ```

5. **fdisk / gdisk / cfdisk** – Partition table manipulation.
   ```bash
   sudo fdisk /dev/sda          # MBR partitioning
   sudo gdisk /dev/nvme0n1      # GPT partitioning
   ```

6. **parted** – Advanced partitioning (supports scripting).
   ```bash
   sudo parted /dev/sda mklabel gpt
   sudo parted -a optimal /dev/sda mkpart primary ext4 1MiB 100%
   ```

7. **mkfs** – Create a filesystem on a block device or partition.
   ```bash
   sudo mkfs.ext4 /dev/sda1
   sudo mkfs.xfs /dev/sdb1
   ```

8. **mount / umount** – Attach/detach filesystems.
   ```bash
   sudo mount /dev/sda1 /mnt/data
   sudo umount /mnt/data
   ```

9. **swapon / swapoff** – Enable/disable swap devices or files.
   ```bash
   sudo swapon /dev/sda2
   sudo swapoff /dev/sda2
   ```

10. **dd** – Low‑level copying and imaging.
    ```bash
    sudo dd if=/dev/zero of=/dev/sda bs=1M count=1024   # Zero first 1 GiB
    sudo dd if=image.img of=/dev/sdb bs=4M status=progress
    ```

11. **btrfs** and **zfs** – Advanced filesystems with snapshots, subvolumes,
    and built‑in RAID. Usage varies; consult their man pages.

=== Managing Disk Space ===

- **Identify large directories**:
  ```bash
  du -ahx / | sort -rh | head -20
  ```

- **Find the biggest files**:
  ```bash
  find / -type f -exec du -h {} + | sort -rh | head -n 10
  ```

- **Clean package caches** (example for apt):
  ```bash
  sudo apt-get clean
  ```

- **Log rotation** – Ensure `/etc/logrotate.d/` is configured to prevent logs
  from filling the root filesystem.

=== Best Practices ===

- Use **UUIDs** or **labels** in `/etc/fstab` to avoid issues when device names
  change.
- Keep a **separate /boot** partition on BIOS systems using a stable device name.
- Regularly **snapshot** critical data (e.g., with `btrfs subvolume snapshot`
  or LVM snapshots) before performing destructive operations.
- Monitor disk health with **smartctl** (from `smartmontools`):
  ```bash
  sudo smartctl -a /dev/sda
  ```

=== References ===

- `man df`, `man du`, `man lsblk`, `man blkid`
- The Linux Documentation Project: https://tldp.org/LDP/
- Filesystem specific docs: ext4, xfs, btrfs, zfs
"""

__all__ = ["NOTES"]