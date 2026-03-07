from uuid import UUID
from sqlalchemy.orm import Session
from ..models.docfile import File
from ..repos.docfile_repo import FileRepo
from shutil import copyfileobj
from pathlib import Path
from fastapi import UploadFile
from fastapi.responses import FileResponse
from ..db.file_client import supabase

class FileService:
    def __init__(self, repo: FileRepo):
        self.repo = repo

    def create_file(self, user_id: UUID, data: UploadFile, db: Session) -> File:
        try:

            if data.content_type != "application/pdf":
                raise ValueError("Only PDF files are allowed")
            if Path(data.filename).suffix.lower() != ".pdf":
                raise ValueError("Invalid file extension")
            if data.size and data.size > 10 * 1024 * 1024:
                raise ValueError("File too large (max 10MB)")
        
            doc = self.repo.create(db, user_id, data.filename)
            try:
                storage_key = f"{doc.id}.pdf"
                file_bytes = data.file.read()
                supabase.storage.from_("studysprint").upload(storage_key, file_bytes, {"content-type": "application/pdf"})
            except Exception as e:
                raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"File upload failed: {e}")
        return self.repo.save(db, doc)
        
    def get_file(self, file_id: UUID, db: Session) -> File | None:
        return self.repo.get_by_id(db, file_id)
    
    def return_file(self, user_id: UUID, file_id: UUID, db: Session) -> dict:
        doc = self.get_file(file_id, db)

        if not doc:
            raise ValueError("file not found")
        
        if doc.user_id != user_id:
            raise ValueError("file not found")
        
        try:
            storage_key = f"{doc.id}.pdf"
            resp = supabase.storage.from_("studysprint").get_public_url(storage_key)
        except Exception as e:
            raise ValueError(str(e))

        return {
            "file id": doc.id,
            "file name": doc.name,
            "file url": resp
        }

    def get_files(self, user_id: UUID, db: Session) -> list[File]:
        return self.repo.get_by_user_id(db, user_id)
    
    def delete_file(self, user_id: UUID, file_id: UUID, db: Session):
        doc = self.get_file(file_id, db)

        if not doc:
            raise ValueError("file not found")
        
        if doc.user_id != user_id:
            raise ValueError("file not found")

        storage_key = f"{doc.id}.pdf"
        supabase.storage.from_("studysprint").remove([storage_key])

        self.repo.delete(db, file_id)
        return doc
