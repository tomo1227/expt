.DEFAULT_GOAL := check

.PHONY: check check-config check-aidlc check-whitespace aidlc-setup

check: check-config check-aidlc check-whitespace

aidlc-setup:
	aidlc config --harness copilot --yes

check-config:
	python3 -m json.tool .devcontainer/devcontainer.json > /dev/null
	sh -n .devcontainer/install-aidlc.sh

check-aidlc:
	python3 scripts/check_aidlc.py

check-whitespace:
	git diff --check