from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.dependencies import (
    get_assignment_repository,
    get_assignment_usecase,
    get_enrollment_repository,
    get_current_user,
    get_notification_service,
    get_section_repository,
    get_user_repository,
    require_roles,
)
from app.data.repositories.assignment_repository_impl import AssignmentRepositoryImpl
from app.data.repositories.enrollment_repository_impl import EnrollmentRepositoryImpl
from app.data.repositories.section_repository_impl import SectionRepositoryImpl
from app.data.repositories.user_repository_impl import UserRepositoryImpl
from app.presentation.schemas.assignment_schema import (
    AssignmentCreateRequest,
    AssignmentListResponse,
    AssignmentResponse,
    AssignmentUpdateRequest,
)
from app.presentation.schemas.auth_schema import MessageResponse, PaginationMeta
from app.services.email_service import NotificationService
from app.usecases.assignment_usecase import AssignmentUseCase


router = APIRouter(prefix="/assignments", tags=["Assignments"])


@router.post("", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
def create_assignment(
    payload: AssignmentCreateRequest,
    current_user=Depends(require_roles("teacher")),
    assignment_usecase: AssignmentUseCase = Depends(get_assignment_usecase),
    enrollment_repository: EnrollmentRepositoryImpl = Depends(get_enrollment_repository),
    section_repository: SectionRepositoryImpl = Depends(get_section_repository),
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
    notification_service: NotificationService = Depends(get_notification_service),
):
    if payload.section_id is not None and not section_repository.belongs_to_teacher(payload.section_id, current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed for this section")

    assignment = assignment_usecase.create_assignment(
        title=payload.title,
        description=payload.description,
        due_date=payload.due_date,
        teacher_id=current_user.id,
        section_id=payload.section_id,
    )
    if assignment.section_id is not None:
        target_student_ids = set(enrollment_repository.list_student_ids_by_section(assignment.section_id))
        students = [
            u for u in user_repository.list(skip=0, limit=1000000) if u.role == "student" and u.id in target_student_ids
        ]
    else:
        students = [u for u in user_repository.list(skip=0, limit=1000000) if u.role == "student"]
    for student in students:
        notification_service.notify_assignment_created(student.email, assignment.title)
    return assignment


@router.get("", response_model=AssignmentListResponse)
def list_assignments(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    search: str = Query(default=""),
    status: str = Query(default="all"),
    sort: str = Query(default="due_soonest"),
    current_user=Depends(get_current_user),
    enrollment_repository: EnrollmentRepositoryImpl = Depends(get_enrollment_repository),
    assignment_repository: AssignmentRepositoryImpl = Depends(get_assignment_repository),
):
    skip = (page - 1) * limit

    if current_user.role == "teacher":
        assignments = assignment_repository.list_by_teacher(
            teacher_id=current_user.id,
            skip=skip,
            limit=limit,
            search=search,
            status=status,
            sort=sort,
        )
        total = assignment_repository.count_by_teacher(current_user.id, search=search, status=status)
    elif current_user.role == "student":
        section_ids = enrollment_repository.list_section_ids_by_student(current_user.id)
        assignments = assignment_repository.list_by_student_sections(
            section_ids=section_ids,
            skip=skip,
            limit=limit,
            search=search,
            status=status,
            sort=sort,
        )
        total = assignment_repository.count_by_student_sections(section_ids, search=search, status=status)
    else:
        assignments = assignment_repository.list(skip=skip, limit=limit, search=search, status=status, sort=sort)
        total = assignment_repository.count(search=search, status=status)

    return AssignmentListResponse(data=assignments, meta=PaginationMeta(page=page, limit=limit, total=total))


@router.put("/{assignment_id}", response_model=AssignmentResponse)
def update_assignment(
    assignment_id: int,
    payload: AssignmentUpdateRequest,
    current_user=Depends(require_roles("teacher")),
    assignment_usecase: AssignmentUseCase = Depends(get_assignment_usecase),
    section_repository: SectionRepositoryImpl = Depends(get_section_repository),
):
    if payload.section_id is not None and not section_repository.belongs_to_teacher(payload.section_id, current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed for this section")
    return assignment_usecase.update_assignment(
        assignment_id=assignment_id,
        title=payload.title,
        description=payload.description,
        due_date=payload.due_date,
        teacher_id=current_user.id,
        section_id=payload.section_id,
    )


@router.delete("/{assignment_id}", response_model=MessageResponse)
def delete_assignment(
    assignment_id: int,
    current_user=Depends(require_roles("teacher")),
    assignment_usecase: AssignmentUseCase = Depends(get_assignment_usecase),
):
    assignment_usecase.delete_assignment(assignment_id, current_user.id)
    return MessageResponse(message="Assignment deleted")
