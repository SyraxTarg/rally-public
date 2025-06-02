from fastapi import UploadFile, File, HTTPException
from services import pictures_service

async def upload_image(file: UploadFile = File(...)):
    try:
        # Utilise le .file pour obtenir un fichier compatible avec requests
        response = pictures_service.upload_to_cloudinary(file.file)
        return {
            "url": response["secure_url"],
            "public_id": response["public_id"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
