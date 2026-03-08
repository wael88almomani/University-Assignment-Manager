from fastapi import APIRouter, Depends, Query, status
from fastapi import HTTPException

from app.core.dependencies import get_user_repository, require_roles
from app.data.repositories.user_repository_impl import UserRepositoryImpl
from app.presentation.schemas.auth_schema import MessageResponse, PaginationMeta
from app.presentation.schemas.user_schema import UserCreateRequest, UserListResponse, UserResponse
from app.usecases.auth_usecase import AuthUseCase


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=UserListResponse)
def list_users(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    _: object = Depends(require_roles("admin")),
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
):
    skip = (page - 1) * limit
    users = user_repository.list(skip=skip, limit=limit)
    total = user_repository.count()
    return UserListResponse(data=users, meta=PaginationMeta(page=page, limit=limit, total=total))


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreateRequest,
    _: object = Depends(require_roles("admin")),
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
):
    auth_usecase = AuthUseCase(user_repository)
    return auth_usecase.register(payload.name, payload.email, payload.password, payload.role)


@router.delete("/{user_id}", response_model=MessageResponse)
def delete_user(
    user_id: int,
    _: object = Depends(require_roles("admin")),
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
):
    deleted = user_repository.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return MessageResponse(message="User deleted")
