# Git doesn't track .git/hooks, so a fresh clone has no pre-commit hook until
# `make install-hooks` runs. The hook lost this way once already (re-clone,
# 2026-09-07); the weekly com.localfirst.blog-validation job is the backstop.

.PHONY: help serve install-hooks validate check-hooks

help:
	@echo "make serve          - hugo server with drafts"
	@echo "make install-hooks  - install the code-block pre-commit hook (run after every clone)"
	@echo "make check-hooks    - fail if the pre-commit hook is missing or out of date"
	@echo "make validate       - run every code block in every post"

serve:
	hugo server -D

install-hooks:
	install -m 755 scripts/hooks/pre-commit .git/hooks/pre-commit
	@echo "pre-commit hook installed"

check-hooks:
	@cmp -s scripts/hooks/pre-commit .git/hooks/pre-commit \
		&& echo "pre-commit hook is installed and current" \
		|| { echo "pre-commit hook missing or stale: run make install-hooks"; exit 1; }

validate:
	blog-validate check --all
