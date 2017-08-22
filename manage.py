"""
Python script for managing the flask application.

This is the script that starts the flask application.
"""

import unittest

import dotenv
from flask_migrate import Migrate, MigrateCommand
from flask_script import Shell, Manager, prompt_bool, Server

from headline import db, create_app
from shell import make_shell_context

dotenv.load()
app = create_app(dotenv.get('FLASK_CONFIG'))
db.init_app(app)
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server())


@manager.command
def test():
    """
    Add custom command to the manage.py script.
    The method runs all the test cases using the unittest module.
    """
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def create_db():
    """
    Create the database tables.
    Using the SQLAlchemy models the method creates database tables
    """
    app = create_app(dotenv.get('FLASK_CONFIG'))
    with app.app_context():
        db.create_all()


@manager.command
def drop_db():
    """
    Delete all database tables .
    Drops all tables in the database after confirmation from the user.
    """
    if prompt_bool("Are you sure you want to lose all your data?"):
        app = create_app(dotenv.get('FLASK_CONFIG'))
        with app.app_context():
            db.drop_all()


# Define root route
@app.route('/')
def index():
    """
    Index route for Headline NG API.

    Doesn't require authentication, just there for the user to know what's up.
    """
    return '<h1>Welcome to Headline-NG API</h1>'


# Run the application using the Flask manager
if __name__ == '__main__':
    manager.run()
