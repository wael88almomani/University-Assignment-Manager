from __future__ import annotations

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.data.models.user_model import User
from app.repositories.user_repository import UserRepository


class UserRepositoryImpl(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, email: str, password: str, role: str) -> User:
        user = User(name=name, email=email, password=password, role=role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def list(self, skip: int, limit: int) -> list[User]:
        return self.db.query(User).order_by(User.id.desc()).offset(skip).limit(limit).all()

    def count(self) -> int:
        return self.db.query(User).count()

    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True

    def list_students(self, search: str, skip: int, limit: int) -> list[User]:
        query = self.db.query(User).filter(User.role == "student")
        if search:
            like = f"%{search.strip()}%"
            query = query.filter(or_(User.name.ilike(like), User.email.ilike(like)))
        return query.order_by(User.id.desc()).offset(skip).limit(limit).all()

    def count_students(self, search: str) -> int:
        query = self.db.query(User).filter(User.role == "student")
        if search:
            like = f"%{search.strip()}%"
            query = query.filter(or_(User.name.ilike(like), User.email.ilike(like)))
        return query.count()
