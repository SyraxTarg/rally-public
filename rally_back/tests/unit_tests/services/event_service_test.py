from unittest.mock import patch, MagicMock
import pytest
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import Request

from models.event_model import Event
from models.type_model import Type
from services import event_service
from errors import EventNotFound



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
def mock_get_profile(mocker):
    return mocker.patch("services.profile_service.get_profile")

@pytest.fixture
def mock_remove_types_to_event(mocker):
    return mocker.patch("services.event_service.remove_types_to_event")

@pytest.fixture
def mock_get_event_by_id(mocker):
    return mocker.patch("services.event_service.get_event_by_id")

@pytest.fixture
def mock_create_event_picture(mocker):
    return mocker.patch("services.event_picture_service.create_event_picture")

@pytest.fixture
def mock_delete_picture(mocker):
    return mocker.patch("services.event_picture_service.delete_picture")

@pytest.fixture
def mock_get_type_by_id(mocker):
    return mocker.patch("repositories.type_repo.get_type_by_id")

@pytest.fixture
def mock_add_new_event(mocker):
    return mocker.patch("repositories.event_repo.add_new_event")

@pytest.fixture
def mock_commit_event(mocker):
    return mocker.patch("repositories.event_repo.commit_event")

@pytest.fixture
def mock_refresh_event(mocker):
    return mocker.patch("repositories.event_repo.refresh_event")

@pytest.fixture
def mock_get_event_by_id(mocker):
    return mocker.patch("repositories.event_repo.get_event_by_id")

@pytest.fixture
def mock_get_events_by_profile(mocker):
    return mocker.patch("repositories.event_repo.get_events_by_profile")

@pytest.fixture
def mock_get_events_filters(mocker):
    return mocker.patch("repositories.event_repo.get_events_filters")


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
def mock_type():
    fake_type = MagicMock(spec=Type)
    return fake_type


@patch("services.event_service.Event")
def test_create_event(
    mock_event_class,
    mock_event,
    mock_db_session,
    mock_add_types_to_event,
    mock_add_new_event,
    mock_commit_event,
    mock_refresh_event
):
    # Arrange
    mock_event_class.return_value = mock_event
    mock_add_new_event.return_value = None
    mock_commit_event.return_value = None
    mock_refresh_event.return_value = None

    # Act
    result = event_service.create_event(
        mock_db_session,
        "Titre",
        "mon event",
        4,
        3.0,
        1,
        datetime.now(),
        datetime.now(),
        [1, 2, 3],
        1
    )

    # Assert
    assert result.title == mock_event.title
    assert result.description == mock_event.description
    assert result.nb_places == mock_event.nb_places
    assert result.profile_id == mock_event.profile_id
    assert result.nb_likes == mock_event.nb_likes
    assert result.nb_comments == mock_event.nb_comments
    mock_add_new_event.assert_called_once_with(mock_db_session, mock_event)
    mock_commit_event.assert_called_once()
    mock_refresh_event.assert_called_once()
    mock_add_types_to_event.assert_called_once()


def test_get_event_by_id(mock_db_session, mock_event, mock_get_event_by_id):
    # Arrange
    mock_get_event_by_id.return_value = mock_event

    # Act
    result = event_service.get_event_by_id(mock_db_session, 1)

    # Assert
    assert result.title == mock_event.title
    assert result.description == mock_event.description
    assert result.nb_places == mock_event.nb_places
    assert result.profile_id == mock_event.profile_id
    assert result.nb_likes == mock_event.nb_likes
    assert result.nb_comments == mock_event.nb_comments
    mock_get_event_by_id.assert_called_once


def test_get_event_by_id_no_event(mock_db_session, mock_get_event_by_id):
    # Arrange
    mock_get_event_by_id.return_value = None

    # Act
    with pytest.raises(EventNotFound) as result:
        event_service.get_event_by_id(mock_db_session, 1)

    # Assert
    assert str(result.value) == "404: event does not exist"
    mock_get_event_by_id.assert_called_once


def test_get_events_filters(mock_db_session, mock_event, mock_get_events_filters):
    # Arrange
    mock_get_events_filters.return_value = [mock_event]

    # Act
    result = event_service.get_events_filters(mock_db_session)

    # Assert
    assert result[0].title == mock_event.title
    assert result[0].description == mock_event.description
    assert result[0].nb_places == mock_event.nb_places
    assert result[0].profile_id == mock_event.profile_id
    assert result[0].nb_likes == mock_event.nb_likes
    assert result[0].nb_comments == mock_event.nb_comments
    assert result == [mock_event]


def test_update_event(
    mock_db_session,
    mock_get_event_by_id,
    mock_add_types_to_event,
    mock_remove_types_to_event,
    mock_event,
    mock_commit_event,
    mock_refresh_event
):
    # Arrange
    mock_get_event_by_id.return_value = mock_event
    mock_commit_event.return_value = None
    mock_refresh_event.return_value = None

    # Act
    result = event_service.update_event(
        mock_db_session,
        1,
        "Titre",
        "mon event",
        4,
        3.0,
        datetime.now(),
        datetime.now(),
        [1, 2, 3],
    )

    # Assert
    assert result.title == mock_event.title
    assert result.description == mock_event.description
    assert result.nb_places == mock_event.nb_places
    assert result.profile_id == mock_event.profile_id
    assert result.nb_likes == mock_event.nb_likes
    assert result.nb_comments == mock_event.nb_comments
    mock_commit_event.assert_called_once()
    mock_refresh_event.assert_called_once()
    mock_add_types_to_event.assert_called_once()
    mock_remove_types_to_event.assert_called_once()


def test_add_types_to_event(
    mock_db_session,
    mock_get_event_by_id,
    mock_get_type_by_id,
    mock_event,
    mock_type,
    mock_commit_event
):
    # Arrange
    mock_get_event_by_id.return_value = mock_event
    mock_get_type_by_id.side_effect = [mock_type, mock_type]
    mock_commit_event.return_value = None

    # Act
    result = event_service.add_types_to_event(mock_db_session, 1, [1, 2])

    # Assert
    assert result.title == mock_event.title
    assert result.description == mock_event.description
    assert result.nb_places == mock_event.nb_places
    assert result.profile_id == mock_event.profile_id
    assert result.nb_likes == mock_event.nb_likes
    assert result.nb_comments == mock_event.nb_comments
    assert mock_get_type_by_id.call_count == 2
    mock_get_event_by_id.assert_called_once()
    mock_commit_event.assert_called_once()


def test_remove_types_to_event(
    mock_db_session,
    mock_get_event_by_id,
    mock_get_type_by_id,
    mock_event,
    mock_type,
    mock_commit_event
):
    # Arrange
    mock_get_event_by_id.return_value = mock_event
    mock_get_type_by_id.side_effect = [mock_type, mock_type]
    mock_commit_event.return_value = None

    # Act
    result = event_service.remove_types_to_event(mock_db_session, 1, [1, 2])

    # Assert
    assert result.title == mock_event.title
    assert result.description == mock_event.description
    assert result.nb_places == mock_event.nb_places
    assert result.profile_id == mock_event.profile_id
    assert result.nb_likes == mock_event.nb_likes
    assert result.nb_comments == mock_event.nb_comments
    assert mock_get_type_by_id.call_count == 2
    mock_get_event_by_id.assert_called_once()
    mock_commit_event.assert_called_once()


def test_get_events_by_profile(mock_db_session, mock_event, mock_get_events_by_profile):
    # Arrange
    mock_get_events_by_profile.return_value = [mock_event]

    # Act
    result = event_service.get_events_by_profile(mock_db_session, 1, 1, 2)

    # Assert
    assert result[0].title == mock_event.title
    assert result[0].description == mock_event.description
    assert result[0].nb_places == mock_event.nb_places
    assert result[0].profile_id == mock_event.profile_id
    assert result[0].nb_likes == mock_event.nb_likes
    assert result[0].nb_comments == mock_event.nb_comments
    assert result == [mock_event]
    mock_get_events_by_profile.assert_called_once()
