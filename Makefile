VENV = venv

# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## This help.
	@echo ""
	@echo "Usage: make [COMMAND] cmd='[EXTRA ARGUMENTS]'"
	@echo ""
	@echo "COMMAND LIST:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "EXTRA ARGUMENTS EXAMPLE:"
	@echo "make startapp cmd='appname'"

.DEFAULT_GOAL := help

#############################
# Venv management commands
#############################
install-test: ## Install test requirements
	pip install .[test]

venv: ## Create a venv and install test requirements
	$(shell which python3) -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -e .[test]

#############################
# Sandbox management commands
#############################
sandbox-build: sandbox-clean venv sandbox-install ## Create a sandbox from scratch, delete the database if it exists

sandbox-clean: ## Destroy sandbox database 
	rm -rf sandbox/db.sqlite3

sandbox-install: ## Migrate the database
	python sandbox/manage.py migrate

#############################
# Test management commands
#############################
test: ## Run test
	cd sandbox && python manage.py test .

pytest: ## Run Pytest
	cd sandbox && pytest ../tests/

.PHONY: help install-test venv sandbox-build sandbox-clean sandbox-install tests
