.PHONY: check travis test coverage init

app=bkmrk

travis:
	pip install pipenv
	pipenv install --three --dev

init:
	pipenv install --three --dev

check:
	pipenv check --style $(app)/*.py $(app)/tests/*.py

test:
	pipenv run pytest .

coverage:
	pipenv run pytest --cov-report term-missing --cov=./ .
