.PHONY: check travis test coverage init run db clean-db clean-pyc clean

app=bkmrk
run=pipenv run
env=FLASK_APP=flask_run.py FLASK_DEBUG=1

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-db:
	-rm -rf migrations
	-rm bkmrk/app.db

clean: clean-pyc

db: clean-db
	$(env) $(run) flask db init
	$(env) $(run) flask db migrate
	$(env) $(run) flask db upgrade

install:
	pipenv install --dev

check:
	$(run) pycodestyle

test:
	$(run) pytest $(app)

coverage:
	$(run) pytest --cov-report term-missing --cov=./ $(app)

run:
	$(env) $(run) flask run
