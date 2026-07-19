.PHONY: help sync generate test typecheck lint build check

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

sync:  ## Install/refresh the dev environment
	uv sync --all-packages

PROTO_OUT := packages/cafanasyev-sapient-proto/src

generate: sync  ## Regenerate the google-protobuf package from proto/
	uv run python -m grpc_tools.protoc --proto_path=proto \
		--python_out=$(PROTO_OUT) --pyi_out=$(PROTO_OUT) \
		proto/sapient_msg/*.proto proto/sapient_msg/*/*.proto

build:  ## Build all workspace wheels and sdists
	uv build --all-packages

test:  ## Run the test suite in parallel
	uv run pytest

typecheck:  ## mypy (strict mode and file list come from pyproject.toml)
	uv run mypy

lint:  ## Ruff over all hand-written code
	uv run ruff check .

check: test typecheck lint  ## Tests (parallel) + mypy --strict + ruff
