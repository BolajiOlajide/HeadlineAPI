"""
Create an context for access the application from an interactive shell.

Write a function to import all the context and objects needed for a shell
prompt.
"""

import dotenv

from headline import db, create_app
from headline.models import User

dotenv.load()

app = create_app(dotenv.get('FLASK_CONFIG'))


def make_shell_context():
    """
    Create a context for interacting in a shell for the application.

    Import the model objects to enable easy interaction.
    """
    return dict(app=app, db=db, User=User)
