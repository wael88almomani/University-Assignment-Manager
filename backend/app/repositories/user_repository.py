from __future__ import annotations

from abc import ABC, abstractmethod

from app.data.models.user_model import User


class UserRepository(ABC):
    @abstractmethod
    def create(self, name: str, email: str, password: str, role: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def list(self, skip: int, limit: int) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def list_students(self, search: str, skip: int, limit: int) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    def count_students(self, search: str) -> int:
        raise NotImplementedError
