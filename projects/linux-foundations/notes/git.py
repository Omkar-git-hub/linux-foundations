"""
Git on Linux Notes

This module contains a collection of useful Git commands and best‑practice
tips for working with Git on Linux systems. The notes are provided as a
single multi‑line string (`GIT_NOTES`) and can be accessed via the
`get_git_notes` helper function.

The content is deliberately kept as plain text so it can be displayed
directly in a terminal, written to a file, or used in documentation
generation pipelines.
"""

GIT_NOTES = """\
# Git on Linux – Quick Reference

## Configuration
# Set your name and email (global)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Core editor (e.g., vim, nano, code)
git config --global core.editor "vim"

# Enable colored output
git config --global color.ui auto

# Show line endings handling (useful on Linux)
git config --global core.autocrlf input

## Repository Setup
# Initialize a new repository
git init

# Clone an existing repository
git clone https://github.com/user/repo.git
git clone git@github.com:user/repo.git   # SSH

## Basic Workflow
# Check status
git status

# Stage changes
git add <file>
git add .          # stage all changes

# Commit
git commit -m "Commit message"

# Push to remote
git push origin main

# Pull updates
git pull

## Branching
# List branches
git branch

# Create a new branch
git branch feature/awesome

# Switch to a branch
git checkout feature/awesome
# Or using the newer command
git switch feature/awesome

# Create and switch in one step
git checkout -b feature/awesome
# Or
git switch -c feature/awesome

# Merge a branch into the current one
git merge feature/awesome

# Delete a branch
git branch -d feature/awesome

## Stashing
# Save uncommitted changes
git stash

# List stashes
git stash list

# Apply the most recent stash
git stash apply

# Drop a stash
git stash drop

## Inspection
# Show commit log
git log
git log --oneline --graph --decorate

# Show changes
git diff               # unstaged changes
git diff --staged      # staged changes
git show <commit>

# Show a file’s history
git log -- <path/to/file>

## Remote Management
# List remotes
git remote -v

# Add a new remote
git remote add upstream https://github.com/other/repo.git

# Fetch from remote
git fetch upstream

# Pull from a specific remote/branch
git pull upstream main

# Push to a specific remote/branch
git push upstream feature/awesome

## Tagging
# Create an annotated tag
git tag -a v1.0.0 -m "Release 1.0.0"

# List tags
git tag

# Push tags to remote
git push origin --tags

## Rewriting History (use with care)
# Amend the most recent commit
git commit --amend -m "Updated commit message"

# Interactive rebase for multiple commits
git rebase -i HEAD~3

# Reset to a previous commit (hard)
git reset --hard <commit>

## Useful Aliases (add to ~/.gitconfig)
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    df = diff
    lg = log --oneline --graph --decorate
    amend = commit --amend
    unstage = reset HEAD --

# End of Git notes
"""

def get_git_notes() -> str:
    """
    Return the Git notes string.

    Returns
    -------
    str
        Multi‑line string containing Git commands and tips for Linux.
    """
    return GIT_NOTES

__all__ = ["GIT_NOTES", "get_git_notes"]