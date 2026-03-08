from __future__ import annotations

from abc import ABC, abstractmethod

from app.data.models.submission_model import Submission


class SubmissionRepository(ABC):
    @abstractmethod
    def create(self, assignment_id: int, student_id: int, file_path: str) -> Submission:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, submission_id: int) -> Submission | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_assignment_and_student(self, assignment_id: int, student_id: int) -> Submission | None:
        raise NotImplementedError

    @abstractmethod
    def list(self, skip: int, limit: int, search: str = "", status: str = "all", sort: str = "newest") -> list[Submission]:
        raise NotImplementedError

    @abstractmethod
    def list_by_assignment(self, assignment_id: int, skip: int, limit: int) -> list[Submission]:
        raise NotImplementedError

    @abstractmethod
    def list_by_student(self, student_id: int, skip: int, limit: int, search: str = "", status: str = "all", sort: str = "newest") -> list[Submission]:
        raise NotImplementedError

    @abstractmethod
    def list_by_teacher(
        self,
        teacher_id: int,
        skip: int,
        limit: int,
        search: str = "",
        status: str = "all",
        sort: str = "newest",
    ) -> list[Submission]:
        raise NotImplementedError

    @abstractmethod
    def count(self, search: str = "", status: str = "all") -> int:
        raise NotImplementedError

    @abstractmethod
    def count_by_assignment(self, assignment_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def count_by_student(self, student_id: int, search: str = "", status: str = "all") -> int:
        raise NotImplementedError

    @abstractmethod
    def count_by_teacher(self, teacher_id: int, search: str = "", status: str = "all") -> int:
        raise NotImplementedError

    @abstractmethod
    def update_file(self, submission: Submission, file_path: str) -> Submission:
        raise NotImplementedError

    @abstractmethod
    def grade(self, submission: Submission, grade: float, feedback: str | None) -> Submission:
        raise NotImplementedError
