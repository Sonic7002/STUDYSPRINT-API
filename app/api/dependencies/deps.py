from ...repos.user_repo import UserRepo
from ...repos.convo_repo import ConvoRepo
from ...repos.msg_repo import MsgRepo
from ...services.user_service import UserService
from ...services.convo_service import ConvoService
from ...services.msg_service import MsgService
user_repo = UserRepo()
convo_repo = ConvoRepo()
msg_repo = MsgRepo()

def get_user_service() -> UserService:
    return UserService(user_repo)

def get_convo_service() -> ConvoService:
    return ConvoService(convo_repo, msg_repo)

def get_msg_service() -> MsgService:
    return MsgService(msg_repo, convo_repo)