from uuid import UUID
from sqlalchemy.orm import Session
from ..models.convo import Convo
from ..repos.convo_repo import ConvoRepo
from ..repos.msg_repo import MsgRepo
from ..schemas.convo import ConvoCreate, ConvoPatch
from ..ai.response import generate_convo

class ConvoService:
    def __init__(self, repo: ConvoRepo, msg_repo: MsgRepo):
        self.repo = repo
        self.msg_repo = msg_repo

    def create_convo(self, user_id: UUID, data: ConvoCreate, db: Session) -> Convo:
        name = generate_convo(data.data)
        return self.repo.create(db, user_id, name)
    
    def create_custom_convo(self, user_id: UUID, data: ConvoCreate, db: Session) -> Convo:
        return self.repo.create(db, user_id, data.data)

    def get_convo(self, convo_id: UUID, db: Session) -> Convo | None:
        return self.repo.get_by_id(db, convo_id)

    def get_convos(self, user_id: UUID, db: Session) -> list[Convo]:
        return self.repo.get_by_user_id(db, user_id)

    def edit_convo(self, user_id: UUID, convo_id: UUID, data: ConvoPatch, db: Session) -> Convo| None:
        convo = self.get_convo(convo_id, db)

        if not convo:
            raise ValueError("Convo not found")
        
        if convo.user_id != user_id:
            raise ValueError("Convo not found")
        
        updates = data.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(convo, field, value)

        return self.repo.save(db, convo)

    def delete_convo(self, user_id: UUID, convo_id: UUID, db: Session):
        convo = self.get_convo(convo_id, db)

        if not convo:
            raise ValueError("Convo not found")
        
        if convo.user_id != user_id:
            raise ValueError("Convo not found")
        
        self.msg_repo.delete_msg_by_convo(db, convo_id)        
        self.repo.delete(db, convo_id)

        return convo