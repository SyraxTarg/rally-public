from fastapi import Depends, APIRouter, UploadFile, File

from controllers import authent_controller
from models.user_model import User
from controllers import pictures_controller

router = APIRouter(
    prefix="/api/v1/pictures",
    tags=["pictures"],
)

@router.post("/", response_model=dict[str, str], status_code=200)
async def upload_picture(
    file: UploadFile = File(...),
    _: User = Depends(authent_controller.get_connected_user)
) -> dict[str, str]:
    """Remove a like from an event for the current user."""
    return await pictures_controller.upload_image(file)

