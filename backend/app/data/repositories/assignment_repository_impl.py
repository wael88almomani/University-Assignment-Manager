from __future__ import annotations

from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.data.models.assignment_model import Assignment
from app.repositories.assignment_repository import AssignmentRepository


class AssignmentRepositoryImpl(AssignmentRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        title: str,
        description: str,
        due_date: datetime,
        teacher_id: int,
        section_id: int | None = None,
    ) -> Assignment:
        assignment = Assignment(
            title=title,
            description=description,
            due_date=due_date,
            teacher_id=teacher_id,
            section_id=section_id,
        )
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def get_by_id(self, assignment_id: int) -> Assignment | None:
        return self.db.query(Assignment).filter(Assignment.id == assignment_id).first()

    def list(self, skip: int, limit: int, search: str = "", status: str = "all", sort: str = "due_soonest") -> list[Assignment]:
        query = self.db.query(Assignment)
        return self._apply_common_filters(query, search=search, status=status, sort=sort).offset(skip).limit(limit).all()

    def list_by_teacher(
        self,
        teacher_id: int,
        skip: int,
        limit: int,
        search: str = "",
        status: str = "all",
        sort: str = "due_soonest",
    ) -> list[Assignment]:
        query = self.db.query(Assignment).filter(Assignment.teacher_id == teacher_id)
        return self._apply_common_filters(query, search=search, status=status, sort=sort).offset(skip).limit(limit).all()

    def list_by_student_sections(
        self,
        section_ids: list[int],
        skip: int,
        limit: int,
        search: str = "",
        status: str = "all",
        sort: str = "due_soonest",
    ) -> list[Assignment]:
        if not section_ids:
            return []
        query = self.db.query(Assignment).filter(Assignment.section_id.in_(section_ids))
        return self._apply_common_filters(query, search=search, status=status, sort=sort).offset(skip).limit(limit).all()

    def _apply_common_filters(self, query, search: str, status: str, sort: str):
        
        # Apply search filter
        if search:
            query = query.filter(
                or_(
                    Assignment.title.ilike(f"%{search}%"),
                    Assignment.description.ilike(f"%{search}%")
                )
            )
        
        # Apply status filter
        now = datetime.utcnow()
        if status == "upcoming":
            query = query.filter(Assignment.due_date >= now)
        elif status == "overdue":
            query = query.filter(Assignment.due_date < now)
        
        # Apply sorting
        if sort == "due_soonest":
            query = query.order_by(Assignment.due_date.asc())
        elif sort == "due_latest":
            query = query.order_by(Assignment.due_date.desc())
        elif sort == "title_asc":
            query = query.order_by(Assignment.title.asc())
        elif sort == "title_desc":
            query = query.order_by(Assignment.title.desc())
        else:
            query = query.order_by(Assignment.id.desc())
        
        return query

    def count(self, search: str = "", status: str = "all") -> int:
        query = self.db.query(Assignment)
        return self._apply_common_count_filters(query, search=search, status=status).count()

    def count_by_teacher(self, teacher_id: int, search: str = "", status: str = "all") -> int:
        query = self.db.query(Assignment).filter(Assignment.teacher_id == teacher_id)
        return self._apply_common_count_filters(query, search=search, status=status).count()

    def count_by_student_sections(self, section_ids: list[int], search: str = "", status: str = "all") -> int:
        if not section_ids:
            return 0
        query = self.db.query(Assignment).filter(Assignment.section_id.in_(section_ids))
        return self._apply_common_count_filters(query, search=search, status=status).count()

    def _apply_common_count_filters(self, query, search: str, status: str):
        
        # Apply search filter
        if search:
            query = query.filter(
                or_(
                    Assignment.title.ilike(f"%{search}%"),
                    Assignment.description.ilike(f"%{search}%")
                )
            )
        
        # Apply status filter
        now = datetime.utcnow()
        if status == "upcoming":
            query = query.filter(Assignment.due_date >= now)
        elif status == "overdue":
            query = query.filter(Assignment.due_date < now)
        
        return query

    def update(self, assignment: Assignment, title: str, description: str, due_date: datetime) -> Assignment:
        assignment.title = title
        assignment.description = description
        assignment.due_date = due_date
        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def delete(self, assignment_id: int) -> bool:
        assignment = self.get_by_id(assignment_id)
        if not assignment:
            return False
        self.db.delete(assignment)
        self.db.commit()
        return True
