import logging
from logging.handlers import RotatingFileHandler
import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment

from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
migrate = Migrate(app, db)
moment = Moment(app)

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/bkmrk.logs', maxBytes=10240, backupCount=10)
    fmt = '(%(asctime)s) [%(levelname)s] %(message)s [in %(pathname)s:%(lineno)d]'
    file_handler.setFormatter(logging.Formatter(fmt))
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('BKMRK Initialized')

from bkmrk import routes, models, errors  # noqa: F401,F402
