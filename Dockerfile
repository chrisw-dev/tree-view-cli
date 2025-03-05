# Use the official astral-sh/uv Python image for a faster build
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Set working directory
WORKDIR /app

# Enable optimization settings
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_NO_INSTALLER_METADATA=1

# First, install only the dependencies to leverage Docker cache
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Now copy the application code and complete the installation
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --compile-bytecode

# Create non-root user for security
RUN useradd -m appuser && \
    chown -R appuser:appuser /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

RUN mkdir -p /app/htmlcov && \
    chown -R appuser:appuser /app/htmlcov && \
    chmod -R 777 /app/htmlcov

# Switch to non-root user
USER appuser

# Reset the entrypoint and set the command
ENTRYPOINT []
CMD ["python", "tree_view_cli.py", "."]
