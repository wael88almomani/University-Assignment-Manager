from __future__ import annotations

from sqlalchemy.orm import Session

from app.data.models.course_model import Course
from app.repositories.course_repository import CourseRepository


class CourseRepositoryImpl(CourseRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, code: str, teacher_id: int) -> Course:
        course = Course(name=name, code=code, teacher_id=teacher_id)
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        return course

    def get_by_id(self, course_id: int) -> Course | None:
        return self.db.query(Course).filter(Course.id == course_id).first()

    def list_by_teacher(self, teacher_id: int) -> list[Course]:
        return self.db.query(Course).filter(Course.teacher_id == teacher_id).order_by(Course.id.desc()).all()
