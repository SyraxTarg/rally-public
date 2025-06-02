from sqlalchemy.orm import Session
from fastapi import status

from services import event_service, profile_service, bad_words_service
from models.comment_model import Comment
from repositories import comment_repo, event_repo, profile_repo
from errors import EventNotFound, ProfileNotFound, CommentNotFound, InvalidContent

def comment_event(db: Session, profile_id: int, event_id: int, content: str) -> Comment:
    """used to comment an event"""
    if not bad_words_service.is_content_clean(content):
        raise InvalidContent(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The comment contains invalid terms"
        )

    event = event_service.get_event_by_id(db, event_id)
    if not event:
        raise EventNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    profile = profile_service.get_profile(db, event.profile_id) if event else None
    if not profile:
        raise ProfileNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    comment = Comment(event_id=event.id, profile_id=profile_id, content=content)
    event.nb_comments += 1
    comment_repo.add_new_comment(db, comment)
    comment_repo.commit_comment(db)
    comment_repo.refresh_comment(db, comment)
    event_repo.refresh_event(db, event)
    profile_repo.refresh_profile(db, profile)

    return comment

def get_comment_by_event(db: Session, event_id: int, offset: int, limit: int)->list[Comment]:
    """used to fetch comment by their event"""
    return comment_repo.get_comment_by_event_id(db, event_id, offset, limit)

def get_all_comments_no_limit_by_event(db: Session, event_id: int)->list[Comment]:
    """used to fetch comment by their event"""
    return comment_repo.get_all_comments_by_event_id(db, event_id)


def get_all_comments(db: Session, offset: int, limit: int)->list[Comment]:
    """used to fetch all comments"""
    return comment_repo.get_all_comments(db, offset, limit)

def get_comment_by_id(db: Session, comment_id: int)->Comment:
    """used to fetch a comment by its id"""
    comment = comment_repo.get_comment_by_id(db, comment_id)
    if not comment:
        raise CommentNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    return comment

def get_comment_from_profile(db: Session, profile_id: int, offset: int, limit: int)->list[Comment]:
    """used to fetch comments by their profile"""
    return comment_repo.get_comments_by_profile_id(db, profile_id, offset, limit)
