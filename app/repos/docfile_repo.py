from uuid import UUID
from sqlalchemy.orm import Session
from ..models.docfile import File
from ..schemas.docfile import FileRead

class FileRepo:
    def create(self, db: Session, user_id: UUID, name: str) -> File | None: 
        doc = File(name = name, user_id = user_id)
        db.add(doc)
        db.flush()
        return doc

    def get_by_id(self, db: Session, file_id: UUID) ->  File | None:
        return db.query(File).filter(File.id == str(file_id)).first()

    def get_by_user_id(self, db: Session, user_id: UUID) -> list[File]:
        return db.query(File).filter(File.user_id == str(user_id)).all()
    
    def save(self, db: Session, doc: File) -> File:
        db.commit()
        db.refresh(doc)
        return doc
    
    def delete(self, db: Session, file_id: UUID):
        doc = self.get_by_id(db, file_id)
        db.delete(doc)
        db.commit()
        return doc