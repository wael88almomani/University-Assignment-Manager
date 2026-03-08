from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.repositories.assignment_repository import AssignmentRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.submission_repository import SubmissionRepository


class SubmissionUseCase:
    def __init__(
        self,
        submission_repository: SubmissionRepository,
        assignment_repository: AssignmentRepository,
        enrollment_repository: EnrollmentRepository,
    ):
        self.submission_repository = submission_repository
        self.assignment_repository = assignment_repository
        self.enrollment_repository = enrollment_repository

    def create_or_update_submission(self, assignment_id: int, student_id: int, file_path: str):
        assignment = self.assignment_repository.get_by_id(assignment_id)
        if not assignment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
        if assignment.section_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assignment is not assigned to a section")
        if not self.enrollment_repository.is_enrolled(student_id=student_id, section_id=assignment.section_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enrolled in assignment section")
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        due_date = assignment.due_date.astimezone(timezone.utc).replace(tzinfo=None) if assignment.due_date.tzinfo else assignment.due_date
        if due_date < now:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Deadline has passed")

        existing_submission = self.submission_repository.get_by_assignment_and_student(assignment_id, student_id)
        if existing_submission:
            return self.submission_repository.update_file(existing_submission, file_path)
        return self.submission_repository.create(assignment_id=assignment_id, student_id=student_id, file_path=file_path)

    def update_submission_before_deadline(self, submission_id: int, student_id: int, file_path: str):
        submission = self.submission_repository.get_by_id(submission_id)
        if not submission:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
        if submission.student_id != student_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

        assignment = self.assignment_repository.get_by_id(submission.assignment_id)
        if not assignment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        due_date = assignment.due_date.astimezone(timezone.utc).replace(tzinfo=None) if assignment.due_date.tzinfo else assignment.due_date
        if due_date < now:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Deadline has passed")

        return self.submission_repository.update_file(submission, file_path)

    def grade_submission(self, submission_id: int, grade: float, feedback: str | None, teacher_id: int):
        submission = self.submission_repository.get_by_id(submission_id)
        if not submission:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
        assignment = self.assignment_repository.get_by_id(submission.assignment_id)
        if not assignment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
        if assignment.teacher_id != teacher_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        return self.submission_repository.grade(submission, grade=grade, feedback=feedback)
