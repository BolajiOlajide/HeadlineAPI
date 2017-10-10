"""Write test for models."""
import pytest

from headline.models import User


def test_password_setter():
    """
    Test password.

    Test the password is actually hashed and exists.
    """
    sample_user = User(username='test')
    sample_user.hash_password('cat')
    assert sample_user.password is not None


def test_password_can_be_decrypred():
    """
    Test the hashed password.

    Check if the hashed password is the same as the password when it has
    been decrypted.
    """
    user = User(username='test')
    user.hash_password('cat')
    assert user.verify_password('cat') is True


def test_password_hash_isnt_similar():
    """
    Test password hash.

    Test identical passwords return disimilar password hashes.
    """
    user = User(username='test')
    user.hash_password('cat')
    user2 = User(username='test2')
    user2.hash_password('cat')
    assert user.password != user2.password
