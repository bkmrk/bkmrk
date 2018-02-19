.PHONY: init lint test

init:
	pip install pipenv
	pipenv install --three --dev

lint:
	pipenv check --style bkmrk/*.py

test:
	pipenv run py.test .
