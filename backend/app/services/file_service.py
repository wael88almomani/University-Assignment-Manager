import os
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.core.config import settings


class FileService:
    allowed_extensions = {".pdf", ".docx"}

    def __init__(self) -> None:
        Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)

    def save_submission_file(self, upload_file: UploadFile) -> str:
        extension = Path(upload_file.filename or "").suffix.lower()
        if extension not in self.allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF and DOCX files are allowed",
            )
        unique_name = f"{uuid.uuid4().hex}{extension}"
        full_path = Path(settings.upload_dir) / unique_name
        with open(full_path, "wb") as output:
            output.write(upload_file.file.read())
        return os.fspath(full_path)
