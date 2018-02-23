.PHONY: check init test coverage

app=bkmrk

init:
	pip install pipenv
	pipenv install --three --dev

check:
	pipenv check --style $(app)/*.py $(app)/tests/*.py

test:
	pipenv run pytest .

coverage:
	pipenv run pytest --cov-report term-missing --cov=./ .
