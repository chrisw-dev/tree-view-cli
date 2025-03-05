.PHONY: install-uv up down

install-uv:
	@echo "Installing Astral UV..."
	@if command -v curl >/dev/null 2>&1; then \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	elif command -v wget >/dev/null 2>&1; then \
		wget -qO- https://astral.sh/uv/install.sh | sh; \
	else \
		echo "Error: Neither curl nor wget is available. Please install one of them."; \
		exit 1; \
	fi
	@echo "Astral UV installed successfully."

check-uv:
	@uv --version || (echo "Astral UV is not installed or not in PATH" && exit 1)

sync:
	@uv sync

editable:
	@uv pip install -e .

up:
	docker compose up -d --build

down:
	docker compose down --remove-orphans  --rmi local --volumes

all: install-uv check-uv sync editable up

.DEFAULT_GOAL := up
