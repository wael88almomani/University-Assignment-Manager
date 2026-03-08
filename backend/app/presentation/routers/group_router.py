from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.dependencies import (
    get_course_repository,
    get_enrollment_repository,
    get_section_repository,
    get_user_repository,
    require_roles,
)
from app.data.repositories.course_repository_impl import CourseRepositoryImpl
from app.data.repositories.enrollment_repository_impl import EnrollmentRepositoryImpl
from app.data.repositories.section_repository_impl import SectionRepositoryImpl
from app.data.repositories.user_repository_impl import UserRepositoryImpl
from app.presentation.schemas.group_schema import (
    CourseCreateRequest,
    CourseResponse,
    EnrollmentResponse,
    SectionCreateRequest,
    SectionResponse,
)
from app.presentation.schemas.user_schema import UserListResponse
from app.presentation.schemas.auth_schema import PaginationMeta


router = APIRouter(prefix="/groups", tags=["Groups"])


@router.get("/students", response_model=UserListResponse)
def list_students_for_enrollment(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    search: str = Query(default=""),
    _: object = Depends(require_roles("teacher")),
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
):
    skip = (page - 1) * limit
    students = user_repository.list_students(search=search, skip=skip, limit=limit)
    total = user_repository.count_students(search=search)
    return UserListResponse(data=students, meta=PaginationMeta(page=page, limit=limit, total=total))


@router.post("/courses", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    payload: CourseCreateRequest,
    current_user=Depends(require_roles("teacher")),
    course_repository: CourseRepositoryImpl = Depends(get_course_repository),
):
    return course_repository.create(name=payload.name, code=payload.code, teacher_id=current_user.id)


@router.get("/courses/me", response_model=list[CourseResponse])
def my_courses(
    current_user=Depends(require_roles("teacher")),
    course_repository: CourseRepositoryImpl = Depends(get_course_repository),
):
    return course_repository.list_by_teacher(current_user.id)


@router.post("/sections", response_model=SectionResponse, status_code=status.HTTP_201_CREATED)
def create_section(
    payload: SectionCreateRequest,
    current_user=Depends(require_roles("teacher")),
    course_repository: CourseRepositoryImpl = Depends(get_course_repository),
    section_repository: SectionRepositoryImpl = Depends(get_section_repository),
):
    course = course_repository.get_by_id(payload.course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    if course.teacher_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    return section_repository.create(name=payload.name, course_id=payload.course_id)


@router.get("/sections/me", response_model=list[SectionResponse])
def my_sections(
    current_user=Depends(require_roles("teacher")),
    section_repository: SectionRepositoryImpl = Depends(get_section_repository),
):
    return section_repository.list_by_teacher(current_user.id)


@router.post("/sections/{section_id}/students/{student_id}", response_model=EnrollmentResponse)
def enroll_student(
    section_id: int,
    student_id: int,
    current_user=Depends(require_roles("teacher")),
    section_repository: SectionRepositoryImpl = Depends(get_section_repository),
    enrollment_repository: EnrollmentRepositoryImpl = Depends(get_enrollment_repository),
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
):
    if not section_repository.belongs_to_teacher(section_id=section_id, teacher_id=current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    student = user_repository.get_by_id(student_id)
    if not student or student.role != "student":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return enrollment_repository.create(student_id=student_id, section_id=section_id)


@router.get("/me/section-ids", response_model=list[int])
def my_section_ids(
    current_user=Depends(require_roles("student")),
    enrollment_repository: EnrollmentRepositoryImpl = Depends(get_enrollment_repository),
):
    return enrollment_repository.list_section_ids_by_student(current_user.id)
