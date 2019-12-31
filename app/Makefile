LOGS_FILE=info.log

# Import local environment overrides
include .env

# Set shell
SHELL=/bin/bash -e -o pipefail

# Cosmetics
RED := "\e[1;31m"
YELLOW := "\e[1;33m"
GREEN := "\033[32m"
NC := "\e[0m"
INFO := @bash -c 'printf $(YELLOW); echo "=> $$1"; printf $(NC)' MESSAGE
INSTRUCTION := @bash -c 'printf $(NC); echo "   $$1"; printf $(NC)' MESSAGE
SUCCESS := @bash -c 'printf $(GREEN); echo "[SUCCESS] $$1"; printf $(NC)' MESSAGE
WARNING := @bash -c 'printf $(RED); echo "[WARNING] $$1"; printf $(NC)' MESSAGE

run-test:
	${INFO} "Running tests"
	@ pytest .
	${SUCCESS} "Tests run successful"

coverage:
	${INFO} "Running test coverage scan"
	@ pytest --cov=. --cov-report=term-missing
	${SUCCESS} "Coverage run successful"

run:
	${INFO} "Running app with DEBUG=${DEBUG}"
	@ python manage.py runserver

logs-show:
	${INFO} "Watching logs"
	@ tail -n2 -f ${LOGS_FILE}

logs-clear:
	${INFO} "Watching logs"
	@ echo "" > ${LOGS_FILE}
