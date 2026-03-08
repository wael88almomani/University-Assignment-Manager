from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_auth_usecase
from app.presentation.schemas.auth_schema import LoginRequest, TokenResponse
from app.presentation.schemas.user_schema import UserCreateRequest, UserResponse
from app.usecases.auth_usecase import AuthUseCase


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreateRequest, auth_usecase: AuthUseCase = Depends(get_auth_usecase)):
    user = auth_usecase.register(
        name=payload.name,
        email=payload.email,
        password=payload.password,
        role=payload.role,
    )
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, auth_usecase: AuthUseCase = Depends(get_auth_usecase)):
    token = auth_usecase.login(email=payload.email, password=payload.password)
    return TokenResponse(access_token=token)
