#!/bin/bash

requirements-dev:
	@poetry install --all-extras

outdated:
	@poetry show --outdated

test:
	@poetry run pytest

test-matching:
	@poetry run pytest -sk $(test) --asyncio-mode=strict

coverage:
	@poetry run pytest --cov=service_repository --cov-report=term-missing --cov-fail-under=80 tests/

flake8:
	@poetry run flake8 --show-source service_repository tests

check-import:
	@poetry run isort service_repository tests --multi-line=3 --trailing-comma --force-grid-wrap=0 --use-parentheses --check-only

fix-import:
	@poetry run isort service_repository tests

check-black:
	@poetry run black service_repository tests --line-length 79 --check

fix-black:
	@poetry run black service_repository tests --line-length 79

check-bandit:
	@poetry run bandit -r -f custom -x tests service_repository tests

check-safety:
	@poetry export --without-hashes -f requirements.txt | safety check --full-report --stdin

check-dead-fixtures:
	@poetry run pytest --dead-fixtures

lint: fix-import fix-black flake8

check-lint: check-import check-black check-bandit flake8 check-dead-fixtures