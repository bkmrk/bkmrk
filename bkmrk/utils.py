import logging
import os
import sys


def add_stream_logger(app, stream=sys.stdout):
    """Initialize a rotating file logger."""
    handler = logging.StreamHandler(stream=stream)
    fmt = '[%(levelname)s] (%(asctime)s) %(message)s [in %(pathname)s:%(lineno)d]'
    handler.setFormatter(logging.Formatter(fmt))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('BKMRK Initialized')
