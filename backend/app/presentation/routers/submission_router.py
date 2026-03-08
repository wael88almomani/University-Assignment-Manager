from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from app.core.dependencies import (
    get_assignment_repository,
    get_current_user,
    get_notification_service,
    get_submission_repository,
    get_submission_usecase,
    get_user_repository,
    require_roles,
)
from app.data.repositories.assignment_repository_impl import AssignmentRepositoryImpl
from app.data.repositories.submission_repository_impl import SubmissionRepositoryImpl
from app.data.repositories.user_repository_impl import UserRepositoryImpl
from app.presentation.schemas.auth_schema import PaginationMeta
from app.presentation.schemas.submission_schema import GradeSubmissionRequest, SubmissionListResponse, SubmissionResponse
from app.services.email_service import NotificationService
from app.usecases.submission_usecase import SubmissionUseCase


router = APIRouter(prefix="/submissions", tags=["Submissions"])


@router.get("", response_model=SubmissionListResponse)
def list_submissions(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    search: str = Query(default=""),
    status: str = Query(default="all"),
    sort: str = Query(default="newest"),
    current_user=Depends(get_current_user),
    submission_repository: SubmissionRepositoryImpl = Depends(get_submission_repository),
):
    skip = (page - 1) * limit
    if current_user.role == "teacher":
        items = submission_repository.list_by_teacher(
            teacher_id=current_user.id,
            skip=skip,
            limit=limit,
            search=search,
            status=status,
            sort=sort,
        )
        total = submission_repository.count_by_teacher(current_user.id, search=search, status=status)
    elif current_user.role == "student":
        items = submission_repository.list_by_student(student_id=current_user.id, skip=skip, limit=limit, search=search, status=status, sort=sort)
        total = submission_repository.count_by_student(current_user.id, search=search, status=status)
    else:
        items = submission_repository.list(skip=skip, limit=limit, search=search, status=status, sort=sort)
        total = submission_repository.count(search=search, status=status)
    return SubmissionListResponse(data=items, meta=PaginationMeta(page=page, limit=limit, total=total))


@router.get("/assignment/{assignment_id}", response_model=SubmissionListResponse)
def list_submissions_for_assignment(
    assignment_id: int,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    current_user=Depends(require_roles("teacher")),
    assignment_repository: AssignmentRepositoryImpl = Depends(get_assignment_repository),
    submission_repository: SubmissionRepositoryImpl = Depends(get_submission_repository),
):
    assignment = assignment_repository.get_by_id(assignment_id)
    if not assignment or assignment.teacher_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    skip = (page - 1) * limit
    items = submission_repository.list_by_assignment(assignment_id=assignment_id, skip=skip, limit=limit)
    total = submission_repository.count_by_assignment(assignment_id)
    return SubmissionListResponse(data=items, meta=PaginationMeta(page=page, limit=limit, total=total))


@router.patch("/{submission_id}/grade", response_model=SubmissionResponse)
def grade_submission(
    submission_id: int,
    payload: GradeSubmissionRequest,
    current_user=Depends(require_roles("teacher")),
    submission_usecase: SubmissionUseCase = Depends(get_submission_usecase),
    assignment_repository: AssignmentRepositoryImpl = Depends(get_assignment_repository),
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
    notification_service: NotificationService = Depends(get_notification_service),
):
    submission = submission_usecase.grade_submission(submission_id, payload.grade, payload.feedback, current_user.id)
    assignment = assignment_repository.get_by_id(submission.assignment_id)
    student = user_repository.get_by_id(submission.student_id)
    if assignment and student:
        notification_service.notify_grade_assigned(student.email, assignment.title, payload.grade)
    return submission
