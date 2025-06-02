from fastapi import Depends, Cookie, Request, APIRouter, Query
from sqlalchemy.orm import Session
from controllers import authent_controller
from database.db import get_db
from schemas.request_schemas.user_schema import UserAuth
from schemas.response_schemas.user_schema_response import UserResponse
from schemas.request_schemas.register_schema import RegisterSchema
from schemas.request_schemas.reset_password_schema import ResetPasswordSchema
from models.user_model import User

router = APIRouter(
    prefix="/api/v1/authent",
    tags=["authent"],
)

@router.post("/register/user", response_model=UserResponse, status_code=201)
async def register_user(
    user: RegisterSchema,
    db: Session = Depends(get_db)
) -> UserResponse:
    """Register a new regular user."""
    return await authent_controller.register_user(user, db)

@router.post("/register/admin", response_model=UserResponse, status_code=201)
async def register_admin(
    user: RegisterSchema,
    db: Session = Depends(get_db)
) -> UserResponse:
    """Register a new admin user."""
    return await authent_controller.register_admin(user, db)

@router.post("/register/super-admin", response_model=UserResponse, status_code=201)
async def register_super_admin(
    user: RegisterSchema,
    db: Session = Depends(get_db)
) -> UserResponse:
    """Register a new super admin user."""
    return await authent_controller.register_super_admin(user, db)

@router.post("/login")
async def login_for_access_token(
    request: Request,
    user_login: UserAuth,
    db: Session = Depends(get_db)
):
    """Authenticate user and return access/refresh tokens."""
    return await authent_controller.login(request, user_login, db)


@router.post("/verify")
async def verify_jwt(
    user: UserResponse = Depends(authent_controller.verify_jwt)
):
    print(f"USER {user}")
    return user


@router.post("/refresh")
async def refresh_token(refresh_token: str = Cookie(None), db: Session = Depends(get_db)):
    """Refresh access token using a valid refresh token."""
    return await authent_controller.refresh_token(refresh_token, db)

@router.post("/logout")
async def logout(
    current_user: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
):
    """Logout the current user and invalidate tokens."""
    return await authent_controller.logout(db, current_user.id)

@router.post("/verify-token")
async def verify_token(
    db: Session = Depends(get_db),
    user_email: str = Query,
    token: int = Query
):
    """Verify email confirmation token for a user."""
    return authent_controller.verify_register_token(db, user_email, token)

@router.post("/send-token")
async def send_token(
    db: Session = Depends(get_db),
    user_email: str = Query
):
    """Send email confirmation token to the user."""
    return authent_controller.send_token_by_email(db, user_email)

@router.post("/generate-reset")
async def generate_link_to_reset_pwd(
    db: Session = Depends(get_db),
    user_email: str = Query
):
    """Generate and send password reset link to user."""
    return authent_controller.generate_link_reset_password(db, user_email)

@router.post("/reset-pwd")
async def reset_pwd(
    reset_password_schema: ResetPasswordSchema,
    db: Session = Depends(get_db)
):
    """Reset the user's password using provided token and new password."""
    return authent_controller.reset_password(db, reset_password_schema)
