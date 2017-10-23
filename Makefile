# Filename: Makefile

# Global configurations
PYTHON := python3
PYLINT := pylint
PYTEST := pytest

# App configurations
PKG := globe_indexer


.PHONY:
lint:
	@$(PYLINT) $(PKG)

.PHONY:
test:
	@$(PYTEST) tests
