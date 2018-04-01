import json
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_processes(host):
    assert host.process.get(user='root', comm='hab-sup')
    assert host.process.get(user='root', comm='hab-launch')


def test_habitat_cmd(host):
    assert host.exists('hab')


def test_habitat_service(host):
    services_json = host.check_output('curl localhost:9631/services')
    services = json.loads(services_json)
    assert len(services) == 1
    nginx_service = services[0]
    assert nginx_service.get('pkg').get('origin') == 'core'
    assert nginx_service.get('pkg').get('name') == 'nginx'
