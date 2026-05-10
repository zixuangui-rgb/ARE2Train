.PHONY: doctor smoke test bootstrap check clean-pyc

PYTHON ?= python3

doctor:
	$(PYTHON) scripts/doctor.py

smoke:
	bash scripts/smoke_test.sh

test:
	$(PYTHON) -m unittest discover -s tests -p "test_*.py"

bootstrap:
	bash scripts/bootstrap_env.sh

check: doctor test

clean-pyc:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
