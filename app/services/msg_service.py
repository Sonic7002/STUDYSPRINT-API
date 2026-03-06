from uuid import UUID
from sqlalchemy.orm import Session
from ..models.msg import Msg
from ..repos.msg_repo import MsgRepo
from ..repos.convo_repo import ConvoRepo
from ..schemas.msg import MsgCreate, MsgRole, MsgDelete
from ..ai.response import generate_response

class MsgService:
    def __init__(self, msg_repo: MsgRepo, convo_repo: ConvoRepo):
        self.msg_repo = msg_repo
        self.convo_repo = convo_repo

    def create_msg(self, user_id: UUID, convo_id: UUID, data: MsgCreate, db: Session) -> Msg:
        convo = self.convo_repo.get_by_id(db, convo_id)
        if not convo or convo.user_id != user_id:
            raise ValueError("Invalid convo id")
        if not data.role == MsgRole.USER:
            raise ValueError("Invalid Role")
        self.msg_repo.create(db, user_id, convo_id, data)

        last_5_msgs = self.get_5_msgs(user_id, convo_id, db)
        response = generate_response(last_5_msgs)
        return self.msg_repo.create(db, user_id, convo_id, response)

    def get_msgs(self, user_id: UUID, convo_id: UUID, db: Session) -> list[Msg]:
        convo = self.convo_repo.get_by_id(db, convo_id)
        if not convo or convo.user_id != user_id:
            raise ValueError("Invalid convo id")
        return self.msg_repo.get_by_convo_id(db, convo_id)

    def get_5_msgs(self, user_id: UUID, convo_id: UUID, db: Session) -> list[Msg]:
        convo = self.convo_repo.get_by_id(db, convo_id)
        if not convo or convo.user_id != user_id:
            raise ValueError("Invalid convo id")
        return self.msg_repo.get_by_convo_id(db, convo_id)
    
    def delete_msg(self, user_id: UUID, data: MsgDelete, db: Session) -> int:
        msg = self.msg_repo.get_msg(db, data.convo_id, data.msg_id)
        if msg is None or msg.user_id != str(user_id):
            raise ValueError("Messege not found")
        
        return self.msg_repo.delete_msg(db, data.convo_id, msg)
