"""This aims to jsendify all responses coming from the API."""
from flask import jsonify


def success(data):
    """Response for a successful API call or whatever."""

    response = {
        "status": "success",
        "data": data
    }
    return jsonify(response)


def failure(message):
    """Response for a failed API call or whatever."""

    response = {
        "status": "failure",
        "message": message
    }
    return jsonify(response)


def error(data):
    """Response for an errored call or whatever."""

    response = {
        "status": "error",
        "details": data
    }
    return jsonify(response)
