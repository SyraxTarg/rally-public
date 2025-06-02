import os
import re
import random
from datetime import datetime, timedelta
import jwt
from jinja2 import Environment, FileSystemLoader
from fastapi import Depends, status, Cookie, Request, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from database.db import get_db
from core.security import verify_password
from models.user_model import User
from schemas.request_schemas.user_schema import UserAuth
from services import (
    banned_user_service,
    failed_login_service,
    role_service,
    user_service,
    email_service
)
from enums.role import RoleEnum
from repositories import user_repo, profile_repo
from errors import (
    UserBannedError,
    TooManyAttemptsError,
    InvalidCredentialsError,
    InvalidTokenError,
    UserNotFoundError,
    BadRoleError,
    NoRefreshTokenError,
    VerificationTokenExpiredError,
    UserNotVerifiedError,
    DifferentPasswordsError
)



load_dotenv()

HOST = os.getenv("RALLY_HOST", "https://127.0.0.1:8000/api/v1")


def generate_code()->int:
    """used to generate a random token with 6 numbers"""
    return random.randint(100000, 999999)


def register_user(
    db: Session,
    email: str,
    password: str,
    phone_number: str,
    first_name: str,
    last_name: str,
    photo: str
)->User:
    """used to register a user"""
    if banned_user_service.get_banned_user_by_email(db, email):
        raise UserBannedError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cet utilisateur a été banni. Création du compte impossible."
        )
    return user_service.create_user(db, email, password, phone_number, first_name, last_name, photo)

def register_admin(
    db: Session,
    email: str,
    password: str,
    phone_number: str,
    first_name: str,
    last_name: str,
    photo: str
)->User:
    """used to register a new admin"""
    if banned_user_service.get_banned_user_by_email(db, email):
        raise UserBannedError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cet utilisateur a été banni. Création du compte impossible."
        )
    return user_service.create_admin(db, email, password, phone_number, first_name, last_name, photo)

def register_super_admin(
    db: Session,
    email: str,
    password: str,
    phone_number: str,
    first_name: str,
    last_name: str,
    photo: str
)->User:
    """used to register a new super admin"""
    if banned_user_service.get_banned_user_by_email(db, email):
        raise UserBannedError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cet utilisateur a été banni. Création du compte impossible."
        )
    return user_service.create_super_admin(db, email, password, phone_number, first_name, last_name, photo)

def create_access_token(data: dict, expires_delta: timedelta = None)->str:
    """used to create a new access token"""
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))


def is_password_strong(password: str)->bool:
    """used to verify if the given password is strong enough"""
    return len(password) >= 8 and bool(re.search(r"[A-Z]", password)) and bool(re.search(r"\d", password))


def create_refresh_token(data: dict, expires_delta: timedelta = None)->str:
    """used to create a refresh token"""
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(days=7))  # Expire dans une semaine
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))


async def login_for_access_token(
    request: Request,
    user_login: UserAuth,
    db: Session = Depends(get_db)
)->JSONResponse:
    """used to login user"""
    client_ip = request.client.host
    failed_login = failed_login_service.get_failed_login(db, client_ip)

    if failed_login:
        # Reset après 60s
        if datetime.now() - failed_login.last_attempt > timedelta(minutes=1):
            failed_login.attempts = 0

        if failed_login.attempts >= 5:
            raise TooManyAttemptsError(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many login attempts. Try again later."
            )

    user = user_service.get_user_by_email(db, user_login.email)
    if not user or not verify_password(user_login.password, user.password):
        if not failed_login:
            failed_login_service.create_failed_login(db, client_ip)
        else:
            failed_login_service.update_failed_login(db, failed_login)

        raise InvalidCredentialsError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    if not user.is_verified:
        raise UserNotVerifiedError(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not verified"
        )

    # Reset tentatives si succès
    if failed_login:
        failed_login_service.delete_failed_login(db, failed_login)

    # Générer les tokens
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))))
    refresh_token = create_refresh_token(data={"sub": user.email}, expires_delta=timedelta(days=7))  # Le refresh token dure 7 jours

    # Réponse avec les tokens et cookie
    response = JSONResponse(content={"msg": "Login successful", "access_token": access_token, "refresh_token": refresh_token, "user_id": user.id})

    # Envoi de l'access_token dans un cookie sécurisé
    # response.set_cookie("access_token", access_token, httponly=True, secure=True, samesite="Strict")
    response.set_cookie(
        "access_token",
        access_token,
        httponly=True,  # Le cookie ne peut pas être lu par JavaScript
        secure=False,   # Utiliser True en production avec HTTPS
        samesite="Strict",  # Peut être "Lax" ou "Strict"
        # max_age=int(timedelta(minutes=30).total_seconds()),
    ) #en attendant https

    # Envoi du refresh_token dans un cookie sécurisé
    # response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, samesite="Strict")
    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        secure=False,
        samesite="Strict",
        # max_age=int(timedelta(days=7)),
    ) # en attendant https

    return response

def get_connected_user(
    db: Session = Depends(get_db),
    authorization: str = Header(None),
    access_token: str = Cookie(None)
) -> User:
    print(f"POPOOOOOO ", authorization, access_token)
    if not authorization and not access_token:
        print("MISSING")
        raise InvalidTokenError(status_code=401, detail="Authorization header or cookie is required")

    try:
        if authorization:
            parts = authorization.split()
            if len(parts) != 2 or parts[0].lower() != "bearer":
                print("INVALID FORMAT")
                raise InvalidTokenError(status_code=401, detail="Invalid Authorization header format")

            token = parts[1]
        elif access_token:
            token = access_token
        else:
            print("NO TOKEN")
            raise InvalidTokenError(status_code=401, detail="No token provided")
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        email = payload.get("sub")
        if not email:
            print("NO EMAIL")
            raise InvalidTokenError(status_code=401, detail="Invalid Token")

        user = user_service.get_user_by_email(db, email)
        if not user:
            raise UserNotFoundError(status_code=404, detail="User not found")

        return user

    except jwt.PyJWTError:
        print("EXPIRED")
        raise InvalidTokenError(status_code=401, detail="Invalid or expired token")


def get_current_user(
    db: Session,
    authorization: str = Header(None),
    access_token: str = Cookie(None)
) -> User:
    """Get current user, checking token from Authorization header or cookie"""

    if not authorization and not access_token:
        raise InvalidTokenError(status_code=401, detail="Authorization header or cookie required")

    if authorization and access_token:
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise InvalidTokenError(status_code=401, detail="Invalid Authorization header format")
        token_from_header = parts[1]
        token_to_use = token_from_header
    else:
        if authorization:
            parts = authorization.split()
            if len(parts) != 2 or parts[0].lower() != "bearer":
                raise InvalidTokenError(status_code=401, detail="Invalid Authorization header format")
            token_to_use = parts[1]
        else:
            token_to_use = access_token

    try:
        payload = jwt.decode(token_to_use, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        email = payload.get("sub")
        if not email:
            raise InvalidTokenError(status_code=401, detail="Invalid Token")

        user = user_service.get_user_by_email(db, email)
        if not user:
            raise UserNotFoundError(status_code=404, detail="User not found")

        if RoleEnum.ROLE_USER != role_service.get_role_by_id(db, user.role_id).role:
            raise BadRoleError(
                status_code=403,
                detail="You do not have the rights to access this resource"
            )
        return user
    except jwt.PyJWTError:
        raise InvalidTokenError(
            status_code=401,
            detail="Invalid Token"
        )


def get_current_admin(
    db: Session = Depends(get_db),
    authorization: str = Header(None),
    access_token: str = Cookie(None)
)->User:
    """used to get the currently connected admin"""
    if not authorization and not access_token:
        raise InvalidTokenError(status_code=401, detail="Both Authorization header and cookie are required")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise InvalidTokenError(status_code=401, detail="Invalid Authorization header format")
    try:
        
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise InvalidTokenError(status_code=401, detail="Invalid Authorization header format")

        token_from_header = parts[1]

        payload = jwt.decode(token_from_header, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        email = payload.get("sub")
        if not email:
            raise InvalidTokenError(status_code=401, detail="Invalid Token")

        user = user_service.get_user_by_email(db, email)
        if not user:
            raise UserNotFoundError(status_code=404, detail="User not found")

        if RoleEnum.ROLE_ADMIN != role_service.get_role_by_id(db, user.role_id).role:
            raise BadRoleError(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have the rights to access this ressource"
            )
        return user
    except jwt.PyJWTError:
        raise InvalidTokenError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )


def get_current_super_admin(
    db: Session = Depends(get_db),
    authorization: str = Header(None),
    access_token: str = Cookie(None)
)->User:
    """used to get the currently connected super admin (role super admin)"""
    if not authorization and not access_token:
        raise InvalidTokenError(status_code=401, detail="Both Authorization header and cookie are required")


    try:
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise InvalidTokenError(status_code=401, detail="Invalid Authorization header format")

        token_from_header = parts[1]

        payload = jwt.decode(token_from_header, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        email = payload.get("sub")
        if not email:
            raise InvalidTokenError(status_code=401, detail="Invalid Token")

        user = user_service.get_user_by_email(db, email)
        if not user:
            raise UserNotFoundError(status_code=404, detail="User not found")

        if RoleEnum.ROLE_SUPER_ADMIN != role_service.get_role_by_id(db, user.role_id).role:
            raise BadRoleError(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have the rights to access this ressource"
            )
        return user
    except jwt.PyJWTError:
        raise InvalidTokenError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

def get_super_admin_or_admin(
    db: Session = Depends(get_db),
    authorization: str = Header(None),
    access_token: str = Cookie(None)
)->User:
    """used to get the currently connected admin or super admin"""
    if not authorization and not access_token:
        raise InvalidTokenError(status_code=401, detail="Both Authorization header and cookie are required")

    print(f"TOKEN {authorization}, {access_token}")

    try:
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise InvalidTokenError(status_code=401, detail="Invalid Authorization header format")

        token_from_header = parts[1]
        payload = jwt.decode(token_from_header, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        email = payload.get("sub")
        if not email:
            raise InvalidTokenError(status_code=401, detail="Invalid Token")

        user = user_service.get_user_by_email(db, email)
        if not user:
            raise UserNotFoundError(status_code=404, detail="User not found")

        if role_service.get_role_by_id(db, user.role_id).role not in (RoleEnum.ROLE_SUPER_ADMIN, RoleEnum.ROLE_ADMIN):
            raise BadRoleError(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have the rights to access this ressource"
            )
        return user
    except jwt.PyJWTError:
        raise InvalidTokenError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )


async def refresh_token(db: Session, refresh_token: str = Cookie(None))->JSONResponse:
    """used to refresh the token"""
    if not refresh_token:
        raise NoRefreshTokenError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No refresh token found"
        )

    try:
        payload = jwt.decode(refresh_token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        email = payload.get("sub")
        if email is None:
            raise InvalidTokenError(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token"
            )

        user = user_service.get_user_by_email(db, email)
        if user is None:
            raise UserNotFoundError(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # 🔹 Générer un nouveau access token
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
        )

        response = JSONResponse(content={"access_token": access_token})
        # response.set_cookie("access_token", access_token, httponly=True, secure=True, samesite="Strict")
        response.set_cookie("access_token", access_token, httponly=True, secure=True, samesite="Strict")
        return response

    except jwt.PyJWTError:
        raise InvalidTokenError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Refresh Token"
        )


async def logout() -> JSONResponse:
    """used to logout"""
    response = JSONResponse(content={"msg": "Logout successful"})

    # Supprime les cookies en les expirant
    # response.delete_cookie("access_token", httponly=True, secure=True, samesite="Strict")
    # response.delete_cookie("refresh_token", httponly=True, secure=True, samesite="Strict")
    response.delete_cookie("access_token", httponly=True, secure=True, samesite="Strict")
    response.delete_cookie("refresh_token", httponly=True, secure=True, samesite="Strict")

    return response


def send_mail_for_email_verif(db: Session, user: User) -> None:
    """used to send the email of verification"""

    #profile id = user id by design
    profile = profile_repo.get_profile_by_id(db, user.id)

    user.verification_token = generate_code()
    user.verification_token_sent_at = datetime.now()
    user_repo.commit_user(db)

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("email_verification.html")

    verification_url = f"{HOST}/authent/verify-token?user_email={user.email}&token={user.verification_token}"
    html_content = template.render(
        first_name=profile.first_name,
        token=user.verification_token,
        url=verification_url
    )

    subject = "Vérifiez votre compte !"
    email_service.send_email(html_content, user.email, subject)


def verify_register_token(db: Session, user: User, token: int) -> bool:
    """used to verify the given token with the one in database"""
    if not user.verification_token_sent_at:
        raise VerificationTokenExpiredError(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Aucun token n’a été envoyé."
        )

    if datetime.now() - user.verification_token_sent_at > timedelta(minutes=20):
        raise VerificationTokenExpiredError(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Le délai est dépassé, veuillez renvoyer l'email."
        )

    if user.verification_token != token:
        return False

    user.is_verified = True
    user_repo.commit_user(db)
    return True

def create_reset_password_token(email: str)->str:
    """used to create the jwt to update the password"""
    expires_delta = timedelta(minutes=10)
    return create_access_token(data={"sub": email}, expires_delta=expires_delta)


def send_mail_for_password_reset(db: Session, user: User) -> None:
    """used to send the mail for password resetting"""
    #profile id = user id by design
    profile = profile_repo.get_profile_by_id(db, user.id)

    reset_token = create_reset_password_token(user.email)

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("reset_password.html")

    verification_url = f"{HOST}/authent/reset?t={reset_token}"
    html_content = template.render(
        first_name=profile.first_name,
        token=user.verification_token,
        url=verification_url
    )

    subject = "Réinitialisez votre mot de passe"
    email_service.send_email(html_content, user.email, subject)


def reset_pwd(db: Session, token: str, new_password: str, confirm_password: str)-> bool:
    """used to modify the user's password"""
    try:
        payload = jwt.decode(
            token,
            os.getenv("SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")]
        )
    except Exception:
        raise InvalidTokenError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    email = payload.get("sub")
    if email is None:
        raise InvalidTokenError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    if new_password != confirm_password:
        raise DifferentPasswordsError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Different passwords"
        )
    user = user_service.get_user_by_email(db, email)
    if not user:
        raise UserNotFoundError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    hashed_password = user_service.hash_password(new_password)
    user.password = hashed_password
    user_repo.commit_user(db)
    return True
