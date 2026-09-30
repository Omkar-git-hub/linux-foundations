"""
Git Learning Notes for Linux

This module provides a concise guide to common Git operations
useful for developers working on Linux systems. The notes are
intended for educational purposes and can be used as a quick
reference.

Functions
---------
get_git_notes() -> str
    Returns a formatted string containing the Git learning guide.
"""

def get_git_notes() -> str:
    """
    Return a formatted guide covering essential Git commands and concepts
    for Linux users.

    The guide includes sections on repository setup, basic workflow,
    branching, remote interactions, and useful configuration tips.
    """
    notes = """
# Git Learning Guide (Linux)

## 1. Install Git
```bash
# Debian/Ubuntu
sudo apt-get update && sudo apt-get install git

# Fedora
sudo dnf install git

# Arch
sudo pacman -S git
```

## 2. Configure Git
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
# Optional: set default editor
git config --global core.editor "vim"
# Optional: enable colored output
git config --global color.ui auto
```

## 3. Initialize a Repository
```bash
mkdir my-project && cd my-project
git init
```

## 4. Basic Workflow
```bash
# Create or modify files
git add <file>          # stage a specific file
git add .               # stage all changes
git status              # view staged/unstaged changes
git commit -m "Message" # commit staged changes
git log                 # view commit history
```

## 5. Branching
```bash
git branch               # list branches
git branch <name>        # create a new branch
git checkout <name>      # switch to branch
git checkout -b <name>   # create and switch in one step
git merge <branch>       # merge branch into current
git branch -d <name>     # delete a branch
```

## 6. Working with Remotes
```bash
# Add a remote repository
git remote add origin https://github.com/user/repo.git

# Push commits
git push -u origin master   # first push, sets upstream
git push                    # subsequent pushes

# Pull changes
git pull                    # fetch + merge
git fetch                   # fetch without merging
git pull --rebase           # rebase instead of merge
```

## 7. Undoing Changes
```bash
# Unstage a file
git reset <file>

# Discard local changes (unstaged)
git checkout -- <file>

# Amend last commit
git commit --amend

# Reset to a previous commit
git reset --hard <commit_hash>
```

## 8. Stashing
```bash
git stash               # save uncommitted changes
git stash list          # view stash entries
git stash apply         # reapply most recent stash
git stash pop           # apply and drop stash
git stash drop stash@{0}# delete specific stash
```

## 9. Useful Tips
- Use `git status -s` for a short status view.
- Alias common commands in `~/.gitconfig`:
  ```
  [alias]
      co = checkout
      br = branch
      ci = commit
      st = status
  ```
- Enable credential caching:
  ```bash
  git config --global credential.helper cache
  ```

## 10. Resources
- Official documentation: https://git-scm.com/doc
- Pro Git book (free online): https://git-scm.com/book/en/v2
- Git cheat sheet: https://education.github.com/git-cheat-sheet-education.pdf
"""
    return notes.strip()