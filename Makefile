# BRAGA README Quality Gate — agent and human entry points.
#   make readme-audit           audit every registered repository (needs checkouts under REPOS_ROOT)
#   make readme-audit REPO=..   audit one checkout
#   make readme-fix             apply safe automatic fixes across the portfolio, then re-audit
#   make readme-fix REPO=..     same for one checkout
#   make readme-hero REPO=..    (re)generate the design-system hero banner for one checkout
#   make readme-check           self-check: tests + this repository's own README
#   make test                   run the test suite
PYTHON ?= python
REPOS_ROOT ?= $(if $(BRAGA_REPOS_ROOT),$(BRAGA_REPOS_ROOT),..)
REPO ?=
FONTS ?= $(BK_FONTS)

.PHONY: install readme-audit readme-fix readme-hero readme-check readme-portfolio test

install:
	$(PYTHON) -m pip install -r requirements.txt

readme-audit:
ifneq ($(REPO),)
	$(PYTHON) -m readme_quality --repos-root "$(REPOS_ROOT)" audit --repo "$(REPO)" --verbose
else
	$(PYTHON) -m readme_quality --repos-root "$(REPOS_ROOT)" portfolio
endif

readme-fix:
ifneq ($(REPO),)
	$(PYTHON) -m readme_quality --repos-root "$(REPOS_ROOT)" fix --repo "$(REPO)" $(if $(FONTS),--fonts "$(FONTS)",)
else
	$(PYTHON) -m readme_quality --repos-root "$(REPOS_ROOT)" portfolio --fix $(if $(FONTS),--fonts "$(FONTS)",)
endif

readme-hero:
	$(PYTHON) -m readme_quality --repos-root "$(REPOS_ROOT)" hero --repo "$(REPO)" $(if $(FONTS),--fonts "$(FONTS)",)

readme-portfolio:
	$(PYTHON) -m readme_quality --repos-root "$(REPOS_ROOT)" portfolio --report docs/readme-audit-latest.md

readme-check: test
	$(PYTHON) -m readme_quality --repos-root "$(REPOS_ROOT)" audit --repo . --verbose

test:
	$(PYTHON) -m pytest -q tests
