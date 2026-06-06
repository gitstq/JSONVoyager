# JSONVoyager Makefile
# Cross-platform build automation

.PHONY: install test clean lint build dist run help

PYTHON := python3
PIP := pip3
SCRIPT := jsonvoyager.py

help:
	@echo "🚀 JSONVoyager Build Commands"
	@echo ""
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run test suite"
	@echo "  make run        - Run interactive mode with sample data"
	@echo "  make build      - Build distribution packages"
	@echo "  make clean      - Clean build artifacts"
	@echo "  make lint       - Run code linting"
	@echo "  make format     - Format code"

install:
	$(PIP) install --break-system-packages -e . || $(PIP) install -e .

test:
	$(PYTHON) -m pytest tests/ -v || $(PYTHON) test_jsonvoyager.py

run:
	$(PYTHON) $(SCRIPT) sample.json

build: clean
	$(PYTHON) setup.py sdist bdist_wheel

clean:
	rm -rf build/ dist/ *.egg-info __pycache__ .pytest_cache
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -delete

lint:
	python3 -m flake8 $(SCRIPT) --max-line-length=120 || true
	python3 -m pylint $(SCRIPT) || true

format:
	python3 -m black $(SCRIPT) || true

dist: build
	@echo "📦 Distribution packages built in dist/"
