from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.data.models.enrollment_model import Enrollment
from app.repositories.enrollment_repository import EnrollmentRepository


class EnrollmentRepositoryImpl(EnrollmentRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, student_id: int, section_id: int) -> Enrollment:
        enrollment = Enrollment(student_id=student_id, section_id=section_id)
        self.db.add(enrollment)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            existing = (
                self.db.query(Enrollment)
                .filter(Enrollment.student_id == student_id, Enrollment.section_id == section_id)
                .first()
            )
            if existing:
                return existing
            raise
        self.db.refresh(enrollment)
        return enrollment

    def is_enrolled(self, student_id: int, section_id: int) -> bool:
        return (
            self.db.query(Enrollment)
            .filter(Enrollment.student_id == student_id, Enrollment.section_id == section_id)
            .first()
            is not None
        )

    def list_section_ids_by_student(self, student_id: int) -> list[int]:
        rows = self.db.query(Enrollment.section_id).filter(Enrollment.student_id == student_id).all()
        return [row[0] for row in rows]

    def list_student_ids_by_section(self, section_id: int) -> list[int]:
        rows = self.db.query(Enrollment.student_id).filter(Enrollment.section_id == section_id).all()
        return [row[0] for row in rows]
