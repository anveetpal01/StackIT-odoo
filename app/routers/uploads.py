from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from uuid import uuid4

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/uploads", tags=["uploads"])

@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    if ext.lower() not in [".jpg", ".jpeg", ".png", ".gif"]:
        raise HTTPException(status_code=400, detail="Invalid image format")
    filename = f"{uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"url": f"/uploads/{filename}"}
