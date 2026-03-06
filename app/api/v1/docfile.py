from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from uuid import UUID
from ...db.session import get_db
from ...schemas.docfile import FileRead
from ...services.docfile_service import FileService
from ..dependencies.deps import get_file_service
from ..dependencies.auth_deps import get_current_user
from ...models.user import User

router = APIRouter(prefix="/files", tags=["files"])

@router.post("/", response_model=FileRead)
def upload_file(file: UploadFile = File(...), current_user: User = Depends(get_current_user), service: FileService = Depends(get_file_service), db: Session = Depends(get_db)):
    try:
        return service.create_file(current_user.id, file, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=list[FileRead])
def get_all_files(current_user: User = Depends(get_current_user), service: FileService = Depends(get_file_service), db: Session = Depends(get_db)):
    return service.get_files(current_user.id, db)

@router.get("/{file_id}")
def download_file(file_id: UUID, current_user: User = Depends(get_current_user), service: FileService = Depends(get_file_service), db: Session = Depends(get_db)):
    try:
        return service.return_file(current_user.id, file_id, db)
    except ValueError:
        raise HTTPException(status_code=404, detail="File not found")

@router.delete("/{file_id}", response_model=FileRead)
def delete_convo(file_id: UUID, current_user: User = Depends(get_current_user), service: FileService = Depends(get_file_service), db: Session = Depends(get_db)):
    try:
        doc = service.delete_file(current_user.id, file_id, db)
    except ValueError:
        raise HTTPException(status_code=404, detail="Invalid file ID")
    return doc
