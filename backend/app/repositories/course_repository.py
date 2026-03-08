from __future__ import annotations

from abc import ABC, abstractmethod

from app.data.models.course_model import Course


class CourseRepository(ABC):
    @abstractmethod
    def create(self, name: str, code: str, teacher_id: int) -> Course:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, course_id: int) -> Course | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_teacher(self, teacher_id: int) -> list[Course]:
        raise NotImplementedError
