from __future__ import annotations

from abc import ABC, abstractmethod

from app.data.models.section_model import Section


class SectionRepository(ABC):
    @abstractmethod
    def create(self, name: str, course_id: int) -> Section:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, section_id: int) -> Section | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_teacher(self, teacher_id: int) -> list[Section]:
        raise NotImplementedError

    @abstractmethod
    def belongs_to_teacher(self, section_id: int, teacher_id: int) -> bool:
        raise NotImplementedError
