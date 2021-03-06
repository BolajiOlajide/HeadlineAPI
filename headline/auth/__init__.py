"""
Create the authentication Blueprint.

Create and import the views to be used for the Blueprint
"""

from flask import Blueprint

authentication = Blueprint('authentication', __name__)

from . import views
