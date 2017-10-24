# Filename: Makefile

# Global configurations
NUKE := /bin/rm -rf

PYTHON := python3
PYLINT := pylint
PYTEST := pytest

# App configurations
PKG := globe_indexer

.PHONY:
clean:
	-@$(NUKE) __pycache__ .cache build $(PKG).egg-info

.PHONY:
lint:
	@$(PYLINT) $(PKG)

.PHONY:
test:
	@$(PYTEST) tests
