.PHONY: readme-audit install

PYTHON ?= python3
REPOS_ROOT ?= $(BRAGA_REPOS_ROOT)

install:
	$(PYTHON) -m pip install -r requirements.txt

readme-audit:
	@if [ -n "$(REPOS_ROOT)" ]; then \
		BRAGA_REPOS_ROOT="$(REPOS_ROOT)" $(PYTHON) tools/readme_audit.py --all; \
	else \
		$(PYTHON) tools/readme_audit.py --all; \
	fi
