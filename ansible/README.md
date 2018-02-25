# Ansible (Server Management)

## Setup Webserver

`pipenv run ansible-playbook -K -u <remote-user> -i inventory webservers.yml`

## Deploy App

`pipenv run ansible-playbook -K -u <remote-user> -i inventory app.yml`
