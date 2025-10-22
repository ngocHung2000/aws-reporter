ZIP_FILE := aws-reporter.zip

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  test     to perform unit tests."
	@echo "  man      to build the man file from README.md"
	@echo "  install  to install. Use PREFIX and MANPREFIX to customize."

init:
	@bash -c scripts/init.sh

deploy:
	@bash -c scripts/deploy.sh

delete:
	@bash -c scripts/delete.sh
.PHONY: help test man