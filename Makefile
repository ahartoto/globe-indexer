# Filename: Makefile

# Global configurations
NUKE := /bin/rm -rf

PYTHON := python3
PYLINT := pylint
PYTEST := py.test

# App configurations
PKG := globe_indexer
TEST_DPATH := tests

.PHONY:
clean:
	-@$(NUKE) __pycache__ .cache build $(PKG).egg-info .coverage htmlcov
	@cd docs; make clean

.PHONY:
lint:
	@$(PYLINT) $(PKG)

.PHONY:
test:
	@$(PYTEST) $(TEST_DPATH) 

.PHONY:
coverage:
	@$(PYTEST) --cov=$(PKG) $(TEST_DPATH) 

.PHONY:
html:
	@cd docs; make html
