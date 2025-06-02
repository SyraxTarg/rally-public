"""This file contains the custom errors extending httpexception"""
from fastapi import HTTPException

class CommentNotFound(HTTPException):
    """ the comment is not found"""


class EventNotFound(HTTPException):
    """ the event is not found"""


class EmailAlreadyRegisteredError(HTTPException):
    """ the user is already registered"""


class WeakPasswordError(HTTPException):
    """ the given password is weak"""


class UserNotFoundError(HTTPException):
    """ the user is not found"""


class InvalidCredentialsError(HTTPException):
    """ the credentials are wrong"""


class NoStripeAccountError(HTTPException):
    """ the user has no stripe account"""


class AddressNotFoundError(HTTPException):
    """ the address is not found"""


class UserBannedError(HTTPException):
    """ the user is banned"""


class TooManyAttemptsError(HTTPException):
    """ too many attempts at login are made"""


class InvalidTokenError(HTTPException):
    """ the token is invalid or missing"""


class BadRoleError(HTTPException):
    """ the given role is not the one required"""


class NoRefreshTokenError(HTTPException):
    """ the refresh token is not found"""


class BannedUserNotFoundError(HTTPException):
    """ the banned user is not found"""


class PictureNotFoundError(HTTPException):
    """ the picture is not found"""


class FailedLoginNotFoundError(HTTPException):
    """ the failed login is not found"""


class LikeNotFoundError(HTTPException):
    """ the like is not found"""


class SignaledCommentNotFound(HTTPException):
    """ the signaled comment is not found"""


class SignaledEventNotFound(HTTPException):
    """ the signaled event is not found"""


class SignaledUserNotFound(HTTPException):
    """ the signaled user is not found"""


class CheckoutError(HTTPException):
    """error during stripe checkout"""


class PaymentError(HTTPException):
    """error during the payment"""


class StripeAccountError(HTTPException):
    """error during the stripe account creation"""


class PaymentNotFound(HTTPException):
    """the payment is not found"""


class RegistrationNotFound(HTTPException):
    """the registration is not found"""


class ProfileNotFound(HTTPException):
    """the profile is not found"""


class ReasonNotFound(HTTPException):
    """the reason is not found"""


class ReasonAlreadyExists(HTTPException):
    """the reason already exists"""


class RegistrationNotPossible(HTTPException):
    """the registration is not possible"""


class RoleNotFound(HTTPException):
    """the role is not found"""


class TypeNotFound(HTTPException):
    """the type is not found"""


class InvalidEmailFormat(HTTPException):
    """the email format is invalid"""


class VerificationTokenExpiredError(HTTPException):
    """the verification token is expired"""


class UserNotVerifiedError(HTTPException):
    """the user is not verified"""


class DifferentPasswordsError(HTTPException):
    """the passwords are different from each other"""


class ErrorDuringEmailing(HTTPException):
    """there was an error during the sending of email"""


class InvalidContent(HTTPException):
    """the content contains invalid terms"""
