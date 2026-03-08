from __future__ import annotations

from sqlalchemy.orm import Session, joinedload

from app.data.models.submission_model import Submission
from app.data.models.assignment_model import Assignment
from app.repositories.submission_repository import SubmissionRepository


class SubmissionRepositoryImpl(SubmissionRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, assignment_id: int, student_id: int, file_path: str) -> Submission:
        submission = Submission(assignment_id=assignment_id, student_id=student_id, file_path=file_path)
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        return submission

    def get_by_id(self, submission_id: int) -> Submission | None:
        return self.db.query(Submission).filter(Submission.id == submission_id).first()

    def get_by_assignment_and_student(self, assignment_id: int, student_id: int) -> Submission | None:
        return (
            self.db.query(Submission)
            .filter(Submission.assignment_id == assignment_id, Submission.student_id == student_id)
            .first()
        )

    def list(self, skip: int, limit: int, search: str = "", status: str = "all", sort: str = "newest") -> list[Submission]:
        query = self.db.query(Submission).options(joinedload(Submission.assignment))
        
        # Apply search filter
        if search:
            query = query.join(Assignment).filter(Assignment.title.ilike(f"%{search}%"))
        
        # Apply status filter
        if status == "graded":
            query = query.filter(Submission.grade != None)
        elif status == "pending":
            query = query.filter(Submission.grade == None)
        
        # Apply sorting
        if sort == "newest":
            query = query.order_by(Submission.submitted_at.desc())
        elif sort == "oldest":
            query = query.order_by(Submission.submitted_at.asc())
        elif sort == "grade_high":
            query = query.order_by(Submission.grade.desc().nullslast())
        elif sort == "grade_low":
            query = query.order_by(Submission.grade.asc().nullslast())
        else:
            query = query.order_by(Submission.id.desc())
        
        return query.offset(skip).limit(limit).all()

    def list_by_assignment(self, assignment_id: int, skip: int, limit: int) -> list[Submission]:
        return (
            self.db.query(Submission)
            .filter(Submission.assignment_id == assignment_id)
            .order_by(Submission.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def list_by_student(self, student_id: int, skip: int, limit: int, search: str = "", status: str = "all", sort: str = "newest") -> list[Submission]:
        query = self.db.query(Submission).options(joinedload(Submission.assignment)).filter(Submission.student_id == student_id)
        
        # Apply search filter
        if search:
            query = query.join(Assignment).filter(Assignment.title.ilike(f"%{search}%"))
        
        # Apply status filter
        if status == "graded":
            query = query.filter(Submission.grade != None)
        elif status == "pending":
            query = query.filter(Submission.grade == None)
        
        # Apply sorting
        if sort == "newest":
            query = query.order_by(Submission.submitted_at.desc())
        elif sort == "oldest":
            query = query.order_by(Submission.submitted_at.asc())
        elif sort == "grade_high":
            query = query.order_by(Submission.grade.desc().nullslast())
        elif sort == "grade_low":
            query = query.order_by(Submission.grade.asc().nullslast())
        else:
            query = query.order_by(Submission.id.desc())
        
        return query.offset(skip).limit(limit).all()

    def list_by_teacher(
        self,
        teacher_id: int,
        skip: int,
        limit: int,
        search: str = "",
        status: str = "all",
        sort: str = "newest",
    ) -> list[Submission]:
        query = (
            self.db.query(Submission)
            .join(Assignment, Assignment.id == Submission.assignment_id)
            .options(joinedload(Submission.assignment))
            .filter(Assignment.teacher_id == teacher_id)
        )

        if search:
            query = query.filter(Assignment.title.ilike(f"%{search}%"))

        if status == "graded":
            query = query.filter(Submission.grade != None)
        elif status == "pending":
            query = query.filter(Submission.grade == None)

        if sort == "newest":
            query = query.order_by(Submission.submitted_at.desc())
        elif sort == "oldest":
            query = query.order_by(Submission.submitted_at.asc())
        elif sort == "grade_high":
            query = query.order_by(Submission.grade.desc().nullslast())
        elif sort == "grade_low":
            query = query.order_by(Submission.grade.asc().nullslast())
        else:
            query = query.order_by(Submission.id.desc())

        return query.offset(skip).limit(limit).all()

    def count(self, search: str = "", status: str = "all") -> int:
        query = self.db.query(Submission)
        
        # Apply search filter
        if search:
            query = query.join(Assignment).filter(Assignment.title.ilike(f"%{search}%"))
        
        # Apply status filter
        if status == "graded":
            query = query.filter(Submission.grade != None)
        elif status == "pending":
            query = query.filter(Submission.grade == None)
        
        return query.count()

    def count_by_assignment(self, assignment_id: int) -> int:
        return self.db.query(Submission).filter(Submission.assignment_id == assignment_id).count()

    def count_by_student(self, student_id: int, search: str = "", status: str = "all") -> int:
        query = self.db.query(Submission).filter(Submission.student_id == student_id)
        
        # Apply search filter
        if search:
            query = query.join(Assignment).filter(Assignment.title.ilike(f"%{search}%"))
        
        # Apply status filter
        if status == "graded":
            query = query.filter(Submission.grade != None)
        elif status == "pending":
            query = query.filter(Submission.grade == None)
        
        return query.count()

    def count_by_teacher(self, teacher_id: int, search: str = "", status: str = "all") -> int:
        query = (
            self.db.query(Submission)
            .join(Assignment, Assignment.id == Submission.assignment_id)
            .filter(Assignment.teacher_id == teacher_id)
        )

        if search:
            query = query.filter(Assignment.title.ilike(f"%{search}%"))

        if status == "graded":
            query = query.filter(Submission.grade != None)
        elif status == "pending":
            query = query.filter(Submission.grade == None)

        return query.count()

    def update_file(self, submission: Submission, file_path: str) -> Submission:
        submission.file_path = file_path
        self.db.commit()
        self.db.refresh(submission)
        return submission

    def grade(self, submission: Submission, grade: float, feedback: str | None) -> Submission:
        submission.grade = grade
        submission.feedback = feedback
        self.db.commit()
        self.db.refresh(submission)
        return submission
