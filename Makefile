.PHONY: check init test

app=bkmrk

init:
	pip install pipenv
	pipenv install --three --dev

check:
	pipenv check --style $(app)/*.py $(app)/tests/*.py

test:
	pipenv run pytest .
