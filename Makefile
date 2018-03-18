.PHONY: check travis test coverage init run db

app=bkmrk
run=pipenv run

db:
	$(run) flask db init

init:
	pipenv install --three --dev

check:
	$(run) pycodestyle

test:
	$(run) pytest .

coverage:
	$(run) pytest --cov-report term-missing --cov=./ .

run:
	FLASK_APP=flask_run.py FLASK_DEBUG=1 $(run) flask run
