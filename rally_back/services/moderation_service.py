from sqlalchemy.orm import Session
from fastapi import status

from services import (
    banned_user_service,
    comment_service,
    event_service,
    like_service,
    signaled_comment_service,
    signaled_event_service,
    signaled_user_service,
    user_service,
    registration_service
)
from errors import (
    CommentNotFound,
    BadRoleError,
    EventNotFound,
    SignaledCommentNotFound,
    SignaledEventNotFound,
    SignaledUserNotFound,
    UserNotFoundError
)
from repositories import (
    user_repo,
    comment_repo,
    event_repo,
    signaled_comment_repo,
    signaled_event_repo,
    signaled_user_repo,
    address_repo,
    like_repo
)



def delete_comment(db: Session, comment_id: int, current_user_id: int) -> bool:
    """used to delete a comment"""
    comment = comment_service.get_comment_by_id(db, comment_id)
    if not comment:
        raise CommentNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    is_admin = user_service.is_admin(db, current_user_id)
    if comment.profile_id != current_user_id and not is_admin:
        raise BadRoleError(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé"
        )

    # Supprimer les signalements liés au commentaire
    signaled_comments = signaled_comment_service.get_signaled_comment_by_comment_id(db, comment_id)
    for signaled_comment in signaled_comments:
        signaled_comment_repo.delete_signaled_comment(db, signaled_comment)
    # Récupérer l'événement lié (pour mettre à jour le nombre de commentaires)
    event = event_service.get_event_by_id(db, comment.event_id)

    # Supprimer le commentaire
    comment_repo.delete_comment(db, comment)

    # S'assurer que l'événement existe avant de modifier nb_comments
    if event and event.nb_comments is not None and event.nb_comments > 0:
        event.nb_comments -= 1

    comment_repo.commit_comment(db)
    return True


def delete_event(db: Session, event_id: int, current_user_id: int) -> None:
    """used to delete an event"""
    event = event_service.get_event_by_id(db, event_id)
    if not event:
        raise EventNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    is_admin = user_service.is_admin(db, current_user_id)
    if current_user_id != event.profile_id and not is_admin:
        raise BadRoleError(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé"
        )

    comments = comment_service.get_all_comments_no_limit_by_event(db, event.id)
    for comment in comments:
        delete_comment(db, comment.id, current_user_id)

    likes = like_service.get_likes_from_event(db, event.id)
    for like in likes:
        like_service.unlike_event(db, like.profile_id, like.event_id)

    registrations = registration_service.get_all_registrations_from_event(db, event.id)
    for registration in registrations:
        registration_service.delete_registration(db, registration.profile_id, registration.event_id)

    signaled_events = signaled_event_service.get_signaled_event_by_event_id(db, event.id)
    for signaled_event in signaled_events:
        signaled_event_repo.delete_signaled_event(db, signaled_event)

    event_repo.delete_event(db, event)

    if event.address:
        address_repo.delete_address(db, event.address)

    event_repo.commit_event(db)


def delete_signaled_comment(db: Session, signaled_comment_id: int, ban: bool, current_user_id: int) -> None:
    """used to delete a signaled comment"""
    signaled_comment = signaled_comment_service.get_signaled_comment_by_id(db, signaled_comment_id)

    if not signaled_comment:
        raise SignaledCommentNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="la ressource n'existe pas"
        )

    # Supprimer le signalement principal
    signaled_comment_repo.delete_signaled_comment(db, signaled_comment)

    if ban:
        # Supprimer le commentaire
        delete_comment(db, signaled_comment.comment_id, current_user_id)

    signaled_comment_repo.commit_signaled_comment(db)


def delete_signaled_event(db: Session, signaled_event_id: int, ban: bool, current_user_id: int)->None:
    """used to delete a signaled event"""
    signaled_event = signaled_event_service.get_signaled_event_by_id(db, signaled_event_id)
    if not signaled_event:
        raise SignaledEventNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Signalment not found"
        )
    signaled_event_repo.delete_signaled_event(db, signaled_event)

    if ban:
        delete_event(db, signaled_event.event_id, current_user_id)

    signaled_event_repo.commit_signaled_events(db)


def delete_signaled_user(db: Session, signaled_user_id: int, ban: bool, current_user_id: int) -> None:
    """used to delete a signaled user"""
    signaled_user = signaled_user_service.get_signaled_user(db, signaled_user_id)
    if not signaled_user:
        raise SignaledUserNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="la ressource n'existe pas"
        )

    # Supprimer ce signalement
    signaled_user_repo.delete_signaled_user(db, signaled_user)

    if ban:
        user_signaled = user_service.get_user(db, signaled_user.user_signaled_id)
        signaled_by = user_service.get_user(db, current_user_id)

        banned_user_service.create_banned_user(db, user_signaled.email, signaled_by.email)
        # Supprimer l'utilisateur signalé
        delete_user(db, signaled_user.user_signaled_id, current_user_id)

    signaled_user_repo.commit_signaled_user(db)


def delete_user(db: Session, user_id: int, current_user_id: int) -> bool:
    """used to delete a user"""
    user = user_service.get_user(db, user_id)
    if not user:
        return UserNotFoundError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="la ressource n'existe pas"
        )

    is_admin = user_service.is_admin(db, current_user_id)
    if current_user_id != user.id and not is_admin:
        raise BadRoleError(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé"
        )

    # Suppression des signalements FAITS PAR le user
    signalements_par = signaled_user_service.get_signaled_user_by_user_by_id(db, user.id)
    for s in signalements_par:
        signaled_user_repo.delete_signaled_user(db, s)

    # Suppression des signalements CONTRE le user
    signalements_contre = signaled_user_service.get_signaled_user_by_id(db, user.id)
    for s in signalements_contre:
        if s not in signalements_par:
            signaled_user_repo.delete_signaled_user(db, s)


    events = event_service.get_all_events_by_profile(db, user.id)
    for event in events:
        delete_event(db, event.id, current_user_id)

    comments = comment_service.get_comment_from_profile(db, user.id)
    for comment in comments:
        delete_comment(db, comment.id, current_user_id)

    likes = like_service.get_likes_from_profile(db, user.id)
    for like in likes:
        like_repo.delete_like(db, like)


    # Suppression du user
    user_repo.delete_user(db, user)
    user_repo.commit_user(db)
    return True
