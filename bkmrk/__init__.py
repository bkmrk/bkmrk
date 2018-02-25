import logging
from logging.handlers import RotatingFileHandler
import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from .config import Config


bootstrap = Bootstrap()
db = SQLAlchemy()
login = LoginManager()
login.login_message = 'Please log in to access this page.'
login.login_view = 'auth.login'
mail = Mail()
migrate = Migrate()
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap.init_app(app)
    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    from bkmrk.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from bkmrk.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from bkmrk.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/bkmrk.log', maxBytes=10240, backupCount=10)
        fmt = '(%(asctime)s) [%(levelname)s] %(message)s [in %(pathname)s:%(lineno)d]'
        file_handler.setFormatter(logging.Formatter(fmt))
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('BKMRK Initialized')

    return app
