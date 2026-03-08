from __future__ import annotations

from abc import ABC, abstractmethod

from app.data.models.assignment_model import Assignment


class AssignmentRepository(ABC):
    @abstractmethod
    def create(
        self,
        title: str,
        description: str,
        due_date,
        teacher_id: int,
        section_id: int | None = None,
    ) -> Assignment:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, assignment_id: int) -> Assignment | None:
        raise NotImplementedError

    @abstractmethod
    def list(self, skip: int, limit: int, search: str = "", status: str = "all", sort: str = "due_soonest") -> list[Assignment]:
        raise NotImplementedError

    @abstractmethod
    def count(self, search: str = "", status: str = "all") -> int:
        raise NotImplementedError

    @abstractmethod
    def list_by_teacher(
        self,
        teacher_id: int,
        skip: int,
        limit: int,
        search: str = "",
        status: str = "all",
        sort: str = "due_soonest",
    ) -> list[Assignment]:
        raise NotImplementedError

    @abstractmethod
    def count_by_teacher(self, teacher_id: int, search: str = "", status: str = "all") -> int:
        raise NotImplementedError

    @abstractmethod
    def list_by_student_sections(
        self,
        section_ids: list[int],
        skip: int,
        limit: int,
        search: str = "",
        status: str = "all",
        sort: str = "due_soonest",
    ) -> list[Assignment]:
        raise NotImplementedError

    @abstractmethod
    def count_by_student_sections(self, section_ids: list[int], search: str = "", status: str = "all") -> int:
        raise NotImplementedError

    @abstractmethod
    def update(self, assignment: Assignment, title: str, description: str, due_date) -> Assignment:
        raise NotImplementedError

    @abstractmethod
    def delete(self, assignment_id: int) -> bool:
        raise NotImplementedError
