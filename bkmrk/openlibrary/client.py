import requests
from urllib.parse import urljoin

class OpenLibraryClient():
    def __init__(self, base_url='http://openlibrary.org/'):
        self.base_url = base_url

    def search(self, **params):
        r = requests.get(urljoin(self.base_url, 'search.json'), params=params)
        return r.json()
