"""
This script contains the routes for the error handlers.

This installs application-wide error handlers
"""
from flask import jsonify
from .jsend import error


def not_found(message="The specified resource cannot be found."):
    """
    The handler handles the 404 (Resource not found) error.
    
    This returns a json object with a description of the error type.
    """

    response = {
        'status': 404,
        'error': 'Resource not found',
        'message': message
    }
    response.status_code = 404
    return response


def bad_request(message):
    """
    The handler handles the 400 (Bad Request) error.

    This returns a json object with a description of the error type.
    """
    response = {
        'status': 400,
        'error': "Bad Request",
        'message': message
    }
    return error(response), 400


def unauthorized(message):
    """
    The handler handles the 401 (Unauthorized) error.

    This returns a json object with a description of the error type.
    """
    response = {
        'status': 401,
        'error': "Unauthorized",
        'message': message
    }
    return error(response), 401


def token_error(message):
    """
    Handle errors relating to token.

    THis returns a json object describing the token error.
    """
    response = jsonify({
        'status': 401,
        'error': "Token Error",
        'message': message
    })
    response.status_code = 401
    return response
