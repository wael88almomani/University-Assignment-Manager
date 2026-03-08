from __future__ import annotations

from sqlalchemy.orm import Session

from app.data.models.course_model import Course
from app.data.models.section_model import Section
from app.repositories.section_repository import SectionRepository


class SectionRepositoryImpl(SectionRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, course_id: int) -> Section:
        section = Section(name=name, course_id=course_id)
        self.db.add(section)
        self.db.commit()
        self.db.refresh(section)
        return section

    def get_by_id(self, section_id: int) -> Section | None:
        return self.db.query(Section).filter(Section.id == section_id).first()

    def list_by_teacher(self, teacher_id: int) -> list[Section]:
        return (
            self.db.query(Section)
            .join(Course, Course.id == Section.course_id)
            .filter(Course.teacher_id == teacher_id)
            .order_by(Section.id.desc())
            .all()
        )

    def belongs_to_teacher(self, section_id: int, teacher_id: int) -> bool:
        return (
            self.db.query(Section)
            .join(Course, Course.id == Section.course_id)
            .filter(Section.id == section_id, Course.teacher_id == teacher_id)
            .first()
            is not None
        )
