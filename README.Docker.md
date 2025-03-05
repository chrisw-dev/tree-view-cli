# Docker Setup for tree-view-cli

This document explains how to use Docker with the tree-view-cli project, including both development and production workflows.

## Development Workflow

The Docker environment is configured for optimal development experience with:

- Fast dependency installation using uv
- Efficient layer caching for quick rebuilds
- Volume mounts for live code editing
- Separate services for testing and coverage viewing

### Starting the Development Environment

Build and start the development environment:

If you enviroment has Make
```bash
make up
```

Or
```bash
docker compose up --build
```

This will:
1. Build the Docker image with your application
2. Start two services:
   - `tree-view-cli`: Serves test coverage reports at http://localhost:8000
   - `dev`: Runs the test suite

For teardown the containers
```bash
make down
```

Or
```bash
docker compose down --remove-orphans  --rmi local --volumes
```

### Working with the Environment

- Edit code locally, and changes will be reflected immediately in the container
- Test results and coverage reports are stored in a persistent Docker volume
- Resource limits prevent the container from consuming excessive resources

## Production Deployment

For production deployment, the Dockerfile is optimized for security and efficiency:

- Uses the official astral-sh/uv Python image
- Implements proper dependency caching
- Runs as a non-root user for enhanced security
- Includes bytecode compilation for better performance
- Minimizes image size through optimal layer management

### Building for Production

Build the production image:

```bash
docker build -t tree-view-cli .
```

If deploying to a different architecture (e.g., from Apple Silicon to x86):

```bash
docker build --platform=linux/amd64 -t tree-view-cli .
```

## References

- [Docker Python Guide](https://docs.docker.com/language/python/)
- [uv Documentation](https://github.com/astral-sh/uv/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Docker Build Reference](https://docs.docker.com/engine/reference/commandline/build/)
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
