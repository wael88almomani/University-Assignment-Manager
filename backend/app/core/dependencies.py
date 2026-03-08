from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.email_service import SMTPEmailService
from app.core.security import decode_access_token
from app.data.repositories.assignment_repository_impl import AssignmentRepositoryImpl
from app.data.repositories.course_repository_impl import CourseRepositoryImpl
from app.data.repositories.enrollment_repository_impl import EnrollmentRepositoryImpl
from app.data.repositories.section_repository_impl import SectionRepositoryImpl
from app.data.repositories.submission_repository_impl import SubmissionRepositoryImpl
from app.data.repositories.user_repository_impl import UserRepositoryImpl
from app.services.email_service import NotificationService
from app.services.file_service import FileService
from app.usecases.assignment_usecase import AssignmentUseCase
from app.usecases.auth_usecase import AuthUseCase
from app.usecases.submission_usecase import SubmissionUseCase


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_repository(db: Session = Depends(get_db)) -> UserRepositoryImpl:
    return UserRepositoryImpl(db)


def get_assignment_repository(db: Session = Depends(get_db)) -> AssignmentRepositoryImpl:
    return AssignmentRepositoryImpl(db)


def get_course_repository(db: Session = Depends(get_db)) -> CourseRepositoryImpl:
    return CourseRepositoryImpl(db)


def get_section_repository(db: Session = Depends(get_db)) -> SectionRepositoryImpl:
    return SectionRepositoryImpl(db)


def get_enrollment_repository(db: Session = Depends(get_db)) -> EnrollmentRepositoryImpl:
    return EnrollmentRepositoryImpl(db)


def get_submission_repository(db: Session = Depends(get_db)) -> SubmissionRepositoryImpl:
    return SubmissionRepositoryImpl(db)


def get_auth_usecase(user_repository: UserRepositoryImpl = Depends(get_user_repository)) -> AuthUseCase:
    return AuthUseCase(user_repository)


def get_assignment_usecase(
    assignment_repository: AssignmentRepositoryImpl = Depends(get_assignment_repository),
) -> AssignmentUseCase:
    return AssignmentUseCase(assignment_repository)


def get_submission_usecase(
    submission_repository: SubmissionRepositoryImpl = Depends(get_submission_repository),
    assignment_repository: AssignmentRepositoryImpl = Depends(get_assignment_repository),
    enrollment_repository: EnrollmentRepositoryImpl = Depends(get_enrollment_repository),
) -> SubmissionUseCase:
    return SubmissionUseCase(submission_repository, assignment_repository, enrollment_repository)


def get_file_service() -> FileService:
    return FileService()


def get_notification_service() -> NotificationService:
    return NotificationService(SMTPEmailService())


def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError, TypeError):
        raise credentials_exception
    user = user_repository.get_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user


def require_roles(*roles: str) -> Callable:
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user

    return role_checker
