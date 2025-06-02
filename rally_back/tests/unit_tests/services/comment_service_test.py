from unittest.mock import patch, MagicMock
import pytest
from sqlalchemy.orm import Session
from fastapi import Request

from models.comment_model import Comment
from services import comment_service



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
def mock_get_profile(mocker):
    return mocker.patch("services.profile_service.get_profile")

@pytest.fixture
def mock_get_comment_by_id(mocker):
    return mocker.patch("services.comment_service.get_comment_by_id")

@pytest.fixture
def mock_is_content_valid(mocker):
    return mocker.patch("services.bad_words_service.is_content_clean")

@pytest.fixture
def mock_add_new_comment(mocker):
    return mocker.patch("repositories.comment_repo.add_new_comment")

@pytest.fixture
def mock_commit_comment(mocker):
    return mocker.patch("repositories.comment_repo.commit_comment")

@pytest.fixture
def mock_refresh_comment(mocker):
    return mocker.patch("repositories.comment_repo.refresh_comment")

@pytest.fixture
def mock_refresh_event(mocker):
    return mocker.patch("repositories.event_repo.refresh_event")

@pytest.fixture
def mock_refresh_profile(mocker):
    return mocker.patch("repositories.profile_repo.refresh_profile")

@pytest.fixture
def mock_get_comment_by_event_id(mocker):
    return mocker.patch("repositories.comment_repo.get_comment_by_event_id")

@pytest.fixture
def mock_get_all_comments(mocker):
    return mocker.patch("repositories.comment_repo.get_all_comments")

@pytest.fixture
def mock_get_comment_by_id(mocker):
    return mocker.patch("repositories.comment_repo.get_comment_by_id")

@pytest.fixture
def mock_get_comments_by_profile_id(mocker):
    return mocker.patch("repositories.comment_repo.get_comments_by_profile_id")



@pytest.fixture
def mock_comment():
    fake_comment = MagicMock(spec=Comment)
    fake_comment.event_id = 1
    fake_comment.profile_id = 1
    fake_comment.content = "Mon super commentaire"
    return fake_comment

@pytest.fixture
def mock_profile():
    profile = MagicMock()
    return profile

@patch("services.comment_service.Comment")
def test_create_comment(
    mock_comment_class,
    mock_comment,
    mock_db_session,
    mock_add_new_comment,
    mock_commit_comment,
    mock_refresh_comment,
    mock_refresh_event,
    mock_refresh_profile,
    mock_get_profile,
    mock_is_content_valid
):
    # Arrange
    mock_comment_class.return_value = mock_comment
    mock_get_profile.return_value = mock_profile
    mock_add_new_comment.return_value = None
    mock_commit_comment.return_value = None
    mock_refresh_comment.return_value = None
    mock_refresh_event.return_value = None
    mock_refresh_profile.return_value = None
    mock_is_content_valid.return_value = True

    # Act
    result = comment_service.comment_event(
        db=mock_db_session,
        profile_id=1,
        event_id=1,
        content="Mon super commentaire"
    )

    # Assert
    assert result.profile_id == mock_comment.profile_id
    assert result.event_id == mock_comment.event_id
    assert result.content == mock_comment.content
    mock_add_new_comment.assert_called_once()
    mock_commit_comment.assert_called_once()
    mock_refresh_comment.assert_called_once()
    mock_refresh_event.assert_called_once()
    mock_refresh_profile.assert_called_once()
    mock_get_profile.assert_called_once()
    mock_is_content_valid.assert_called_once()


def test_get_comment_by_id(mock_comment, mock_db_session, mock_get_comment_by_id):
    # Arrange
    mock_get_comment_by_id.return_value = mock_comment

    # Act
    result = comment_service.get_comment_by_id(db=mock_db_session, comment_id=1)

    # Assert
    assert result.profile_id == mock_comment.profile_id
    assert result.event_id == mock_comment.event_id
    assert result.content == mock_comment.content
    mock_get_comment_by_id.assert_called_once()


def test_get_comments(mock_comment, mock_db_session, mock_get_all_comments):
    # Arrange
    mock_get_all_comments.return_value = [mock_comment]

    # Act
    result = comment_service.get_all_comments(mock_db_session, 1, 2)

    # Assert
    assert result[0].profile_id == mock_comment.profile_id
    assert result[0].event_id == mock_comment.event_id
    assert result[0].content == mock_comment.content
    assert result == [mock_comment]
    mock_get_all_comments.assert_called_once()


def test_get_comment_by_event_id(mock_comment, mock_db_session, mock_get_comment_by_event_id):
    # Arrange
    mock_get_comment_by_event_id.return_value = [mock_comment]

    # Act
    result = comment_service.get_comment_by_event(
        db=mock_db_session,
        event_id=1,
        offset=1,
        limit=2
    )

    # Assert
    assert result[0].profile_id == mock_comment.profile_id
    assert result[0].event_id == mock_comment.event_id
    assert result[0].content == mock_comment.content
    assert result == [mock_comment]
    mock_get_comment_by_event_id.assert_called_once()


def test_get_comment_from_profile(mock_comment, mock_db_session, mock_get_comments_by_profile_id):
    # Arrange
    mock_get_comments_by_profile_id.return_value = [mock_comment]

    # Act
    result = comment_service.get_comment_from_profile(
        db=mock_db_session,
        profile_id=1,
        offset=1,
        limit=2
    )

    # Assert
    assert result[0].profile_id == mock_comment.profile_id
    assert result[0].event_id == mock_comment.event_id
    assert result[0].content == mock_comment.content
    assert result == [mock_comment]
    mock_get_comments_by_profile_id.assert_called_once()
