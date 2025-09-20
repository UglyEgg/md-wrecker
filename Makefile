# Default shell for executing commands
SHELL := /bin/bash

# Project variables
SOURCE_DIR := src/md-wrecker
VENV_DIR := .venv
PYTHON := $(VENV_DIR)/bin/python
VENV_PYTHON := $(VENV_DIR)/bin/python

# Phony targets prevent conflicts with files of the same name.
# This list includes all defined targets.
.PHONY: all help install install-dev clean clean-venv clean-build clean-pyc lint format test docs

# Default target executed when you run `make` without arguments.
all: help

# ==============================================================================
# HELP
# ==============================================================================

help: ## Display this help screen.
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ==============================================================================
# PROJECT SETUP & INSTALLATION
# ==============================================================================

install: ## Create a virtual environment and install the project.
	uv venv $(VENV_DIR)
	uv pip install -e .

install-dev: ## Create a venv and install project with dev and docs dependencies.
	uv venv $(VENV_DIR)
	uv pip install -e ".[dev,docs]"

# ==============================================================================
# CODE QUALITY & TESTING
# ==============================================================================

lint: ## Run the linter (ruff) to check for style and errors.
	@echo "Running linter..."
	uvx ruff check $(SOURCE_DIR) tests

format: ## Format the code using black.
	@echo "Formatting code..."
	uvx black $(SOURCE_DIR) tests

test: ## Run tests using pytest.
	@echo "Running tests..."
	uvx pytest

# ==============================================================================
# DOCUMENTATION
# ==============================================================================

docs: ## Build the Sphinx documentation.
	@echo "Building documentation..."
	@$(VENV_PYTHON) -m sphinx.cmd.build -b html docs/source docs/_build/html

publish-docs: docs ## Build and publish documentation to GitHub Pages.
	@echo "Publishing documentation to GitHub Pages..."
	@ghp-import -n -p docs/_build/html

# ==============================================================================
# CLEANING
# ==============================================================================

clean-venv: ## Remove the virtual environment directory.
	@echo "Removing virtual environment..."
	rm -rf $(VENV_DIR)
	rm -rf docs/_build

clean-build: ## Remove build artifacts.
	@echo "Removing build artifacts..."
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## Remove Python file artifacts.
	@echo "Removing Python file artifacts..."
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

clean: clean-build clean-pyc ## Run all cleaning tasks except for the venv.
	@echo "Project cleaned."
