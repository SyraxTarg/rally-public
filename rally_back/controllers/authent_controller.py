"""
This file contains the controller related to authentication
"""
from datetime import datetime
from fastapi import Depends, Cookie, Request, status, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models.user_model import User
from database.db import get_db
from schemas.request_schemas.register_schema import RegisterSchema
from services import action_log_service, authent_service, role_service, user_service
from schemas.response_schemas.user_schema_response import UserResponse
from schemas.response_schemas.role_schema_response import RoleSchemaResponse
from enums.log_level import LogLevelEnum
from enums.action import ActionEnum
from schemas.request_schemas.reset_password_schema import ResetPasswordSchema
from schemas.request_schemas.user_schema import UserAuth
from errors import (
    EmailAlreadyRegisteredError,
    WeakPasswordError,
    UserNotFoundError,
    InvalidCredentialsError
)


async def register_user(
    user: RegisterSchema,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
        Register a new user if the email is not already in use and the password is strong.

        Args:
            user (RegisterSchema): The registration data including email, password, phone number, first name, and last name.
            db (Session, optional): SQLAlchemy session injected via FastAPI dependency.

        Returns:
            UserResponse: The registered user's public information.

        Raises:
            EmailAlreadyRegisteredError: If the email is already associated with an existing user.
            WeakPasswordError: If the provided password does not meet the strength requirements.
    """

    if user_service.get_user_by_email(db, user.email):
        raise EmailAlreadyRegisteredError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email already registered"
        )

    if not authent_service.is_password_strong(user.password):
        raise WeakPasswordError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long, include an uppercase letter and a number"
        )

    new_user = authent_service.register_user(db, user.email, user.password, user.phone_number, user.first_name, user.last_name, user.photo)
    role = role_service.get_role_by_id(db, new_user.role_id)
    action_log_service.create_action_log(
        db,
        new_user.id,
        LogLevelEnum.INFO,
        ActionEnum.REGISTRATION,
        f"User {role.role} {new_user.email} registered at {new_user.created_at}"
    )
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        phone_number=new_user.phone_number,
        is_planner=new_user.is_planner,
        role=RoleSchemaResponse(
            id=role.id,
            role=role.role
        ),
        account_id=new_user.account_id
    )


async def register_admin(
    user: RegisterSchema,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Registers a new admin user in the system.

    Args:
        user (RegisterSchema): Data required to register the admin.
        db (Session): Database session dependency.

    Raises:
        EmailAlreadyRegisteredError: If the email is already used by another user.
        WeakPasswordError: If the password doesn't meet strength requirements.

    Returns:
        UserResponse: The created admin user's response data.
    """
    if user_service.get_user_by_email(db, user.email):
        raise EmailAlreadyRegisteredError(status_code=400, detail="email already registered")

    if not authent_service.is_password_strong(user.password):
        raise WeakPasswordError(status_code=400, detail="Password must be at least 8 characters long, include an uppercase letter and a number")

    new_user = authent_service.register_admin(db, user.email, user.password, user.phone_number, user.first_name, user.last_name, user.photo)
    role = role_service.get_role_by_id(db, new_user.role_id)
    action_log_service.create_action_log(
        db,
        new_user.id,
        LogLevelEnum.INFO,
        ActionEnum.REGISTRATION,
        f"User {role.role} {new_user.email} registered at {new_user.created_at}"
    )
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        phone_number=new_user.phone_number,
        is_planner=new_user.is_planner,
        role=RoleSchemaResponse(
            id=role.id,
            role=role.role
        ),
        account_id=new_user.account_id
    )


async def register_super_admin(
    user: RegisterSchema,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Registers a new super admin user in the system.

    Args:
        user (RegisterSchema): Data required to register the super admin.
        db (Session): Database session dependency.

    Raises:
        EmailAlreadyRegisteredError: If the email is already registered.
        WeakPasswordError: If the provided password does not meet security criteria.

    Returns:
        UserResponse: The registered super admin's response data.
    """
    if user_service.get_user_by_email(db, user.email):
        raise EmailAlreadyRegisteredError(status_code=400, detail="email already registered")

    if not authent_service.is_password_strong(user.password):
        raise WeakPasswordError(status_code=400, detail="Password must be at least 8 characters long, include an uppercase letter and a number")

    new_user = authent_service.register_super_admin(db, user.email, user.password, user.phone_number, user.first_name, user.last_name, user.photo)
    role = role_service.get_role_by_id(db, new_user.role_id)
    action_log_service.create_action_log(
        db,
        new_user.id,
        LogLevelEnum.INFO,
        ActionEnum.REGISTRATION,
        f"User {role.role} {new_user.email} registered at {new_user.created_at}"
    )
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        phone_number=new_user.phone_number,
        is_planner=new_user.is_planner,
        role=RoleSchemaResponse(
            id=role.id,
            role=role.role
        ),
        account_id=new_user.account_id
    )


async def refresh_token(refresh_token: str = Cookie(None), db: Session = Depends(get_db))->JSONResponse:
    """
    Refreshes the authentication token using the provided refresh token.

    Args:
        refresh_token (str, optional): The refresh token passed via a cookie. Defaults to None.
        db (Session): The database session dependency used for token validation.

    Returns:
        JSONResponse: A JSON response containing the new authentication token.

    """
    return await authent_service.refresh_token(db, refresh_token)


def verify_jwt(
    access_token: str = Cookie(None),
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Retrieves the currently connected user based on the provided access token.

    Args:
        access_token (str, optional): The access token passed via a cookie to identify the user. Defaults to None.
        db (Session): The database session dependency used for user retrieval.

    Returns:
        User: The user object corresponding to the provided access token.

    Raises:
        UserNotFoundError: If no user is found associated with the provided access token.
    """
    print(authorization, access_token)
    user = authent_service.get_connected_user(db, authorization, access_token)
    print("USER ", user)
    if not user:
        print("pas trouve")
        raise UserNotFoundError(status_code=404, detail="L'utilisateur n'a pas été trouvé")

    role = role_service.get_role_by_id(db, user.role_id)
    print("ROLE ", role)
    user_schema = UserResponse(
        id=user.id,
        email=user.email,
        phone_number=user.phone_number,
        is_planner=user.is_planner,
        account_id=user.account_id,
        role=RoleSchemaResponse(
            id=role.id,
            role=role.role
        )
    )
    print("SCHEMA ", user_schema)
    return user_schema


def get_connected_user(
    access_token: str = Cookie(None),
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Retrieves the currently connected user based on the provided access token.

    Args:
        access_token (str, optional): The access token passed via a cookie to identify the user. Defaults to None.
        db (Session): The database session dependency used for user retrieval.

    Returns:
        User: The user object corresponding to the provided access token.

    Raises:
        UserNotFoundError: If no user is found associated with the provided access token.
    """
    print(authorization, access_token)
    user = authent_service.get_connected_user(db, authorization, access_token)
    if not user:
        raise UserNotFoundError(status_code=404, detail="L'utilisateur n'a pas été trouvé")
    return user

def get_current_user(
    access_token: str = Cookie(None),
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Fetches the current user based on the provided access token.

    Args:
        access_token (str, optional): The access token passed via a cookie to authenticate the user. Defaults to None.
        db (Session): The database session dependency used for fetching the user from the database.

    Returns:
        User: The user object associated with the provided access token.

    Raises:
        UserNotFoundError: If no user is found with the given access token.
    """
    user = authent_service.get_current_user(db, authorization, access_token)
    if not user:
        raise UserNotFoundError(status_code=404, detail="L'utilisateur n'a pas été trouvé")
    return user


def get_current_admin(
    access_token: str = Cookie(None),
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Fetches the current admin user based on the provided access token.

    Args:
        access_token (str, optional): The access token passed via a cookie to authenticate the admin user. Defaults to None.
        db (Session): The database session dependency used for fetching the admin user from the database.

    Returns:
        User: The admin user object associated with the provided access token.

    Raises:
        UserNotFoundError: If no admin user is found with the given access token.
    """
    user = authent_service.get_current_admin(db, authorization, access_token)
    if not user:
        raise UserNotFoundError(status_code=404, detail="L'utilisateur n'a pas été trouvé")
    return user

def get_current_admin_or_super_admin(
    access_token: str = Cookie(None),
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Fetches the current admin or super admin user based on the provided access token.

    Args:
        access_token (str, optional): The access token passed via a cookie to authenticate the user. Defaults to None.
        db (Session): The database session dependency used for fetching the user from the database.

    Returns:
        User: The admin or super admin user object associated with the provided access token.

    Raises:
        UserNotFoundError: If no admin or super admin user is found with the given access token.
    """
    user = authent_service.get_super_admin_or_admin(db, authorization, access_token)
    if not user:
        raise UserNotFoundError(status_code=404, detail="L'utilisateur n'a pas été trouvé")
    return user

def get_current_super_admin(
    access_token: str = Cookie(None),
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Fetches the current super admin user based on the provided access token.

    Args:
        access_token (str, optional): The access token passed via a cookie to authenticate the user. Defaults to None.
        db (Session): The database session dependency used for fetching the user from the database.

    Returns:
        User: The super admin user object associated with the provided access token.

    Raises:
        UserNotFoundError: If no super admin user is found with the given access token.
    """
    user = authent_service.get_current_super_admin(db, authorization, access_token)
    if not user:
        raise UserNotFoundError(status_code=404, detail="L'utilisateur n'a pas été trouvé")
    return user

async def login(request: Request, user_login: UserAuth, db: Session)->JSONResponse:
    """
    Handles user login by verifying the provided credentials and generating an access token.

    Args:
        request (Request): The HTTP request object containing client information (e.g., IP address).
        user_login (UserAuth): The user login credentials, including email and password.
        db (Session): The database session used to interact with the user data.

    Returns:
        JSONResponse: A response containing the generated access token for the authenticated user.

    Raises:
        InvalidCredentialsError: If the user is not found or the provided credentials are incorrect.
    """
    user = user_service.get_user_by_email(db, user_login.email)

    if not user:
        raise InvalidCredentialsError(status_code=401, detail="Email ou mot de passe incorrect")

    response = await authent_service.login_for_access_token(request, user_login, db)

    action_log_service.create_action_log(
        db=db,
        user_id=user.id,
        log_type=LogLevelEnum.INFO,
        action_type=ActionEnum.LOGIN,
        description=f"L'utilisateur {user.email} s'est connecté depuis {request.client.host}"
    )

    return response

async def logout(db: Session, current_user_id: int)->JSONResponse:
    """
    Logs out the currently authenticated user and generates a logout action log.

    Args:
        db (Session): The database session used to interact with the user data.
        current_user_id (int): The ID of the currently authenticated user.

    Returns:
        JSONResponse: A response indicating the successful logout of the user.

    Raises:
        UserNotFoundError: If the user with the given ID is not found in the database.
    """
    user = user_service.get_user(db, current_user_id)
    if not user:
        raise UserNotFoundError(status_code=404, detail="L'utilisateur n'a pas été trouvé")

    logout = await authent_service.logout()

    action_log_service.create_action_log(
        db=db,
        user_id=user.id,
        log_type=LogLevelEnum.INFO,
        action_type=ActionEnum.LOGOUT,
        description=f"L'utilisateur {user.email} s'est déconnecté à {datetime.now()}"
    )

    return logout

def verify_register_token(db: Session, user_email: str, token: int)->bool:
    """
    Verifies the registration token for a user.

    Args:
        db (Session): The database session used to interact with the user data.
        user_email (str): The email address of the user to verify the registration token for.
        token (int): The registration token to be verified.

    Returns:
        bool: True if the registration token is valid, otherwise False.

    Raises:
        UserNotFoundError: If no user is found with the provided email address.
    """
    user = user_service.get_user_by_email(db, user_email)
    print(user)
    if not user:
        raise UserNotFoundError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return authent_service.verify_register_token(db, user, token)


def send_token_by_email(db: Session, user_email: str)->None:
    """
    Sends a verification token to the user's email for email verification.

    Args:
        db (Session): The database session used to interact with the user data.
        user_email (str): The email address of the user to send the verification token to.

    Returns:
        None

    Raises:
        UserNotFoundError: If no user is found with the provided email address.
    """
    user = user_service.get_user_by_email(db, user_email)
    if not user:
        raise UserNotFoundError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return authent_service.send_mail_for_email_verif(db, user)

def generate_link_reset_password(db: Session, user_email: str)->None:
    """
    Generates and sends a password reset link to the user's email.

    Args:
        db (Session): The database session used to interact with the user data.
        user_email (str): The email address of the user to send the password reset link to.

    Returns:
        None

    Raises:
        UserNotFoundError: If no user is found with the provided email address.
    """
    user = user_service.get_user_by_email(db, user_email)
    if not user:
        raise UserNotFoundError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return authent_service.send_mail_for_password_reset(db, user)

def reset_password(db: Session, reset_password_schema: ResetPasswordSchema)->bool:
    """
    Resets the user's password using the provided reset token and new password.

    Args:
        db (Session): The database session used to interact with the user data.
        reset_password_schema (ResetPasswordSchema): The schema containing the reset token, new password, and confirm password.

    Returns:
        bool: True if the password reset was successful, otherwise False.

    Raises:
        WeakPasswordError: If the new password doesn't meet the required strength (at least 8 characters, including an uppercase letter and a number).
    """
    if not authent_service.is_password_strong(reset_password_schema.new_password):
        raise WeakPasswordError(status_code=400, detail="Password must be at least 8 characters long, include an uppercase letter and a number")

    return authent_service.reset_pwd(db,
                                     reset_password_schema.token,
                                     reset_password_schema.new_password,
                                     reset_password_schema.confirm_password
                                    )
