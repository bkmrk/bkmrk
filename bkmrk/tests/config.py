from ..config import Config


class TestConfig(Config):
    SERVER_NAME = 'localhost'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    MAIL_ADMIN = 'mail.bkmrk@email.com'
