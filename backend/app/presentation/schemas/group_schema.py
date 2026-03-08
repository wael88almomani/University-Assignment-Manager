from datetime import datetime

from pydantic import BaseModel


class CourseCreateRequest(BaseModel):
    name: str
    code: str


class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    teacher_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class SectionCreateRequest(BaseModel):
    name: str
    course_id: int


class SectionResponse(BaseModel):
    id: int
    name: str
    course_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    section_id: int
    created_at: datetime

    class Config:
        from_attributes = True
