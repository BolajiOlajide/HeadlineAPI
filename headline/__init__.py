"""
Setup an initialization to delay the creation of the application after runtime.

This helps to enable the use of blueprint.
"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def create_app(config_name):
    """
    Initialize the application after runtime.

    This is done to enable the use of Blueprint.
    """

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    cors = CORS(app)
    cors.init_app(app)

    # Register the authentication blueprint in the application instance.
    from headline.auth import authentication as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # Register the main app's blueprint in the application instance.
    from headline.main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/api/v1')

    # handle default 404 exceptions with a custom response
    @app.errorhandler(404)
    def resource_not_found(error):
        response = jsonify(dict(status=404, error='Not found', message='The '
                                'requested URL was not found on the server. If'
                                ' you entered the URL manually please check '
                                'your spelling and try again'))
        response.status_code = 404
        return response

    # handle default 500 exceptions with a custom response
    @app.errorhandler(500)
    def internal_server_error(error):
        response = jsonify(dict(status=500, error='Internal server error',
                                message="It is not you. It is me. The server "
                                "encountered an internal error and was unable "
                                "to complete your request.  Either the server "
                                "is overloaded or there is an error in the "
                                "application"))
        response.status_code = 500
        return response

    return app
