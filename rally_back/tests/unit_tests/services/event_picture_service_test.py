from unittest.mock import patch, MagicMock
import pytest
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from fastapi import Request

from models.event_picture_model import EventPicture
from services import event_picture_service


@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)

@pytest.fixture
def mock_request():
    return MagicMock(spec=Request)

@pytest.fixture
def mock_get_event_by_id(mocker):
    return mocker.patch("services.event_service.get_event_by_id")

@pytest.fixture
def mock_add_event_picture(mocker):
    return mocker.patch("repositories.event_picture_repo.add_new_event_picture")

@pytest.fixture
def mock_commit_event_picture(mocker):
    return mocker.patch("repositories.event_picture_repo.commit_event_picture")

@pytest.fixture
def mock_refresh_event_picture(mocker):
    return mocker.patch("repositories.event_picture_repo.refresh_event_picture")

@pytest.fixture
def mock_get_event_picture_by_id(mocker):
    return mocker.patch("repositories.event_picture_repo.get_event_picture_by_id")

@pytest.fixture
def mock_get_all_event_pictures(mocker):
    return mocker.patch("repositories.event_picture_repo.get_all_event_pictures")

@pytest.fixture
def mock_get_event_pictures_from_event_id(mocker):
    return mocker.patch("repositories.event_picture_repo.get_event_pictures_from_event_id")

@pytest.fixture
def mock_get_profile(mocker):
    return mocker.patch("services.profile_service.get_profile")

@pytest.fixture
def mock_get_picture_by_id(mocker):
    return mocker.patch("services.event_picture_service.get_picture_by_id")

@pytest.fixture
def mock_get_picture_by_name(mocker):
    return mocker.patch("services.event_picture_service.get_picture_by_name")

@pytest.fixture
def mock_create_event_picture(mocker):
    return mocker.patch("services.event_picture_service.create_event_picture")

@pytest.fixture
def mock_delete_picture(mocker):
    return mocker.patch("services.event_picture_service.delete_picture")

@pytest.fixture
def mock_get_first_picture_of_event(mocker):
    return mocker.patch("repositories.event_picture_repo.get_first_picture_of_event")

@pytest.fixture
def mock_delete_event_picture(mocker):
    return mocker.patch("repositories.event_picture_repo.delete_event_picture")

@pytest.fixture
def mock_get_picture_by_name(mocker):
    return mocker.patch("repositories.event_picture_repo.get_picture_by_name")



@pytest.fixture
def mock_event_picture():
    fake_picture = MagicMock(spec=EventPicture)
    fake_picture.event_id = 1
    fake_picture.photo = "photo.jpg"
    fake_picture.uuid = uuid4()
    return fake_picture

@pytest.fixture
def mock_event_picture2():
    fake_picture = MagicMock(spec=EventPicture)
    fake_picture.event_id = 2
    fake_picture.photo = "photo2.jpg"
    fake_picture.uuid = uuid4()
    return fake_picture


@patch("services.event_picture_service.EventPicture")
def test_create_event_picture(
    mock_event_picture_class,
    mock_event_picture,
    mock_db_session,
    mock_add_event_picture,
    mock_commit_event_picture,
    mock_refresh_event_picture
):
    # Arrange
    mock_event_picture_class.return_value = mock_event_picture
    mock_add_event_picture.return_value = None
    mock_commit_event_picture.return_value = None
    mock_refresh_event_picture.return_value = None

    # Act
    result = event_picture_service.create_event_picture(mock_db_session, 1, "photo.jpg")

    # Assert
    assert isinstance(result, EventPicture)
    assert result.event_id == mock_event_picture.event_id
    assert result.photo == mock_event_picture.photo
    assert isinstance(result.uuid, UUID)
    mock_add_event_picture.assert_called_once()
    mock_commit_event_picture.assert_called_once()
    mock_refresh_event_picture.assert_called_once()


def test_get_picture_by_id(mock_event_picture, mock_db_session, mock_get_event_picture_by_id):
    # Arrange
    mock_get_event_picture_by_id.return_value = mock_event_picture

    # Act
    result = event_picture_service.get_picture_by_id(db=mock_db_session, picture_id=1)

    # Assert
    assert isinstance(result, EventPicture)
    assert result.event_id == mock_event_picture.event_id
    assert result.photo == mock_event_picture.photo
    assert isinstance(result.uuid, UUID)
    mock_get_event_picture_by_id.assert_called_once()


def test_get_pictures(mock_event_picture, mock_db_session, mock_get_all_event_pictures):
    # Arrange
    mock_get_all_event_pictures.return_value = [mock_event_picture]

    # Act
    result = event_picture_service.get_pictures(db=mock_db_session)

    # Assert
    assert isinstance(result[0], EventPicture)
    assert result[0].event_id == mock_event_picture.event_id
    assert result[0].photo == mock_event_picture.photo
    assert isinstance(result[0].uuid, UUID)
    assert result == [mock_event_picture]
    mock_get_all_event_pictures.assert_called_once()


def test_get_pictures_from_event(mock_event_picture, mock_db_session, mock_get_event_pictures_from_event_id):
    # Arrange
    mock_get_event_pictures_from_event_id.return_value = [mock_event_picture]

    # Act
    result = event_picture_service.get_pictures_from_event(db=mock_db_session, event_id=1)

    # Assert
    assert result[0].event_id == mock_event_picture.event_id
    assert result[0].photo == mock_event_picture.photo
    assert result == [mock_event_picture]
    mock_get_event_pictures_from_event_id.assert_called_once()


def test_get_first_picture_from_event(mock_event_picture, mock_db_session, mock_get_first_picture_of_event):
    # Arrange
    mock_get_first_picture_of_event.return_value = mock_event_picture

    # Act
    result = event_picture_service.get_first_picture_of_event(db=mock_db_session, event_id=1)

    # Assert
    assert isinstance(result, EventPicture)
    assert result.event_id == mock_event_picture.event_id
    assert result.photo == mock_event_picture.photo
    assert isinstance(result.uuid, UUID)
    mock_get_first_picture_of_event.assert_called_once()


def test_delete_picture(mock_event_picture, mock_db_session, mock_get_picture_by_id, mock_delete_event_picture, mock_commit_event_picture):
    # Arrange
    mock_get_picture_by_id.return_value = mock_event_picture
    mock_delete_event_picture.return_value = None
    mock_commit_event_picture.return_value = None

    # Act
    event_picture_service.delete_picture(db=mock_db_session, picture_id=1)

    # Assert
    mock_get_picture_by_id.assert_called_once()
    mock_delete_event_picture.assert_called_once_with(mock_db_session, mock_event_picture)
    mock_commit_event_picture.assert_called_once()


def test_get_picture_by_name(mock_event_picture, mock_db_session, mock_get_picture_by_name):
    # Arrange
    mock_get_picture_by_name.return_value = mock_event_picture

    # Act
    result = event_picture_service.get_picture_by_name(db=mock_db_session, name="photo.jpg")

    # Assert
    assert isinstance(result, EventPicture)
    assert result.event_id == mock_event_picture.event_id
    assert result.photo == mock_event_picture.photo
    assert isinstance(result.uuid, UUID)
    mock_get_picture_by_name.assert_called_once()


def test_add_picture_to_event(
    mock_event_picture,
    mock_db_session,
    mock_get_picture_by_name,
    mock_event_picture2,
    mock_commit_event_picture,
    mock_refresh_event_picture
):
    # Arrange
    mock_get_picture_by_name.side_effect = [mock_event_picture, mock_event_picture2]
    mock_commit_event_picture.return_value = None
    mock_refresh_event_picture.return_value = None

    # Act
    event_picture_service.add_picture_to_event(db=mock_db_session, names=["photo.jpg", "photo2.jpg"], event_id=1)

    # Assert
    assert mock_get_picture_by_name.call_count == 2
    assert mock_refresh_event_picture.call_count == 2
    assert mock_commit_event_picture.call_count == 2


def test_add_picture_to_event_no_picture(
    mock_event_picture,
    mock_db_session,
    mock_get_picture_by_name,
    mock_event_picture2,
    mock_create_event_picture,
    mock_commit_event_picture,
    mock_refresh_event_picture
):
    # Arrange
    mock_get_picture_by_name.side_effect = [None, mock_event_picture2]
    mock_create_event_picture.return_value = mock_event_picture
    mock_commit_event_picture.return_value = None
    mock_refresh_event_picture.return_value = None

    # Act
    event_picture_service.add_picture_to_event(db=mock_db_session, names=["photo.jpg", "photo2.jpg"], event_id=1)

    # Assert
    assert mock_get_picture_by_name.call_count == 2
    assert mock_commit_event_picture.call_count == 2
    assert mock_refresh_event_picture.call_count == 2
    mock_create_event_picture.assert_called_once()


def test_delete_pictures(
    mock_event_picture,
    mock_db_session,
    mock_get_picture_by_name,
    mock_event_picture2,
    mock_delete_event_picture
):
    # Arrange
    mock_get_picture_by_name.side_effect = [mock_event_picture, mock_event_picture2]

    # Act
    event_picture_service.delete_pictures(db=mock_db_session, names=["photo.jpg", "photo2.jpg"])

    # Assert
    assert mock_get_picture_by_name.call_count == 2
    assert mock_delete_event_picture.call_count == 2
