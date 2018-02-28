.PHONY: check travis test coverage init run db

app=bkmrk
run=pipenv run

db:
	$(run) flask db init
	$(run) flask db migrate
	$(run) flask db upgrade

init:
	pipenv install --three --dev

check:
	$(run) pycodestyle

test:
	$(run) pytest .

coverage:
	$(run) pytest --cov-report term-missing --cov=./ .

run:
	$(run) flask run
