.DEFAULT_GOAL := check

.PHONY: check check-config check-whitespace

check: check-config check-whitespace

check-config:
	python3 -m json.tool .devcontainer/devcontainer.json > /dev/null

check-whitespace:
	git diff --check