.PHONY: help sync generate test typecheck build check

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

sync:  ## Install/refresh the dev environment
	uv sync

generate: sync  ## Regenerate protobuf modules and type stubs from proto/
	uv run python scripts/generate.py

test:  ## Run the test suite in parallel
	uv run pytest

typecheck:  ## Type-check the typed usage sample under mypy --strict
	uv run mypy --strict tests/typing_sample.py

build:  ## Build the wheel and sdist
	uv build

check: test typecheck  ## Run tests and type checks
