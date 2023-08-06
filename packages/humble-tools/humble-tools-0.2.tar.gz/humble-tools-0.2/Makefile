PYTHON_SCRIPT_PATH := bin
VENV_NAME := .venv
VENV_BIN_PATH := ./.venv/$(PYTHON_SCRIPT_PATH)
VENV_PYTHON := $(VENV_BIN_PATH)/python
VENV_PIP := $(VENV_BIN_PATH)/pip
VENV_PYLINT := $(VENV_BIN_PATH)/pylint
VENV_TWINE := $(VENV_BIN_PATH)/twine

PROJECT_NAME := cwb

SOURCE_PATH = src/$(PROJECT_NAME)

clean:
	-rm -rf $(VENV_NAME)
	-rm -rf src/*.egg-info

develop: clean
	python3.8 -m venv .venv
	$(VENV_PIP) install --upgrade pip wheel
	$(VENV_PIP) install -e .[develop]

lint:
	$(VENV_PYLINT) $(SOURCE_PATH)

ci: lint
	$(VENV_BIN_PATH)/py.test --cov=$(SOURCE_PATH) --cov-report xml:coverage.xml --junitxml=junit.xml tests

coverage:
	$(VENV_BIN_PATH)/py.test --cov=$(SOURCE_PATH) --cov-report term-missing tests

.PHONY: dist
dist:
	-rm -rf dist/ build/
	$(VENV_PYTHON) setup.py sdist

