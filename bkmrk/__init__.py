from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from .config import Config
from . import utils


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

    utils.add_stream_logger(app)

    return app
