from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.presentation.schemas.auth_schema import PaginationMeta


class UserCreateRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    data: list[UserResponse]
    meta: PaginationMeta
