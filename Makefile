PYTHON ?= python3

.PHONY: help test lint typecheck validate

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

test: ## Run test suite
	$(PYTHON) -m pytest tests/ -x -v

lint: ## Run ruff linter
	$(PYTHON) -m ruff check src/ tests/

typecheck: ## Run mypy type checking
	$(PYTHON) -m mypy src/

validate: lint typecheck test ## Run all checks (lint, typecheck, test)
