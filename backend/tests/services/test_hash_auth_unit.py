import pytest
from src.services.auth import Hash



@pytest.fixture
def hasher():
    return Hash()


def test_get_password_hash(hasher):
    """
    Test hashing a password.
    """
    password = "testpassword"
    hashed = hasher.get_password_hash(password)
    assert isinstance(hashed, str)
    assert hashed != password


def test_verify_password_success(hasher):
    """
    Test verifying correct password.
    """
    password = "securepassword"
    hashed = hasher.get_password_hash(password)
    assert hasher.verify_password(password, hashed)


def test_verify_password_failure(hasher):
    """
    Test verifying incorrect password.
    """
    password = "securepassword"
    hashed = hasher.get_password_hash(password)
    assert not hasher.verify_password("wrongpassword", hashed)
