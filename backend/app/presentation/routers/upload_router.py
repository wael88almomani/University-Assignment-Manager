from fastapi import APIRouter, Depends, File, UploadFile

from app.core.dependencies import (
    get_assignment_repository,
    get_current_user,
    get_file_service,
    get_notification_service,
    get_submission_usecase,
    get_user_repository,
    require_roles,
)
from app.data.repositories.assignment_repository_impl import AssignmentRepositoryImpl
from app.data.repositories.user_repository_impl import UserRepositoryImpl
from app.presentation.schemas.submission_schema import SubmissionResponse
from app.services.email_service import NotificationService
from app.services.file_service import FileService
from app.usecases.submission_usecase import SubmissionUseCase


router = APIRouter(prefix="/upload", tags=["Uploads"])


@router.post("/submissions/{assignment_id}", response_model=SubmissionResponse)
def upload_submission(
    assignment_id: int,
    file: UploadFile = File(...),
    current_user=Depends(require_roles("student")),
    file_service: FileService = Depends(get_file_service),
    submission_usecase: SubmissionUseCase = Depends(get_submission_usecase),
    assignment_repository: AssignmentRepositoryImpl = Depends(get_assignment_repository),
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
    notification_service: NotificationService = Depends(get_notification_service),
):
    file_path = file_service.save_submission_file(file)
    submission = submission_usecase.create_or_update_submission(assignment_id, current_user.id, file_path)

    assignment = assignment_repository.get_by_id(assignment_id)
    if assignment:
        teacher = user_repository.get_by_id(assignment.teacher_id)
        if teacher:
            notification_service.notify_submission_uploaded(teacher.email, assignment.title)
    return submission


@router.put("/submissions/{submission_id}", response_model=SubmissionResponse)
def update_submission(
    submission_id: int,
    file: UploadFile = File(...),
    current_user=Depends(require_roles("student")),
    file_service: FileService = Depends(get_file_service),
    submission_usecase: SubmissionUseCase = Depends(get_submission_usecase),
):
    file_path = file_service.save_submission_file(file)
    return submission_usecase.update_submission_before_deadline(submission_id, current_user.id, file_path)
