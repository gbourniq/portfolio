# Set shell
SHELL=/bin/bash -e -o pipefail

# Cosmetics
RED := "\e[1;31m"
YELLOW := "\e[1;33m"
GREEN := "\033[32m"
NC := "\e[0m"
INFO := @bash -c 'printf $(YELLOW); echo "[ANSIBLE] $$1"; printf $(NC)' MESSAGE
INSTRUCTION := @bash -c 'printf $(NC); echo "   $$1"; printf $(NC)' MESSAGE
SUCCESS := @bash -c 'printf $(GREEN); echo "[SUCCESS] $$1"; printf $(NC)' MESSAGE
WARNING := @bash -c 'printf $(RED); echo "[WARNING] $$1"; printf $(NC)' MESSAGE

ENVIRONMENT_NAME=portfolio

### REPO ###
.PHONY: pre-commit
pre-commit:
	@pre-commit install -t pre-commit -t commit-msg
	${SUCCESS} "pre-commit installed"


### CONDA ###
.PHONY: env
env:
	${INFO} "Creating conda environment and running `poetry install`"
	@conda env create
	@conda activate ${ENVIRONMENT_NAME}
	@poetry install
	${SUCCESS} "Success"

### PACKAGE ###
# .PHONY: portfolio
# mvp:
# 	${INFO} "Building portfolio package"
# 	python package/builder.py --name ${ENVIRONMENT_NAME}
# 	${SUCCESS} "Success"

