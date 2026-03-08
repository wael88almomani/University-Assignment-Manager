from datetime import datetime

from pydantic import BaseModel

from app.presentation.schemas.auth_schema import PaginationMeta


class AssignmentCreateRequest(BaseModel):
    title: str
    description: str
    due_date: datetime
    section_id: int | None = None


class AssignmentUpdateRequest(BaseModel):
    title: str
    description: str
    due_date: datetime
    section_id: int | None = None


class AssignmentResponse(BaseModel):
    id: int
    title: str
    description: str
    due_date: datetime
    teacher_id: int
    section_id: int | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class AssignmentListResponse(BaseModel):
    data: list[AssignmentResponse]
    meta: PaginationMeta
