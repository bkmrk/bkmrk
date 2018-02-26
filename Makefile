.PHONY: check travis test coverage init run

app=bkmrk

init:
	pipenv install --three --dev

check:
	pipenv check --style $(app)/*.py $(app)/tests/*.py

test:
	pipenv run pytest .

coverage:
	pipenv run pytest --cov-report term-missing --cov=./ .

run:
	pipenv run flask run
