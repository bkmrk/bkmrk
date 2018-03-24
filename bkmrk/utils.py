import logging
from logging.handlers import RotatingFileHandler
import os

from openlibrary_api.client import OpenLibraryClient


def init_file_logger(app, log_dir='logs'):
    """Initialize a rotating file logger."""
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    file_handler = RotatingFileHandler(os.path.join(log_dir, 'bkmrk.log'), maxBytes=10240, backupCount=10)
    fmt = '(%(asctime)s) [%(levelname)s] %(message)s [in %(pathname)s:%(lineno)d]'
    file_handler.setFormatter(logging.Formatter(fmt))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('BKMRK Initialized')


def get_openlibrary_book(isbn, client=None):
    if client is None:
        client = OpenLibraryClient()
    bibkey = 'ISBN:{}'.format(isbn)
    ol_book = client.books(bibkeys=bibkey, format='json', jscmd='data')
    return ol_book.get(bibkey)
