from datetime import datetime

from pydantic import BaseModel, Field

from app.presentation.schemas.auth_schema import PaginationMeta


class SubmissionResponse(BaseModel):
    id: int
    assignment_id: int
    student_id: int
    file_path: str
    grade: float | None
    feedback: str | None
    submitted_at: datetime

    class Config:
        from_attributes = True


class GradeSubmissionRequest(BaseModel):
    grade: float = Field(ge=0, le=100)
    feedback: str | None = None


class SubmissionListResponse(BaseModel):
    data: list[SubmissionResponse]
    meta: PaginationMeta
