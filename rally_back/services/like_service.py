from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import status
from services import event_service, profile_service
from models.like_model import Like
from repositories import event_repo, like_repo, profile_repo
from errors import EventNotFound, ProfileNotFound, LikeNotFoundError


def like_event(db: Session, profile_id: int, event_id: int) -> Like:
    """used to like an event"""
    like = get_like(db, profile_id, event_id)

    if like:
        return like

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

    like = Like(profile_id=profile_id, event_id=event_id)
    like_repo.add_like(db, like)

    event.nb_likes = (event.nb_likes or 0) + 1
    event.updated_at = datetime.now()

    profile.nb_like = (profile.nb_like or 0) + 1
    profile.updated_at = datetime.now()

    like_repo.commit_like(db)

    like_repo.refresh_like(db, like)
    event_repo.refresh_event(db, event)
    profile_repo.refresh_profile(db, profile)

    return like


def get_like(db: Session, profile_id: int, event_id: int) -> Like:
    """used to fetch a like by its profile and event"""
    like = like_repo.get_like_by_profile_and_event(db, profile_id, event_id)
    return like


def unlike_event(db: Session, profile_id: int, event_id: int) -> bool:
    """used to remove a like"""
    like = get_like(db, profile_id, event_id)

    if not like:
        raise LikeNotFoundError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Like not found"
        )

    event = event_service.get_event_by_id(db, event_id)
    if not event:
        raise EventNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    profile = profile_service.get_profile(db, profile_id) if event else None
    if not profile:
        raise ProfileNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    like_repo.delete_like(db, like)

    event.nb_likes = max(0, (event.nb_likes or 0) - 1)
    event.updated_at = datetime.now()

    profile.nb_like = max(0, (profile.nb_like or 0) - 1)
    profile.updated_at = datetime.now()

    like_repo.commit_like(db)

    event_repo.refresh_event(db, event)
    profile_repo.refresh_profile(db, profile)

    return True

def get_likes(db: Session, offset: int, limit: int) -> list[Like]:
    """used to get all likes"""
    return like_repo.get_likes(db, offset, limit)

def get_likes_from_event(db: Session, event_id: int)->list[Like]:
    """used to get all likes from an event"""
    return like_repo.get_likes_from_event(db, event_id)

def get_likes_from_profile(db: Session, profile_id: int)->list[Like]:
    """used to get all likes from a profile"""
    return like_repo.get_likes_from_profile(db, profile_id)
