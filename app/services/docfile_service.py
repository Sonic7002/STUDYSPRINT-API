from uuid import UUID
from sqlalchemy.orm import Session
from ..models.docfile import File
from ..repos.docfile_repo import FileRepo
from ..schemas.docfile import FileRead
from shutil import copyfileobj
from pathlib import Path
from fastapi import UploadFile
from fastapi.responses import FileResponse

class FileService:
    def __init__(self, repo: FileRepo):
        self.repo = repo
        self.UPLOAD_DIR = Path("files")

    def create_file(self, user_id: UUID, data: UploadFile, db: Session) -> File:
        try:
            self.UPLOAD_DIR.mkdir(exist_ok=True)

            if data.content_type != "application/pdf":
                raise ValueError("Only PDF files are allowed")
            if Path(data.filename).suffix.lower() != ".pdf":
                raise ValueError("Invalid file extension")
            if data.size and data.size > 10 * 1024 * 1024:
                raise ValueError("File too large (max 10MB)")
        
            doc = self.repo.create(db, user_id, data.filename)
            file_path = self.UPLOAD_DIR / f"{doc.id}.pdf"

            with file_path.open("wb") as buffer:
                copyfileobj(data.file, buffer)

        except Exception as e:
            raise ValueError(f"File upload failed: {e}")

        return self.repo.save(db, doc)

    def get_file(self, file_id: UUID, db: Session) -> File | None:
        return self.repo.get_by_id(db, file_id)
    
    def return_file(self, user_id: UUID, file_id: UUID, db: Session) -> FileResponse:
        doc = self.get_file(file_id, db)

        if not doc:
            raise ValueError("file not found")
        
        if doc.user_id != str(user_id):
            raise ValueError("file not found")
        
        file_path = (self.UPLOAD_DIR / f"{file_id}.pdf").resolve()

        if not file_path.exists():
            raise ValueError("File not found")

        return FileResponse(path=file_path, filename=doc.name, media_type="application/octet-stream")

    def get_files(self, user_id: UUID, db: Session) -> list[File]:
        return self.repo.get_by_user_id(db, user_id)
    
    def delete_file(self, user_id: UUID, file_id: UUID, db: Session):
        doc = self.get_file(file_id, db)

        if not doc:
            raise ValueError("file not found")
        
        if doc.user_id != str(user_id):
            raise ValueError("file not found")
        
        file_path = self.UPLOAD_DIR / f"{doc.id}.pdf"
        if not file_path.exists():
            raise ValueError("File not found")

        file_path.unlink()

        self.repo.delete(db, file_id)
        return doc
