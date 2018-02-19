.PHONY: init check test

init:
	pip install pipenv
	pipenv install --three --dev

check:
	pipenv check --style bkmrk/*.py bkmrk/tests/*.py

test:
	pipenv run pytest .
