from __future__ import annotations

from abc import ABC, abstractmethod

from app.data.models.enrollment_model import Enrollment


class EnrollmentRepository(ABC):
    @abstractmethod
    def create(self, student_id: int, section_id: int) -> Enrollment:
        raise NotImplementedError

    @abstractmethod
    def is_enrolled(self, student_id: int, section_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def list_section_ids_by_student(self, student_id: int) -> list[int]:
        raise NotImplementedError

    @abstractmethod
    def list_student_ids_by_section(self, section_id: int) -> list[int]:
        raise NotImplementedError
