from flask import Blueprint

bp = Blueprint('errors', __name__)

from bkmrk.errors import handlers
