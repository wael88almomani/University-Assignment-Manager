from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.repositories.assignment_repository import AssignmentRepository


class AssignmentUseCase:
    def __init__(self, assignment_repository: AssignmentRepository):
        self.assignment_repository = assignment_repository

    def create_assignment(
        self,
        title: str,
        description: str,
        due_date: datetime,
        teacher_id: int,
        section_id: int | None = None,
    ):
        normalized_due_date = due_date.astimezone(timezone.utc).replace(tzinfo=None) if due_date.tzinfo else due_date
        if normalized_due_date <= datetime.now(timezone.utc).replace(tzinfo=None):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Due date must be in the future")
        return self.assignment_repository.create(
            title=title,
            description=description,
            due_date=normalized_due_date,
            teacher_id=teacher_id,
            section_id=section_id,
        )

    def update_assignment(
        self,
        assignment_id: int,
        title: str,
        description: str,
        due_date: datetime,
        teacher_id: int,
        section_id: int | None = None,
    ):
        assignment = self.assignment_repository.get_by_id(assignment_id)
        if not assignment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
        if assignment.teacher_id != teacher_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        normalized_due_date = due_date.astimezone(timezone.utc).replace(tzinfo=None) if due_date.tzinfo else due_date
        assignment.section_id = section_id
        return self.assignment_repository.update(assignment, title=title, description=description, due_date=normalized_due_date)

    def delete_assignment(self, assignment_id: int, teacher_id: int) -> None:
        assignment = self.assignment_repository.get_by_id(assignment_id)
        if not assignment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
        if assignment.teacher_id != teacher_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        self.assignment_repository.delete(assignment_id)
