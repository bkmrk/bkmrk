.PHONY: check travis test coverage init run db clean-db

app=bkmrk
run=pipenv run
env=FLASK_APP=flask_run.py FLASK_DEBUG=1

clean-db:
	rm -rf migrations
	rm bkmrk/app.db

db:
	$(env) $(run) flask db init
	$(env) $(run) flask db migrate
	$(env) $(run) flask db upgrade

install:
	pipenv install --three --dev

check:
	$(run) pycodestyle

test:
	$(run) pytest .

coverage:
	$(run) pytest --cov-report term-missing --cov=./ .

run:
	$(env) $(run) flask run
