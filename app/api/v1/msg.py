from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from ...db.session import get_db
from ...schemas.msg import MsgCreate, MsgRead, MsgDelete
from ...schemas.docfile import FileGen
from ...services.msg_service import MsgService
from ..dependencies.deps import get_msg_service
from ...api.dependencies.auth_deps import get_current_user
from ...models.user import User

router = APIRouter(prefix="/msgs", tags=["msgs"])

@router.post("/focus/{convo_id}", response_model=MsgRead)
def create_focused_msg(data: MsgCreate, convo_id: UUID, current_user: User = Depends(get_current_user), service: MsgService = Depends(get_msg_service), db: Session = Depends(get_db)):
    try:
        return service.create_locked_msg(current_user.id, convo_id, data, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/notes")
def generate_notes(data: FileGen, current_user: User = Depends(get_current_user), service: MsgService = Depends(get_msg_service), db: Session = Depends(get_db)):
    try:
        return service.create_notes(current_user.id, data.convo_id, data.file_id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/quiz")
def generate_quiz(data: FileGen, current_user: User = Depends(get_current_user), service: MsgService = Depends(get_msg_service), db: Session = Depends(get_db)):
    try:
        return service.create_quiz(current_user.id, data.convo_id, data.file_id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{convo_id}", response_model=MsgRead)
def create_msg(data: MsgCreate, convo_id: UUID, current_user: User = Depends(get_current_user), service: MsgService = Depends(get_msg_service), db: Session = Depends(get_db)):
    try:
        return service.create_msg(current_user.id, convo_id, data, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[MsgRead])
def get_all_msgs(convo_id: UUID, current_user: User = Depends(get_current_user), service: MsgService = Depends(get_msg_service), db: Session = Depends(get_db)):
    try:
        return service.get_msgs(current_user.id, convo_id, db)
    except ValueError:
        raise HTTPException(status_code=404, detail="Invalid convo ID")

@router.delete("/delete")
def delete_msg(data: MsgDelete, current_user: User = Depends(get_current_user), service: MsgService = Depends(get_msg_service), db: Session = Depends(get_db)):
    try:
        return service.delete_msg(current_user.id, data, db)
    except ValueError:
        raise HTTPException(status_code=404, detail="Invalid convo or msg ID")