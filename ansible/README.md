# Ansible (Server Management)

## Setup Webserver

`ansible-playbook -K -u <remote-user> -i inventory webservers.yml`

## Deploy App

`ansible-playbook -K -u <remote-user> -i inventory app.yml`
