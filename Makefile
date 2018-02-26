.PHONY: check travis test coverage init run

app=bkmrk

init:
	pipenv install --three --dev

check:
	pipenv run pycodestyle

test:
	pipenv run pytest .

coverage:
	pipenv run pytest --cov-report term-missing --cov=./ .

run:
	pipenv run flask run
