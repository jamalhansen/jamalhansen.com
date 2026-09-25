# Git doesn't track .git/hooks, so a fresh clone has no pre-commit hook until
# `make install-hooks` runs. The hook lost this way once already (re-clone,
# 2026-09-07); the weekly com.localfirst.blog-validation job is the backstop.

.PHONY: help serve install-hooks validate check-hooks publish find preview drift

help:
	@echo "make serve          - hugo server with drafts"
	@echo "make install-hooks  - install the code-block pre-commit hook (run after every clone)"
	@echo "make check-hooks    - fail if the pre-commit hook is missing or out of date"
	@echo "make validate       - run every code block in every post"
	@echo "make publish POST=<vault note>    - convert a vault post into its page bundle"
	@echo "make find FIND=<vault find>       - convert a vault find into content/finds/"
	@echo "make preview POST=<vault note>    - render a note as a draft in the real theme"
	@echo "make drift                        - list published posts where vault and site disagree"

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

# Publishing goes through obsidian-hugo-bridge (uv tool install ~/projects/local-first/obsidian-hugo-bridge).
# POST/FIND may be absolute or relative to the vault. Extra flags: ARGS="--overwrite", ARGS="--dry-run".
VAULT ?= $(HOME)/vaults/BrainSync
note = $(if $(filter /%,$(1)),$(1),$(VAULT)/$(1))

publish:
	@test -n "$(POST)" || { echo "usage: make publish POST=<vault note> [ARGS=--overwrite]"; exit 2; }
	obsidian-hugo publish post "$(call note,$(POST))" --hugo-dir . --vault-path "$(VAULT)" $(ARGS)

find:
	@test -n "$(FIND)" || { echo "usage: make find FIND=<vault find>"; exit 2; }
	obsidian-hugo publish find "$(call note,$(FIND))" --hugo-dir . $(ARGS)

preview:
	@test -n "$(POST)" || { echo "usage: make preview POST=<vault note>"; exit 2; }
	obsidian-hugo preview "$(call note,$(POST))" --hugo-dir . --vault-path "$(VAULT)" $(ARGS)

drift:
	obsidian-hugo drift --hugo-dir . --vault-blog "$(VAULT)/blog" $(ARGS)
