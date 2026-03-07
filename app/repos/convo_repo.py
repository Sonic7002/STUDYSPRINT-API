from uuid import UUID
from sqlalchemy.orm import Session
from ..models.convo import Convo
from ..schemas.convo import ConvoCreate

class ConvoRepo:
    def create(self, db: Session, user_id: UUID, name: str) -> Convo | None:
        convo = Convo(name = name, user_id = user_id)
        db.add(convo)
        db.commit()
        db.refresh(convo)
        return convo

    def get_by_id(self, db: Session, convo_id: UUID) ->  Convo | None:
        return db.query(Convo).filter(Convo.id == convo_id).first()

    def get_by_user_id(self, db: Session, user_id: UUID) -> list[Convo]:
        return db.query(Convo).filter(Convo.user_id == user_id).all()

    def save(self, db: Session, convo: Convo) -> Convo:
        db.commit()
        db.refresh(convo)
        return convo

    def delete(self, db: Session, convo_id: UUID):
        convo = self.get_by_id(db, convo_id)
        db.delete(convo)
        db.commit()
        return convo