#!/bin/bash

outdated:
	@pip list --outdated

test:
	@py.test

test-matching:
	@py.test -sk $(test)

coverage:
	@py.test --cov=service_repository --cov-report=term-missing --cov-fail-under=80 tests/

flake8:
	@flake8 --show-source service_repository tests

check-import:
	@isort service_repository tests --multi-line=3 --trailing-comma --force-grid-wrap=0 --use-parentheses --check-only

fix-import:
	@poetry run isort service_repository tests

check-black:
	@black service_repository tests --line-length 79 --check

fix-black:
	black service_repository tests --line-length 79

check-bandit:
	@bandit -r -f custom -x tests service_repository tests

check-safety:
	safety check --file=requirements/production.txt

check-dead-fixtures:
	@pytest --dead-fixtures

lint: fix-import fix-black flake8

check-lint: check-import check-black check-bandit flake8 check-dead-fixtures