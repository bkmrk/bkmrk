from bkmrk import app, db
from bkmrk.models import User, Book, BookQuote


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Book': Book,
        'BookQuote': BookQuote,
    }
