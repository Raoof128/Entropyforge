.PHONY: install format format-check lint test check clean

install:
	python -m pip install --upgrade pip
	pip install -e ".[dev]"

format:
	ruff format src tests

format-check:
	ruff format --check src tests

lint:
	ruff check src tests

test:
	pytest tests/ -v --cov=entropyforge --cov-report=term-missing --cov-report=xml

check: format-check lint test

clean:
	rm -rf build dist *.egg-info .coverage coverage.xml htmlcov .pytest_cache .ruff_cache
