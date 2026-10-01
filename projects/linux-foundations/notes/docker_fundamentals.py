"""
Docker Fundamentals Notes

This module provides a concise reference of Docker concepts, commands,
and best practices. It is intended for educational purposes and can be
imported to access the documentation programmatically.

Typical usage:

    from projects.linux_foundations.notes.docker_fundamentals import (
        DOCKER_OVERVIEW,
        COMMON_COMMANDS,
        BEST_PRACTICES,
    )
"""

DOCKER_OVERVIEW = """
Docker is a platform for developing, shipping, and running applications
inside lightweight, portable containers. Containers bundle an
application and its dependencies, ensuring consistent behavior across
different environments.

Key concepts:
- **Image**: A read‑only template that defines the filesystem and
  configuration of a container.
- **Container**: A runnable instance of an image, isolated from the host
  system and other containers.
- **Dockerfile**: A script of instructions to build an image.
- **Registry**: A service (e.g., Docker Hub) that stores and distributes
  images.
"""

COMMON_COMMANDS = """
# Image management
docker pull <image>          # Download an image from a registry
docker build -t <tag> .      # Build an image from a Dockerfile in the current directory
docker images                # List local images
docker rmi <image>           # Remove a local image

# Container lifecycle
docker run -d --name <c> <image>          # Run a container in detached mode
docker ps                                 # List running containers
docker ps -a                              # List all containers (including stopped)
docker stop <c>                           # Stop a running container
docker start <c>                          # Start a stopped container
docker rm <c>                             # Remove a container
docker exec -it <c> /bin/bash            # Open an interactive shell inside a container

# Networking
docker network ls                         # List networks
docker network create <net>               # Create a new network
docker run --network <net> ...            # Attach container to a specific network

# Volumes and data persistence
docker volume ls                          # List volumes
docker volume create <vol>                # Create a volume
docker run -v <vol>:/path/in/container ...# Mount a volume into a container
"""

BEST_PRACTICES = """
1. **Use .dockerignore** – Exclude unnecessary files from the build context
   to speed up image builds and keep images small.

2. **Leverage multi‑stage builds** – Compile or build artifacts in a temporary
   stage and copy only the final artifacts into a minimal runtime image.

3. **Pin base image tags** – Use specific version tags (e.g., python:3.11-slim)
   instead of `latest` to ensure reproducible builds.

4. **Run as non‑root** – Create and switch to a non‑root user inside the
   container to reduce security risks.

5. **Keep containers immutable** – Treat containers as immutable; make
   configuration changes via environment variables or mounted config files
   rather than editing files inside a running container.

6. **Limit resources** – Use `--memory`, `--cpus`, and other resource limits
   to prevent a container from exhausting host resources.

7. **Tag images appropriately** – Follow a tagging convention such as
   `<repo>:<app>-<version>` to simplify version tracking and rollbacks.
"""

# End of Docker fundamentals notes