PY_MODULE := abi3info

# Optionally overridden by the user in the `test` target.
TESTS :=

# If the user selects a specific test pattern to run, set `pytest` to fail fast
# and only run tests that match the pattern.
# Otherwise, run all tests and enable coverage assertions, since we expect
# complete test coverage.
ifneq ($(TESTS),)
	TEST_ARGS := -x -k $(TESTS)
	COV_ARGS :=
else
	TEST_ARGS :=
	COV_ARGS := --fail-under 100
endif

.PHONY: all
all:
	@echo "Run my targets individually!"

.PHONY: dev
dev:
	uv sync

.PHONY: codegen
codegen:
	uv run --dev --script codegen/codegen.py

.PHONY: lint
lint:
	uv run --dev ruff format --check
	uv run --dev ruff check
	uv run --dev mypy $(PY_MODULE)
	uv run --dev interrogate -c pyproject.toml .

.PHONY: reformat
reformat:
	uv run --dev ruff format
	uv run --dev ruff check --fix

.PHONY: test tests
test tests:
	uv run --dev pytest --cov=$(PY_MODULE) $(T) $(TEST_ARGS)
	uv run --dev python -m coverage report -m $(COV_ARGS)

.PHONY: doc
doc:
	uv run --dev pdoc $(PY_MODULE) -o html

.PHONY: dist
dist:
	uv build

