from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from ...db.session import get_db
from ...schemas.convo import ConvoCreate, ConvoPatch, ConvoRead
from ...services.convo_service import ConvoService
from ..dependencies.deps import get_convo_service
from ...api.dependencies.auth_deps import get_current_user
from ...models.user import User

router = APIRouter(prefix="/convos", tags=["convos"])

@router.post("/", response_model=ConvoRead)
def create_convo(data: ConvoCreate, current_user: User = Depends(get_current_user), service: ConvoService = Depends(get_convo_service), db: Session = Depends(get_db)):
    return service.create_convo(current_user.id, data, db)

@router.get("/", response_model=list[ConvoRead])
def get_all_convos(current_user: User = Depends(get_current_user), service: ConvoService = Depends(get_convo_service), db: Session = Depends(get_db)):
    return service.get_convos(current_user.id, db)

@router.patch("/{convo_id}", response_model=ConvoRead)
def edit_convo(convo_id: UUID, data: ConvoPatch, current_user: User = Depends(get_current_user), service: ConvoService = Depends(get_convo_service), db: Session = Depends(get_db)):
    try:
        convo = service.edit_convo(current_user.id, convo_id, data, db)
    except ValueError:
        raise HTTPException(status_code=404, detail="Invalid convo ID")
    return convo

@router.delete("/{convo_id}", response_model=ConvoRead)
def delete_convo(convo_id: UUID, current_user: User = Depends(get_current_user), service: ConvoService = Depends(get_convo_service), db: Session = Depends(get_db)):
    try:
        convo = service.delete_convo(current_user.id, convo_id, db)
    except ValueError:
        raise HTTPException(status_code=404, detail="Invalid convo ID")
    return convo