"""
Tests for the ``linux_foundations.links`` module.

The tests create temporary files and verify that the helper functions correctly
identify symbolic and hard links and that link creation works as expected.
"""

import os
import sys
import tempfile
from pathlib import Path

import pytest

# Import the module under test
from linux_foundations import (
    create_symlink,
    create_hardlink,
    is_symlink,
    is_hardlink,
    get_link_target,
    get_hardlink_count,
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for each test."""
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)


def test_symlink_creation_and_detection(temp_dir: Path):
    target = temp_dir / "original.txt"
    target.write_text("hello")

    link = temp_dir / "symlink.txt"
    created = create_symlink(target, link)
    assert created == link
    assert link.exists()
    assert is_symlink(link) is True
    assert get_link_target(link) == target
    # A symlink is not considered a hard link
    assert is_hardlink(link) is False
    # The original file's link count should be unchanged (1)
    assert get_hardlink_count(target) == 1


def test_hardlink_creation_and_detection(temp_dir: Path):
    source = temp_dir / "source.bin"
    source.write_bytes(b"data")
    hard = temp_dir / "hardlink.bin"

    created = create_hardlink(source, hard)
    assert created == hard
    assert hard.exists()
    # Hard link is not a symlink
    assert is_symlink(hard) is False
    # Both files share the same inode (link count == 2)
    assert is_hardlink(hard) is True
    assert get_hardlink_count(source) == 2
    assert get_hardlink_count(hard) == 2

    # Modifying one should affect the other
    hard.write_text("changed")
    assert source.read_text() == "changed"


@pytest.mark.skipif(
    sys.platform.startswith("win") and not os.getenv("CI"),
    reason="Creating symlinks on Windows without admin rights may fail",
)
def test_symlink_target_is_directory(temp_dir: Path):
    # Directory symlink test (requires target_is_directory=True on Windows)
    target_dir = temp_dir / "dir"
    target_dir.mkdir()
    link_dir = temp_dir / "link_dir"
    created = create_symlink(target_dir, link_dir, target_is_directory=True)
    assert created == link_dir
    assert link_dir.is_dir()
    assert is_symlink(link_dir) is True
    assert get_link_target(link_dir) == target_dir