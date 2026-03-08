from fastapi import HTTPException, status

from app.core.security import create_access_token, get_password_hash, verify_password
from app.repositories.user_repository import UserRepository


class AuthUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, name: str, email: str, password: str, role: str):
        existing_user = self.user_repository.get_by_email(email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        if role not in {"admin", "teacher", "student"}:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")
        hashed_password = get_password_hash(password)
        return self.user_repository.create(name=name, email=email, password=hashed_password, role=role)

    def login(self, email: str, password: str) -> str:
        user = self.user_repository.get_by_email(email)
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return create_access_token(subject=user.id, role=user.role)
