"""
Define models for Headline application.

The SQLAlchemy models for the database is defined here.
"""

from datetime import datetime

from flask import current_app
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature, SignatureExpired)
from werkzeug.security import check_password_hash, generate_password_hash
import sqlalchemy

from . import db
from .id_generator import PushID
from .helpers import to_camel_case


push_id = PushID()


class Base(db.Model):
    """
    Define the Create,Read, Update, Delete mixin.

    Instantiate a mixin to handle save, delete and also handle common model
    columns and methods.
    """

    __abstract__ = True

    id = db.Column(db.String, primary_key=True)
    date_created = db.Column(
        db.DateTime, default=datetime.now(), nullable=False)
    date_modified = db.Column(
        db.DateTime, default=datetime.now(),
        onupdate=datetime.now(), nullable=False)

    def serialize(self):
        """Map model objects to dict representation."""
        return {to_camel_case(column.name): getattr(self, column.name)
                for column in self.__table__.columns}

    def save(self):
        """
        Save to database.

        Save instance of the object to database and commit.
        """
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except (sqlalchemy.exc.SQLAlchemyError,
                sqlalchemy.exc.IntegrityError,
                sqlalchemy.exc.InvalidRequestError):
            db.session.rollback()
            return False

    def delete(self):
        """
        Delete from database.

        Deletes instance of an object from database
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except sqlalchemy.exc.SQLAlchemyError:
            db.session.rollback()
            return False

    @classmethod
    def fetch_all(cls):
        """ Returns all the data in the model"""
        return cls.query.all()

    @classmethod
    def get(cls, *args):
        """Returns data by the Id"""
        return cls.query.get(*args)

    @classmethod
    def count(cls):
        """Returns the count of all the data in the model"""
        return cls.query.count()

    @classmethod
    def get_first_item(cls):
        """Returns the first data in the model"""
        return cls.query.first()

    @classmethod
    def order_by(cls, *args):
        """Query and order the data of the model"""
        return cls.query.order_by(*args)

    @classmethod
    def filter_all(cls, **kwargs):
        """Query and filter the data of the model"""
        return cls.query.filter(**kwargs).all()

    @classmethod
    def filter_by(cls, **kwargs):
        """Query and filter the data of the model"""
        return cls.query.filter_by(**kwargs)

    @classmethod
    def find_first(cls, **kwargs):
        """
        Query and filter the data of a model,
        returning the first result
        """
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def filter_and_count(cls, **kwargs):
        """Query, filter and counts all the data of a model"""
        return cls.query.filter_by(**kwargs).count()

    @classmethod
    def filter_and_order(cls, *args, **kwargs):
        """Query, filter and orders all the data of a model"""
        return cls.query.filter_by(**kwargs).order_by(*args)


class User(Base):
    """
    Set up the User model.

    Set up the properties of the User object and the table name too.
    """

    __tablename__ = 'users'
    username = db.Column(db.String(32), unique=True, index=True,
                         nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    isVerified = db.Column(db.Boolean, default=False)

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
        return s.dumps({'id': self.id})

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

        return {'username': self.username}

    def __repr__(self):
        """
        Display the object.

        Displays the string representation of the User object.
        """

        return '<User: {}>'.format(self.username)


def fancy_id_generator(mapper, connection, target):
    """A function to generate unique identifiers on insert."""
    target.id = push_id.next_id()


# associate the listener function with models, to execute during the
# "before_insert" event
tables = [User]

for table in tables:
    sqlalchemy.event.listen(table, 'before_insert', fancy_id_generator)
