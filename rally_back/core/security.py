"""
This file contains the security related functions
"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str)->str:
    """
    Hashes the provided password using a secure hashing algorithm.

    This function takes a plain text password and hashes it using a cryptographic hashing algorithm
    defined by the `pwd_context` (such as bcrypt, argon2, etc.). The resulting hash can then be stored
    securely in the database.

    Args:
        password (str): The plain text password that needs to be hashed.

    Returns:
        str: The hashed password, which is a string that can be stored securely in a database.
    """
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password)->bool:
    """
    Verifies if the provided plain password matches the hashed password.

    This function takes a plain text password and a hashed password, and compares the two to
    check if they match. The comparison is done securely using the `pwd_context.verify()` method.

    Args:
        plain_password (str): The plain text password to be verified.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the plain password matches the hashed password, otherwise False.
    """
    return pwd_context.verify(plain_password, hashed_password)
