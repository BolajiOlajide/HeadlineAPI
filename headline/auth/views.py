"""
Authentication settings for the BucketList API.

Password verification and user registration takes place here.
"""
from flask import g, request
from flask_cors import cross_origin
from flask_httpauth import HTTPBasicAuth

from . import authentication
from headline import errors
from headline.helpers import email_validation
from headline.models import User
from headline.jsend import success


auth = HTTPBasicAuth()


@auth.verify_password
def verify_token(token, password):
    """
    Verify token.

    Verify token, password doesn't need to be present here. The token is going
    to be in the request headers always.
    """
    user = User.verify_auth_token(token)

    if not user:
        return False

    g.user = user
    return True


@authentication.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin()
def login():
    """
    Verify username & password

    Verify the user's identity using the username and password and returns
    a token.
    """
    if not request.json:
        return errors.bad_request("No JSON file detected.")

    _username = request.json.get('username')
    _password = request.json.get('password')

    if not (_username and _password):
        return errors.bad_request("username or password missing")
    
    username = _username.strip()
    password = _password.strip()

    user = User.query.filter_by(username=username).first()
    if not (user and user.verify_password(password)):
        return errors.unauthorized("Username and password didn't match.")

    token = user.generate_auth_token().decode('utf-8')
    response = {
        "token": token,
        "message": "You've been successfully signed in"
    }
    return success(response), 200


@authentication.route('/register', methods=['POST', 'OPTIONS'])
@cross_origin()
def register_user():
    """
    Create a new user.

    Using the supplied information in the body of the request, a new user is
    created using the user name & password provided.
    """
    if not request.json:
        return errors.bad_request("No JSON file detected.")

    _username = request.json.get('username', None)
    _password = request.json.get('password', None)
    _email = request.json.get('email', None)

    if not (_username and _password):
        return errors.bad_request("Username or Password field is missing.")
    
    if not _email:
        return errors.bad_request("Email field is missing.")

    username = _username.strip()
    password = _password.strip()

    if (len(password) < 6):
        return errors.bad_request("Password strength is low. Try again")

    # Email validation
    if not email_validation(_email):
        return errors.bad_request("Please enter a valid email address!")

    if User.query.filter_by(username=username).first():
        return errors.bad_request("username:{} already exist".format(
                                 username))

    user = User(username=username, email=_email)
    user.hash_password(password)
    if user.save():
        token = user.generate_auth_token().decode('utf-8')
        return success({
            "username": user.username,
            "token": token
        }), 201
    else:
        return errors.bad_request("An error occurred while saving. "
                                  "Please try again.")


@auth.error_handler
def auth_error():
    """
    Handle authentication errors.

    Handle all auth errors.
    """
    return errors.unauthorized('Invalid credentials')
