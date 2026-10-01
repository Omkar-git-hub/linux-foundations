"""
GitHub Actions Notes

This module contains notes about using GitHub Actions for CI/CD workflows.
"""

def get_notes() -> str:
    """
    Return a string containing GitHub Actions notes.

    Returns
    -------
    str
        Multiline string with GitHub Actions related notes.
    """
    notes = """
GitHub Actions Overview
-----------------------
- GitHub Actions enables automation of software workflows directly in a
  repository.
- Workflows are defined in YAML files located in `.github/workflows/`.

Key Concepts
------------
- **Workflow**: A configurable automated process that runs one or more jobs.
- **Job**: A set of steps that execute on the same runner.
- **Step**: An individual task that can be an action or a shell command.
- **Runner**: The environment where jobs are executed (GitHub‑hosted or self‑hosted).

Workflow Syntax
---------------
```yaml
name: CI
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

Common Actions
--------------
- `actions/checkout`: Checks out repository code.
- `actions/setup-python`, `setup-node`, `setup-go`: Configure language runtimes.
- `actions/cache`: Caches dependencies between runs.
- `docker/build-push-action`: Build and push Docker images.

Secrets & Environment Variables
-------------------------------
- Store sensitive data in repository or organization **Secrets**.
- Access via `${{ secrets.NAME }}` in workflow files.
- Define environment variables with `env:` at workflow, job, or step level.

Matrix Builds
-------------
- Run a job multiple times with different parameters:
```yaml
strategy:
  matrix:
    python-version: [3.9, 3.10, 3.11]
```

Self‑Hosted Runners
-------------------
- Install a runner on your own infrastructure for custom environments.
- Register the runner with the repository or organization.

Best Practices
--------------
- Pin action versions (e.g., `actions/checkout@v3`) to avoid breaking changes.
- Use caching to speed up builds.
- Keep workflows DRY by using reusable workflows or composite actions.
- Limit permissions with `permissions:` to the minimum required.

These notes provide a quick reference for creating and maintaining
GitHub Actions workflows.
"""
    return notes.strip()