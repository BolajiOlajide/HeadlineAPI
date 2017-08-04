"""
Define models for Headline application.

The SQLAlchemy models for the database is defined here.
"""

from datetime import datetime

from flask import current_app, url_for
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature, SignatureExpired)
from werkzeug.security import check_password_hash, generate_password_hash

from . import db


class CRUDMixin(object):
    """
    Define the Create,Read, Update, Delete mixin.

    Instantiate a mixin to handle save, delete and also handle common model
    columns and methods.
    """

    date_created = db.Column(
        db.DateTime, default=datetime.now(), nullable=False)
    date_modified = db.Column(
        db.DateTime, default=datetime.now(),
        onupdate=datetime.now(), nullable=False)

    def save(self):
        """
        Save to database.

        Save instance of the object to database and commit.
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete from database.

        Deletes instance of an object from database
        """
        db.session.delete(self)
        db.session.commit()


class User(CRUDMixin, db.Model):
    """
    Set up the User model.

    Set up the properties of the User object and the table name too.
    """

    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True,
                         nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def hash_password(self, password):
        """
        Hash user password.

        Passwords shouldn't be stored as string so we hash them.
        """
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        """
        Verify password.

        Use the pwd_context to decrypt the password hash and confirm if it
        matches the initial password set by the user.
        """
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expiration=36000):
        """
        Generate token.

        This function generates a token to be used by the user for requests.
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.user_id})

    @staticmethod
    def verify_auth_token(token):
        """
        Verify token.

        Verify that the token is valid and return the user id.
        """

        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None

            # valid token, but expired
        except BadSignature:
            return None

            # invalid token
        user = User.query.get(data['id'])
        return user

    def to_json(self):
        """
        Display the object properties as a json object.

        Mold up all the properties of User object into an object for display.
        """

        return { 'username': self.username }

    def __repr__(self):
        """
        Display the object.

        Displays the string representation of the User object.
        """

        return '<User: {}>'.format(self.username)
