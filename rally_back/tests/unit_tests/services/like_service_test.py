from unittest.mock import patch, MagicMock
import pytest
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import Request

from models.event_model import Event
from models.like_model import Like
from models.profile_model import Profile
from services import like_service
from errors import EventNotFound, ProfileNotFound



@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)

@pytest.fixture
def mock_request():
    return MagicMock(spec=Request)

@pytest.fixture
def mock_add_types_to_event(mocker):
    return mocker.patch("services.event_service.add_types_to_event")

@pytest.fixture
def mock_get_like(mocker):
    return mocker.patch("services.like_service.get_like")

@pytest.fixture
def mock_get_event_by_id(mocker):
    return mocker.patch("services.event_service.get_event_by_id")

@pytest.fixture
def mock_get_profile_by_id(mocker):
    return mocker.patch("services.profile_service.get_profile")

@pytest.fixture
def mock_add_like(mocker):
    return mocker.patch("repositories.like_repo.add_like")

@pytest.fixture
def mock_commit_like(mocker):
    return mocker.patch("repositories.like_repo.commit_like")

@pytest.fixture
def mock_refresh_like(mocker):
    return mocker.patch("repositories.like_repo.refresh_like")

@pytest.fixture
def mock_refresh_event(mocker):
    return mocker.patch("repositories.event_repo.refresh_event")

@pytest.fixture
def mock_refresh_profile(mocker):
    return mocker.patch("repositories.profile_repo.refresh_profile")

@pytest.fixture
def mock_get_like_by_profile_and_event(mocker):
    return mocker.patch("repositories.like_repo.get_like_by_profile_and_event")

@pytest.fixture
def mock_delete_like(mocker):
    return mocker.patch("repositories.like_repo.delete_like")



@pytest.fixture
def mock_event():
    fake_event = MagicMock(spec=Event)
    fake_event.title = "Titre"
    fake_event.description = "mon event"
    fake_event.nb_places = 4
    fake_event.price = 3.0
    fake_event.profile_id = 1
    fake_event.nb_likes = 12
    fake_event.nb_comments = 4
    fake_event.date = datetime.now()
    fake_event.cloture_billets = datetime.now()
    fake_event.address_id = 1
    fake_event.created_at = datetime.now()
    fake_event.updated_at = datetime.now()
    return fake_event

@pytest.fixture
def mock_like():
    fake_like = MagicMock(spec=Like)
    fake_like.profile_id = 1
    fake_like.event_id = 2
    return fake_like

@pytest.fixture
def mock_profile():
    fake_profile = MagicMock(spec=Profile)
    return fake_profile

@patch("services.like_service.Like")
def test_like_event(
    mock_like_model,
    mock_db_session,
    mock_get_like,
    mock_get_profile_by_id,
    mock_get_event_by_id,
    mock_event,
    mock_profile,
    mock_like,
    mock_add_like,
    mock_commit_like,
    mock_refresh_event,
    mock_refresh_like,
    mock_refresh_profile
):
    # Arrange
    mock_like_model.return_value = mock_like
    mock_get_like.return_value = None
    mock_get_event_by_id.return_value = mock_event
    mock_get_profile_by_id.return_value = mock_profile
    mock_add_like.return_value = None
    mock_commit_like.return_value = None
    mock_refresh_event.return_value = None
    mock_refresh_like.return_value = None
    mock_refresh_profile.return_value = None

    # Act
    result = like_service.like_event(mock_db_session, 1, 2)

    # Assert
    assert result == mock_like
    mock_get_like.assert_called_once()
    mock_get_event_by_id.assert_called_once()
    mock_get_profile_by_id.assert_called_once()
    mock_add_like.assert_called_once_with(mock_db_session, mock_like)
    mock_commit_like.assert_called_once()
    mock_refresh_event.assert_called_once()
    mock_refresh_like.assert_called_once()
    mock_refresh_profile.assert_called_once()


@patch("services.like_service.Like")
def test_like_event_already_liked(
    mock_like_model,
    mock_db_session,
    mock_get_like,
    mock_like
):
    # Arrange
    mock_like_model.return_value = mock_like
    mock_get_like.return_value = mock_like

    # Act
    result = like_service.like_event(mock_db_session, 1, 2)

    # Assert
    assert result == mock_like
    mock_get_like.assert_called_once()


@patch("services.like_service.Like")
def test_like_event_no_event(
    mock_like_model,
    mock_db_session,
    mock_get_like,
    mock_get_profile_by_id,
    mock_get_event_by_id,
    mock_like
):
    # Arrange
    mock_like_model.return_value = mock_like
    mock_get_like.return_value = None
    mock_get_event_by_id.return_value = None

    # Act
    with pytest.raises(EventNotFound) as result:
        like_service.like_event(mock_db_session, 1, 2)

    # Assert
    assert str(result.value) == "404: Event not found"
    mock_get_like.assert_called_once()
    mock_get_event_by_id.assert_called_once()
    mock_get_profile_by_id.assert_not_called()


@patch("services.like_service.Like")
def test_like_event_no_profile(
    mock_like_model,
    mock_db_session,
    mock_get_like,
    mock_get_profile_by_id,
    mock_get_event_by_id,
    mock_like,
    mock_event
):
    # Arrange
    mock_like_model.return_value = mock_like
    mock_get_like.return_value = None
    mock_get_event_by_id.return_value = mock_event
    mock_get_profile_by_id.return_value = None

    # Act
    with pytest.raises(ProfileNotFound) as result:
        like_service.like_event(mock_db_session, 1, 2)

    # Assert
    assert str(result.value) == "404: Profile not found"
    mock_get_like.assert_called_once()
    mock_get_event_by_id.assert_called_once()
    mock_get_profile_by_id.assert_called_once()


def test_get_like(
    mock_db_session,
    mock_like,
    mock_get_like_by_profile_and_event
):
    # Arrange
    mock_get_like_by_profile_and_event.return_value = mock_like

    # Act
    result = like_service.get_like(mock_db_session, 1, 2)

    # Assert
    assert result.profile_id == mock_like.profile_id
    assert result.event_id == mock_like.event_id
    mock_get_like_by_profile_and_event.assert_called_once()


def test_unlike_event(
    mock_db_session,
    mock_get_like,
    mock_get_profile_by_id,
    mock_get_event_by_id,
    mock_event,
    mock_profile,
    mock_like,
    mock_delete_like,
    mock_commit_like,
    mock_refresh_event,
    mock_refresh_profile
):
    # Arrange
    mock_get_like.return_value = mock_like
    mock_event.nb_like = 12
    mock_get_event_by_id.return_value = mock_event
    mock_profile.nb_like = 4
    mock_get_profile_by_id.return_value = mock_profile
    mock_delete_like.return_value = None
    mock_commit_like.return_value = None
    mock_refresh_event.return_value = None
    mock_refresh_profile.return_value = None

    # Act
    result = like_service.unlike_event(mock_db_session, 1, 2)

    # Assert
    assert result == True
    mock_get_like.assert_called_once()
    mock_get_event_by_id.assert_called_once()
    mock_get_profile_by_id.assert_called_once()
    mock_delete_like.assert_called_once_with(mock_db_session, mock_like)
    mock_commit_like.assert_called_once()
    mock_refresh_event.assert_called_once()
    mock_refresh_profile.assert_called_once()
