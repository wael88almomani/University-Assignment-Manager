from pydantic import BaseModel, ConfigDict, EmailStr


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MessageResponse(BaseModel):
    message: str


class PaginationMeta(BaseModel):
    page: int
    limit: int
    total: int


class BaseResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
