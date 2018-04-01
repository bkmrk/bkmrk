.PHONY: check setup-app install

check:
	pipenv run yamllint .

setup-app: install
	ansible-playbook -i inventory -l app_servers -u root app.yml

install:
	ansible-galaxy install -r requirements.yml
