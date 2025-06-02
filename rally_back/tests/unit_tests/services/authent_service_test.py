from unittest.mock import patch, MagicMock
import pytest
import jwt
import os
import json
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta

from services import authent_service
from schemas.request_schemas.user_schema import UserAuth
from errors import (
    UserBannedError,
    TooManyAttemptsError,
    InvalidCredentialsError,
    InvalidTokenError,
    UserNotFoundError,
    BadRoleError,
    NoRefreshTokenError,
    UserNotVerifiedError
)



@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)

@pytest.fixture
def mock_request():
    return MagicMock(spec=Request)

@pytest.fixture
def mock_create_user(mocker):
    return mocker.patch("services.user_service.create_user")

@pytest.fixture
def mock_create_admin(mocker):
    return mocker.patch("services.user_service.create_admin")

@pytest.fixture
def mock_create_super_admin(mocker):
    return mocker.patch("services.user_service.create_super_admin")

@pytest.fixture
def mock_get_user_by_email(mocker):
    return mocker.patch("services.user_service.get_user_by_email")

@pytest.fixture
def mock_get_failed_login(mocker):
    return mocker.patch("services.failed_login_service.get_failed_login")

@pytest.fixture
def mock_create_failed_login(mocker):
    return mocker.patch("services.failed_login_service.create_failed_login")

@pytest.fixture
def mock_update_failed_login(mocker):
    return mocker.patch("services.failed_login_service.update_failed_login")

@pytest.fixture
def mock_delete_failed_login(mocker):
    return mocker.patch("services.failed_login_service.delete_failed_login")

@pytest.fixture
def mock_create_access_token(mocker):
    return mocker.patch("services.authent_service.create_access_token")

@pytest.fixture
def mock_get_role_by_id(mocker):
    return mocker.patch("services.role_service.get_role_by_id")

@pytest.fixture
def mock_create_refresh_token(mocker):
    return mocker.patch("services.authent_service.create_refresh_token")

@pytest.fixture
def mock_get_banned_user_by_email(mocker):
    return mocker.patch("services.banned_user_service.get_banned_user_by_email")

@pytest.fixture
def mock_role():
    role = MagicMock()
    return role

@pytest.fixture
def mock_user():
    user = MagicMock()
    user.email = "john.doe@mail.com"
    user.password = "password"
    user.phone_number = "0632144087"
    user.is_planner = False
    user.role.role = "ROLE_USER"
    return user


@pytest.fixture
def mock_admin():
    admin = MagicMock()
    admin.email = "john.doe@mail.com"
    admin.password = "password"
    admin.phone_number = "0632144087"
    admin.is_planner = False
    admin.role.role = "ROLE_ADMIN"
    return admin

@pytest.fixture
def mock_super_admin():
    super_admin = MagicMock()
    super_admin.email = "john.doe@mail.com"
    super_admin.password = "password"
    super_admin.phone_number = "0632144087"
    super_admin.is_planner = False
    super_admin.role.role = "ROLE_SUPER_ADMIN"
    return super_admin


@pytest.fixture
def mock_failed_login():
    failed_login = MagicMock()
    failed_login.last_attempt = datetime.now()
    return failed_login


def test_register_user(mock_create_user, mock_db_session, mock_user, mock_get_banned_user_by_email):
    # Arrange
    mock_create_user.return_value = mock_user
    mock_get_banned_user_by_email.return_value = None

    # Act
    result = authent_service.register_user(
        db=mock_db_session,
        email="john.doe@mail.com",
        password="password",
        phone_number="0000000000",
        first_name="John",
        last_name="Doe",
        photo="default.jpg"
    )

    # Assert
    assert result.email == mock_user.email
    assert result.password == mock_user.password
    assert result.phone_number == mock_user.phone_number
    assert result.is_planner == False
    assert result.role.role == "ROLE_USER"
    mock_create_user.assert_called_once()
    mock_get_banned_user_by_email.assert_called_once()


def test_register_user_banned(mock_create_user, mock_db_session, mock_user, mock_get_banned_user_by_email):
    # Arrange
    mock_get_banned_user_by_email.return_value = mock_user

    # Act
    with pytest.raises(UserBannedError) as result:
        authent_service.register_user(
            db=mock_db_session,
            email="john.doe@mail.com",
            password="password",
            phone_number="0000000000",
            first_name="John",
            last_name="Doe",
            photo="default.jpg"
        )

    # Assert
    assert str(result.value) == "401: Cet utilisateur a été banni. Création du compte impossible."
    mock_get_banned_user_by_email.assert_called_once()
    mock_create_user.assert_not_called()


def test_register_admin(mock_create_admin, mock_db_session, mock_admin, mock_get_banned_user_by_email):
    # Arrange
    mock_create_admin.return_value = mock_admin
    mock_get_banned_user_by_email.return_value = None

    # Act
    result = authent_service.register_admin(
        db=mock_db_session,
        email="john.doe@mail.com",
        password="password",
        phone_number="0000000000",
        first_name="John",
        last_name="Doe",
        photo="default.jpg"
    )

    # Assert
    assert result.email == mock_admin.email
    assert result.password == mock_admin.password
    assert result.phone_number == mock_admin.phone_number
    assert result.is_planner == False
    assert result.role.role == "ROLE_ADMIN"
    mock_create_admin.assert_called_once()
    mock_get_banned_user_by_email.assert_called_once()

def test_register_admin_banned(mock_create_admin, mock_db_session, mock_admin, mock_get_banned_user_by_email):
    # Arrange
    mock_get_banned_user_by_email.return_value = mock_admin

    # Act
    with pytest.raises(UserBannedError) as result:
        authent_service.register_admin(
            db=mock_db_session,
            email="john.doe@mail.com",
            password="password",
            phone_number="0000000000",
            first_name="John",
            last_name="Doe",
            photo="default.jpg"
        )

    # Assert
    assert str(result.value) == "401: Cet utilisateur a été banni. Création du compte impossible."
    mock_get_banned_user_by_email.assert_called_once()
    mock_create_admin.assert_not_called()


def test_register_super_admin(mock_create_super_admin, mock_db_session, mock_super_admin, mock_get_banned_user_by_email):
    # Arrange
    mock_create_super_admin.return_value = mock_super_admin
    mock_get_banned_user_by_email.return_value = None

    # Act
    result = authent_service.register_super_admin(
        db=mock_db_session,
        email="john.doe@mail.com",
        password="password",
        phone_number="0000000000",
        first_name="John",
        last_name="Doe",
        photo="default.jpg"
    )

    # Assert
    assert result.email == mock_super_admin.email
    assert result.password == mock_super_admin.password
    assert result.phone_number == mock_super_admin.phone_number
    assert result.is_planner == False
    assert result.role.role == "ROLE_SUPER_ADMIN"
    mock_create_super_admin.assert_called_once()
    mock_get_banned_user_by_email.assert_called_once()


def test_register_super_admin_banned(mock_create_super_admin, mock_db_session, mock_super_admin, mock_get_banned_user_by_email):
    # Arrange
    mock_get_banned_user_by_email.return_value = mock_super_admin

    # Act
    with pytest.raises(UserBannedError) as result:
        authent_service.register_super_admin(
            db=mock_db_session,
            email="john.doe@mail.com",
            password="password",
            phone_number="0000000000",
            first_name="John",
            last_name="Doe",
            photo="default.jpg"
        )

    # Assert
    assert str(result.value) == "401: Cet utilisateur a été banni. Création du compte impossible."
    mock_get_banned_user_by_email.assert_called_once()
    mock_create_super_admin.assert_not_called()


@patch.dict(os.environ, {"SECRET_KEY": "mysecret", "ALGORITHM": "HS256"})
def test_create_access_token():
    # Arrange
    data = {"sub": "user_id_123"}
    expires = timedelta(minutes=5)

    # Act
    token = authent_service.create_access_token(data, expires)
    decoded = jwt.decode(token, "mysecret", algorithms=["HS256"])

    # Assert
    assert isinstance(token, str)
    assert decoded["sub"] == "user_id_123"
    assert "exp" in decoded
    assert datetime.fromtimestamp(decoded["exp"]) > datetime.now()


def test_is_password_strong():
    assert authent_service.is_password_strong("Password.123") == True
    assert authent_service.is_password_strong("Password123") == True
    assert authent_service.is_password_strong("Password") == False
    assert authent_service.is_password_strong("Passwordzertyhjurez") == False
    assert authent_service.is_password_strong("password.123") == False
    assert authent_service.is_password_strong("1234567892") == False


@pytest.mark.asyncio
async def test_login_for_access_token(
    mock_request,
    mock_get_failed_login,
    mock_get_user_by_email,
    mock_user,
    mock_db_session
):
    # Arrange
    user_auth = UserAuth(email="john.doe@mail.com", password="password")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash("password")
    mock_user.password = hashed_password
    mock_user.is_verified = True
    mock_user.id = 1
    mock_get_user_by_email.return_value = mock_user
    mock_get_failed_login.return_value = None

    # Act
    result = await authent_service.login_for_access_token(mock_request, user_auth, mock_db_session)

    # Assert
    assert isinstance(result, JSONResponse)
    assert result.status_code == 200
    body = json.loads(result.body)
    assert body["msg"] == "Login successful"
    assert "access_token" in body
    assert "refresh_token" in body
    assert body["user_id"] == 1
    mock_get_user_by_email.assert_called_once()
    mock_get_failed_login.assert_called_once()



@pytest.mark.asyncio
async def test_login_for_access_token_user_not_verified(
    mock_request,
    mock_get_failed_login,
    mock_get_user_by_email,
    mock_user,
    mock_db_session
):
    user_auth = UserAuth(email="john.doe@mail.com", password="password")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash("password")
    mock_user.password = hashed_password
    mock_user.is_verified = False
    mock_get_user_by_email.return_value = mock_user
    mock_get_failed_login.return_value = None

    # Act
    with pytest.raises(UserNotVerifiedError) as result:
        await authent_service.login_for_access_token(mock_request, user_auth, mock_db_session)

    # Assert
    assert str(result.value) == "403: User is not verified"
    mock_get_user_by_email.assert_called_once()
    mock_get_failed_login.assert_called_once()


@pytest.mark.asyncio
async def test_login_for_access_token_failed_to_many_times(
    mock_request,
    mock_get_failed_login,
    mock_db_session,
    mock_failed_login
):
    # Arrange
    user_auth = UserAuth(email="john.doe@mail.com", password="password")
    mock_failed_login.attempts = 6
    mock_get_failed_login.return_value = mock_failed_login

    # Act
    with pytest.raises(TooManyAttemptsError) as result:
        await authent_service.login_for_access_token(mock_request, user_auth, mock_db_session)

    # Assert
    assert str(result.value) == "429: Too many login attempts. Try again later."
    mock_get_failed_login.assert_called_once()


@pytest.mark.asyncio
async def test_login_for_access_token_invalid_credentials_no_failed_login(
    mock_request,
    mock_get_failed_login,
    mock_get_user_by_email,
    mock_db_session,
    mock_create_failed_login,
    mock_failed_login
):
    # Arrange
    user_auth = UserAuth(email="john.doe@mail.com", password="password")
    mock_get_user_by_email.return_value = None
    mock_get_failed_login.return_value = None
    mock_create_failed_login.return_value = mock_failed_login

    # Act
    with pytest.raises(InvalidCredentialsError) as result:
        await authent_service.login_for_access_token(mock_request, user_auth, mock_db_session)

    # Assert
    assert str(result.value) == "401: Invalid credentials"
    mock_get_user_by_email.assert_called_once()
    mock_get_failed_login.assert_called_once()
    mock_create_failed_login.assert_called_once()


@pytest.mark.asyncio
async def test_login_for_access_token_invalid_credentials(
    mock_request,
    mock_get_failed_login,
    mock_get_user_by_email,
    mock_db_session,
    mock_update_failed_login,
    mock_failed_login
):
    # Arrange
    user_auth = UserAuth(email="john.doe@mail.com", password="password")
    mock_get_user_by_email.return_value = None
    mock_failed_login.attempts = 2
    mock_get_failed_login.return_value = mock_failed_login
    mock_update_failed_login.return_value = mock_failed_login

    # Act
    with pytest.raises(InvalidCredentialsError) as result:
        await authent_service.login_for_access_token(mock_request, user_auth, mock_db_session)

    # Assert
    assert str(result.value) == "401: Invalid credentials"
    mock_get_user_by_email.assert_called_once()
    mock_get_failed_login.assert_called_once()
    mock_update_failed_login.assert_called_once()


@pytest.mark.asyncio
async def test_login_for_access_token_delete_failed_login(
    mock_request,
    mock_get_failed_login,
    mock_get_user_by_email,
    mock_user,
    mock_db_session,
    mock_failed_login,
    mock_delete_failed_login
):
    # Arrange
    user_auth = UserAuth(email="john.doe@mail.com", password="password")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash("password")
    mock_user.password = hashed_password
    mock_user.is_verified = True
    mock_user.id = 1
    mock_get_user_by_email.return_value = mock_user
    mock_failed_login.attempts = 4
    mock_get_failed_login.return_value = mock_failed_login
    mock_delete_failed_login.return_value = None

    # Act
    result = await authent_service.login_for_access_token(mock_request, user_auth, mock_db_session)

    # Assert
    assert isinstance(result, JSONResponse)
    assert result.status_code == 200

    body = json.loads(result.body.decode())
    assert body["msg"] == "Login successful"
    assert "access_token" in body
    assert "refresh_token" in body
    assert "user_id" in body

    mock_delete_failed_login.assert_called_once()
    mock_get_user_by_email.assert_called_once()
    mock_get_failed_login.assert_called_once()



def test_get_current_user_no_token(mock_db_session):
    # Act / Arrange
    with pytest.raises(InvalidTokenError) as result:
        authent_service.get_current_user(mock_db_session, None)

    # Assert
    assert str(result.value) == "401: Invalid Token"


@patch.dict(os.environ, {"SECRET_KEY": "mysecret", "ALGORITHM": "HS256"})
def test_get_current_user_with_valid_header_token(
    mock_db_session,
    mock_user,
    mock_get_user_by_email,
    mock_get_role_by_id,
    mock_role
):
    # Arrange
    mock_role.role = "ROLE_USER"
    mock_user.role = mock_role
    access_token = "Mon_token_valide"
    token_header = f"Bearer {access_token}"
    mock_get_user_by_email.return_value = mock_user
    mock_get_role_by_id.return_value = mock_role

    with patch("services.authent_service.jwt.decode", return_value={"sub": "admin@example.com"}):
        # Act
        result = authent_service.get_current_user(mock_db_session, token_header, access_token)

    # Assert
    assert result.email == mock_user.email
    assert result.password == mock_user.password
    assert result.is_planner == mock_user.is_planner
    assert result.phone_number == mock_user.phone_number
    assert result.role.role == mock_user.role.role
    mock_get_user_by_email.assert_called_once()
    mock_get_role_by_id.assert_called_once()



@patch.dict(os.environ, {"SECRET_KEY": "mysecret", "ALGORITHM": "HS256"})
def test_get_current_user_not_role_user(
    mock_db_session,
    mock_user,
    mock_get_user_by_email,
    mock_get_role_by_id,
    mock_role
):
    # Arrange
    mock_role.role = "ROLE_INVALIDE"
    access_token = "Mon_token_valide"
    token_header = "Bearer Mon_token_valide"
    mock_get_user_by_email.return_value = mock_user
    mock_get_role_by_id.return_value = mock_role

    # Act
    with pytest.raises(BadRoleError) as result:
        with patch("services.authent_service.jwt.decode", return_value={"sub": "admin@example.com"}):
            authent_service.get_current_user(mock_db_session, token_header, access_token)

    # Assert
    assert str(result.value) == "403: You do not have the rights to access this resource"
    mock_get_user_by_email.assert_called_once()
    mock_get_role_by_id.assert_called_once()



def test_get_current_user_email_not_in_token(mock_db_session):
    # Arrange
    access_token = "Mon_token_invalide"
    token_header = "Bearer Mon_token_invalide"

    # Act
    with patch("services.authent_service.jwt.decode", return_value={"sub": None}):
        with pytest.raises(InvalidTokenError) as result:
            authent_service.get_current_user(mock_db_session, token_header, access_token)

    # Assert
    assert str(result.value) == "401: Invalid Token"


def test_get_current_user_not_found(mock_db_session, mock_get_user_by_email):
    # Arrange
    access_token = "Mon_token_invalidevalide"
    token_header = " Bearer Mon_token_header"
    mock_get_user_by_email.return_value = None

    # Act
    with patch("services.authent_service.jwt.decode", return_value={"sub": "admin@example.com"}):
        with pytest.raises(UserNotFoundError) as result:
            authent_service.get_current_user(mock_db_session, token_header, access_token)

    # Assert
    assert str(result.value) == "404: User not found"


@patch.dict(os.environ, {"SECRET_KEY": "mysecret", "ALGORITHM": "HS256"})
def test_get_current_admin_not_role_admin(mock_db_session, mock_admin, mock_get_user_by_email, mock_get_role_by_id, mock_role):
    # Arrange
    mock_role.role = "ROLE_INVALIDE"
    access_token = "Mon_token_valide"
    token_header = "bearer Mon_token_header"
    mock_get_user_by_email.return_value = mock_admin
    mock_get_role_by_id.return_value = mock_role

    # Act
    with pytest.raises(BadRoleError) as result:
        with patch("services.authent_service.jwt.decode", return_value={"sub": "admin@example.com"}):
            authent_service.get_current_admin(mock_db_session, token_header, access_token)

    # Assert
    assert str(result.value) == "403: You do not have the rights to access this ressource"
    mock_get_user_by_email.assert_called_once()
    mock_get_role_by_id.assert_called_once()


@patch.dict(os.environ, {"SECRET_KEY": "mysecret", "ALGORITHM": "HS256"})
def test_get_current_admin(mock_db_session, mock_admin, mock_get_user_by_email, mock_get_role_by_id, mock_role):
    # Arrange
    mock_role.role = "ROLE_ADMIN"
    access_token = "Mon_token_valide"
    token_header = "bearer Mon_token_header"
    mock_get_user_by_email.return_value = mock_admin
    mock_get_role_by_id.return_value = mock_role

    # Act
    with patch("services.authent_service.jwt.decode", return_value={"sub": "admin@example.com"}):
        result = authent_service.get_current_admin(mock_db_session, token_header, access_token)

    # Assert
    assert result.email == mock_admin.email
    assert result.password == mock_admin.password
    assert result.is_planner == mock_admin.is_planner
    assert result.phone_number == mock_admin.phone_number
    assert result.role.role == mock_admin.role.role
    mock_get_user_by_email.assert_called_once()
    mock_get_role_by_id.assert_called_once()


def test_get_current_admin_no_token(mock_db_session):
    # Act / Arrange
    token_header = "bearer Mon_token_header"
    with pytest.raises(InvalidTokenError) as result:
        authent_service.get_current_admin(mock_db_session, token_header, None)

    # Assert
    assert str(result.value) == "401: Invalid Token"


def test_get_current_admin_email_not_in_token(mock_db_session):
    # Arrange
    access_token = "Mon_token_invalidevalide"
    token_header = "bearer Mon_token_header"

    # Act
    with patch("services.authent_service.jwt.decode", return_value={"sub": None}):
        with pytest.raises(InvalidTokenError) as result:
            authent_service.get_current_admin(mock_db_session, token_header, access_token)

    # Assert
    assert str(result.value) == "401: Invalid Token"


def test_get_current_admin_not_found(mock_db_session, mock_get_user_by_email):
    # Arrange
    access_token = "Mon_token_invalidevalide"
    token_header = "bearer Mon_token_header"
    mock_get_user_by_email.return_value = None

    # Act
    with patch("services.authent_service.jwt.decode", return_value={"sub": "admin@example.com"}):
        with pytest.raises(UserNotFoundError) as result:
            authent_service.get_current_admin(mock_db_session, token_header, access_token)

    # Assert
    assert str(result.value) == "404: User not found"

def test_get_current_super_admin_no_token(mock_db_session):
    # Act / Arrange
    token_header = "bearer Mon_token_header"
    with pytest.raises(InvalidTokenError) as result:
        authent_service.get_current_super_admin(mock_db_session, token_header, None)

    # Assert
    assert str(result.value) == "401: Invalid Token"


@patch.dict(os.environ, {"SECRET_KEY": "mysecret", "ALGORITHM": "HS256"})
def test_get_current_super_admin(mock_db_session, mock_super_admin, mock_get_user_by_email, mock_role, mock_get_role_by_id):
    # Arrange
    mock_role.role = "ROLE_SUPER_ADMIN"
    access_token = "Mon_token_valide"
    token_header = "bearer Mon_token_header"
    mock_get_user_by_email.return_value = mock_super_admin
    mock_get_role_by_id.return_value = mock_role

    # Act
    with patch("services.authent_service.jwt.decode", return_value={"sub": "admin@example.com"}):
        result = authent_service.get_current_super_admin(mock_db_session, token_header, access_token)

    # Assert
    assert result.email == mock_super_admin.email
    assert result.password == mock_super_admin.password
    assert result.is_planner == mock_super_admin.is_planner
    assert result.phone_number == mock_super_admin.phone_number
    assert result.role.role == mock_super_admin.role.role
    mock_get_user_by_email.assert_called_once()
    mock_get_role_by_id.assert_called_once()


@patch.dict(os.environ, {"SECRET_KEY": "mysecret", "ALGORITHM": "HS256"})
def test_get_current_super_admin_no_role_super_admin(mock_db_session, mock_super_admin, mock_get_user_by_email, mock_role, mock_get_role_by_id):
    # Arrange
    mock_role.role = "ROLE_INVALIDE"
    access_token = "Mon_token_valide"
    token_header = "bearer Mon_token_header"
    mock_get_user_by_email.return_value = mock_super_admin
    mock_get_role_by_id.return_value = mock_role

    # Act
    with pytest.raises(BadRoleError) as result:
        with patch("services.authent_service.jwt.decode", return_value={"sub": "admin@example.com"}):
            authent_service.get_current_super_admin(mock_db_session, token_header, access_token)

    # Assert
    assert str(result.value) == "403: You do not have the rights to access this ressource"
    mock_get_user_by_email.assert_called_once()
    mock_get_role_by_id.assert_called_once()


def test_get_current_super_admin_email_not_in_token(mock_db_session):
    # Arrange
    access_token = "Mon_token_invalide"
    token_header = "bearer Mon_token_header"

    # Act
    with patch("services.authent_service.jwt.decode", return_value={"sub": None}):
        with pytest.raises(InvalidTokenError) as result:
            authent_service.get_current_super_admin(mock_db_session, token_header, access_token)

    # Assert
    assert str(result.value) == "401: Invalid Token"


def test_get_current_super_admin_not_found(mock_db_session, mock_get_user_by_email):
    # Arrange
    access_token = "Mon_token_invalidevalide"
    token_header = "bearer Mon_token_header"
    mock_get_user_by_email.return_value = None

    # Act
    with patch("services.authent_service.jwt.decode", return_value={"sub": "admin@example.com"}):
        with pytest.raises(UserNotFoundError) as result:
            authent_service.get_current_super_admin(mock_db_session, token_header, access_token)

    # Assert
    assert str(result.value) == "404: User not found"



@pytest.mark.asyncio
async def test_refresh_token_email_not_in_payload(mock_db_session):
    # Arrange
    refresh_token = "Mon_token_invalide"

    # Act
    with patch("services.authent_service.jwt.decode", return_value={"sub": None}):
        with pytest.raises(InvalidTokenError) as result:
            await authent_service.refresh_token(mock_db_session, refresh_token)

    # Assert
    assert str(result.value) == "401: Invalid Token"


@pytest.mark.asyncio
async def test_refresh_token_no_refresh_token(mock_db_session):
    # Act / Arrange
    with patch("services.authent_service.jwt.decode", return_value={"sub": "admin@example.com"}):
        with pytest.raises(NoRefreshTokenError) as result:
            await authent_service.refresh_token(mock_db_session, None)

    # Assert
    assert str(result.value) == "400: No refresh token found"


@pytest.mark.asyncio
async def test_refresh_token_user_none(mock_db_session, mock_get_user_by_email):
    # Arrange
    refresh_token = "Mon_token_invalide"
    mock_get_user_by_email.return_value = None
    # Act
    with patch("services.authent_service.jwt.decode", return_value={"sub": "admin@example.com"}):
        with pytest.raises(UserNotFoundError) as result:
            await authent_service.refresh_token(mock_db_session, refresh_token)

    # Assert
    assert str(result.value) == "404: User not found"


@pytest.mark.asyncio
async def test_refresh_token(mock_db_session, mock_get_user_by_email, mock_user, mock_create_access_token):
    # Arrange
    refresh_token = "Mon_token_valide"
    mock_get_user_by_email.return_value = mock_user
    mock_create_access_token.return_value = "mon_access_token"

    # Act
    with patch("services.authent_service.jwt.decode", return_value={"sub": "admin@example.com"}):
        result = await authent_service.refresh_token(mock_db_session, refresh_token)

    # Assert
    assert isinstance(result, JSONResponse) == True
    assert result.body == JSONResponse(content={"access_token": "mon_access_token"}).body
    assert result.status_code == 200


@patch.dict(os.environ, {"SECRET_KEY": "mysecret", "ALGORITHM": "HS256"})
def test_get_connected_user(
    mock_db_session,
    mock_user,
    mock_get_user_by_email,
):
    # Arrange
    access_token = "Mon_token_valide"
    token_header = "bearer Mon_token_header"
    mock_get_user_by_email.return_value = mock_user

    # Act
    with patch("services.authent_service.jwt.decode", return_value={"sub": "admin@example.com"}):
        result = authent_service.get_connected_user(mock_db_session, token_header, access_token)

    # Assert
    assert result.email == mock_user.email
    assert result.password == mock_user.password
    assert result.is_planner == mock_user.is_planner
    assert result.phone_number == mock_user.phone_number
    assert result.role.role == mock_user.role.role
    mock_get_user_by_email.assert_called_once()


def test_get_connected_user_email_not_in_token(mock_db_session):
    # Arrange
    access_token = "Mon_token_invalidevalide"
    token_header = "bearer Mon_token_header"

    # Act
    with patch("services.authent_service.jwt.decode", return_value={"sub": None}):
        with pytest.raises(InvalidTokenError) as result:
            authent_service.get_connected_user(mock_db_session, token_header, access_token)

    # Assert
    assert str(result.value) == "401: Invalid Token"


def test_get_connected_user_not_found(mock_db_session, mock_get_user_by_email):
    # Arrange
    access_token = "Mon_token_invalidevalide"
    token_header = "bearer Mon_token_header"
    mock_get_user_by_email.return_value = None

    # Act
    with patch("services.authent_service.jwt.decode", return_value={"sub": "admin@example.com"}):
        with pytest.raises(UserNotFoundError) as result:
            authent_service.get_connected_user(mock_db_session, token_header, access_token)

    # Assert
    assert str(result.value) == "404: User not found"
