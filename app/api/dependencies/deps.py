from ...repos.user_repo import UserRepo
from ...repos.convo_repo import ConvoRepo
from ...repos.msg_repo import MsgRepo
from ...repos.docfile_repo import FileRepo
from ...services.user_service import UserService
from ...services.convo_service import ConvoService
from ...services.msg_service import MsgService
from ...services.docfile_service import FileService
user_repo = UserRepo()
convo_repo = ConvoRepo()
msg_repo = MsgRepo()
file_repo = FileRepo()

def get_user_service() -> UserService:
    return UserService(user_repo)

def get_convo_service() -> ConvoService:
    return ConvoService(convo_repo, msg_repo)

def get_msg_service() -> MsgService:
    return MsgService(msg_repo, convo_repo, file_repo)

def get_file_service() -> FileService:
    return FileService(file_repo)