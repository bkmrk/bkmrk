import pytest
import os
import tempfile

from .fixtures import *

import bkmrk


def test_init_file_logger(app):
    """Test init_file_logger."""
    with tempfile.TemporaryDirectory() as tmpdir:
        bkmrk.utils.init_file_logger(app, log_dir=tmpdir)


def test_init_file_logger_nonexisting_dir(app):
    """Test init_file_logger with nonexisting_dir."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.rmdir(tmpdir)
        bkmrk.utils.init_file_logger(app, log_dir=tmpdir)
