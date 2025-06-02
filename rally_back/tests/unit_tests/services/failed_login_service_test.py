from unittest.mock import patch, MagicMock
import pytest
from sqlalchemy.orm import Session

from models.failed_login_model import FailedLogin
from services import failed_login_service

 

@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)

@pytest.fixture
def mock_get_failed_login_by_ip_address(mocker):
    return mocker.patch("repositories.failed_login_repo.get_failed_login_by_ip_address")

@pytest.fixture
def mock_add_new_failed_login(mocker):
    return mocker.patch("repositories.failed_login_repo.add_new_failed_login")

@pytest.fixture
def mock_commit_failed_login(mocker):
    return mocker.patch("repositories.failed_login_repo.commit_failed_login")

@pytest.fixture
def mock_refresh_failed_login(mocker):
    return mocker.patch("repositories.failed_login_repo.refresh_failed_login")

@pytest.fixture
def mock_delete_failed_login(mocker):
    return mocker.patch("repositories.failed_login_repo.delete_failed_login")

@pytest.fixture
def mock_failed_login():
    fake_failed_login = MagicMock(spec=FailedLogin)
    fake_failed_login.ip_address = 123
    return fake_failed_login


def test_get_failed_login(mock_db_session, mock_failed_login, mock_get_failed_login_by_ip_address):
    # Arrange
    mock_get_failed_login_by_ip_address.return_value = mock_failed_login

    # Act
    result = failed_login_service.get_failed_login(mock_db_session, 123)

    # Assert
    assert result == mock_failed_login
    mock_get_failed_login_by_ip_address.assert_called_once()


@patch("services.failed_login_service.FailedLogin")
def test_create_failed_login(
    mock_failed_login_model,
    mock_db_session,
    mock_failed_login,
    mock_add_new_failed_login,
    mock_commit_failed_login,
    mock_refresh_failed_login
):
    # Arrange
    mock_failed_login_model.return_value = mock_failed_login
    mock_add_new_failed_login.return_avleu = None
    mock_commit_failed_login.return_value = None
    mock_refresh_failed_login.return_value = None

    # Act
    failed_login_service.create_failed_login(db=mock_db_session, client_ip=123)

    # Assert
    mock_add_new_failed_login.assert_called_once_with(mock_db_session, mock_failed_login)
    mock_commit_failed_login.assert_called_once()
    mock_refresh_failed_login.assert_called_once_with(mock_db_session, mock_failed_login)


def test_update_failed_login(mock_db_session, mock_failed_login, mock_commit_failed_login):
    # Arrange
    mock_commit_failed_login.return_value = None

    # Act
    failed_login_service.update_failed_login(mock_db_session, mock_failed_login)

    # Assert
    mock_commit_failed_login.assert_called_once()


def test_delete_failed_login(
    mock_db_session,
    mock_failed_login,
    mock_delete_failed_login,
    mock_commit_failed_login
):
    # Arrange
    mock_commit_failed_login.return_value = None
    mock_delete_failed_login.return_value = None

    # Act
    failed_login_service.delete_failed_login(mock_db_session, mock_failed_login)

    # Assert
    mock_delete_failed_login.assert_called_once_with(mock_db_session, mock_failed_login)
    mock_commit_failed_login.assert_called_once()


def test_reset_failed_login(mock_db_session, mock_failed_login, mock_commit_failed_login):
    # Arrange
    mock_commit_failed_login.return_value = None

    # Act
    failed_login_service.reset_failed_login(mock_db_session, mock_failed_login)

    # Assert
    mock_commit_failed_login.assert_called_once()