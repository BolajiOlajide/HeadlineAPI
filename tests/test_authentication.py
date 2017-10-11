"""
Test Authentication.

Test user authentication and token generation.
"""
import json
import unittest

from flask import url_for

try:
    from headline import db, create_app
    from headline.models import User
except:
    from headlineapi.headline import db, create_app
    from headline.models import User


class TestUserModel(unittest.TestCase):
    """
    The class encompasses all test cases related to the Application's model.

    I wrote simple tests to test the models.
    """

    def setUp(self):
        """
        Set up the application for testing.

        The method 'setUp' simply starts the application in test mode.
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.user = User(username='test_user', email='test@user.com')
        self.user.hash_password('test_password')
        self.user.save()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_encode_decode_auth_token(self):
        """
        Test the encoded token.

        This test whether the token returned is in bytes.
        """
        auth_token = self.user.generate_auth_token()
        assert isinstance(auth_token, bytes) is True
        assert User.verify_auth_token(auth_token).id == self.user.id

    def test_register(self):
        """
        Test register user.

        This tests user registration route.
        """
        with self.client:
            response = self.client.post(
                url_for('authentication.register_user'),
                data=json.dumps({
                    'username': 'proton',
                    'password': 'andela',
                    'email': 'proton@andela.com'
                }),
                content_type='application/json'
            )
        assert response.status_code == 201

    def test_register_with_null_values(self):
        """
        Test register user.

        This tests user registration route with null values
        sent to the API.
        """
        with self.client:
            response = self.client.post(
                url_for('authentication.register_user'),
                data=json.dumps({
                    'username': '',
                    'password': '',
                    'email': ''
                }),
                content_type='application/json'
            )
        assert response.status_code == 400

    def test_register_with_existing_username(self):
        """
        Test register user.

        This tests user registration route with already existing username
        """
        with self.client:
            response = self.client.post(
                url_for('authentication.register_user'),
                data=json.dumps({
                    'username': 'test_user',
                    'password': 'andela',
                    'email': 'proton@andela.com'
                }),
                content_type='application/json'
            )
        assert response.status_code == 400

    def test_register_with_invalid_username(self):
        """
        Test register user.

        This tests user registration route with invalid email address
        """
        with self.client:
            response = self.client.post(
                url_for('authentication.register_user'),
                data=json.dumps({
                    'username': 'proton_test',
                    'password': 'andela',
                    'email': 'protonandela.com'
                }),
                content_type='application/json'
            )
        assert response.status_code == 400

    def test_login(self):
        """
        Test the login route.

        This test checks if a user is successful logged in and the status
        code returned.
        """
        with self.client:
            response = self.client.post(
                url_for('authentication.login'),
                data=json.dumps(
                    {'username': 'test_user', 'password': 'test_password'}),
                content_type='application/json'
            )
        assert response.status_code == 200

    def test_login_without_json(self):
        """
        Test login without json.
        Test that when a user tries to logging without sending a JSON object,
        the API flags it as an error.
        """
        with self.client:
            response = self.client.post(
                url_for('authentication.login'),
                data={'username': 'test_user', 'password': 'test_password'},
            )
        assert response.status_code == 400

    def test_login_with_null_password(self):
        """
        Test if a user can supply a null password.
        This test checks if the user supplies a null string as username or
        password.
        """
        with self.client:
            response = self.client.post(
                url_for('authentication.login'),
                data=json.dumps({'username': 'test_user', 'password': ''}),
                content_type='application/json'
            )
        assert response.status_code == 400

    def test_login_with_wrong_credentials(self):
        """
        Test user signing in with wrong credentials.
        When a user logs in with wrong credentials, the API should return a
        400 error.
        """
        with self.client:
            response = self.client.post(
                url_for('authentication.login'),
                data=json.dumps(
                    {'username': 'test_user', 'password': 'something_else'}
                ),
                content_type='application/json'
            )
        assert response.status_code == 401
