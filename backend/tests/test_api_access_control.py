from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash
from app.data.models.user_model import User


def _create_user(db: Session, name: str, email: str, role: str) -> User:
    user = User(
        name=name,
        email=email,
        password=get_password_hash("password123"),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _auth_headers(user: User) -> dict[str, str]:
    token = create_access_token(subject=user.id, role=user.role)
    return {"Authorization": f"Bearer {token}"}


def test_teacher_can_create_course_and_section(client: TestClient, db_session: Session) -> None:
    teacher = _create_user(db_session, "Teacher One", "teacher1@example.com", "teacher")

    course_response = client.post(
        "/groups/courses",
        json={"name": "Algorithms", "code": "CS301"},
        headers=_auth_headers(teacher),
    )
    assert course_response.status_code == 201
    course_id = course_response.json()["id"]

    section_response = client.post(
        "/groups/sections",
        json={"name": "Section A", "course_id": course_id},
        headers=_auth_headers(teacher),
    )
    assert section_response.status_code == 201
    assert section_response.json()["course_id"] == course_id


def test_student_cannot_create_course_or_section(client: TestClient, db_session: Session) -> None:
    student = _create_user(db_session, "Student One", "student1@example.com", "student")

    course_response = client.post(
        "/groups/courses",
        json={"name": "Physics", "code": "PH101"},
        headers=_auth_headers(student),
    )
    assert course_response.status_code == 403

    section_response = client.post(
        "/groups/sections",
        json={"name": "Section A", "course_id": 1},
        headers=_auth_headers(student),
    )
    assert section_response.status_code == 403


def test_student_sees_only_enrolled_section_assignments(client: TestClient, db_session: Session) -> None:
    teacher = _create_user(db_session, "Teacher", "teacher@example.com", "teacher")
    student = _create_user(db_session, "Student", "student@example.com", "student")

    course = client.post(
        "/groups/courses",
        json={"name": "Databases", "code": "CS410"},
        headers=_auth_headers(teacher),
    )
    assert course.status_code == 201
    course_id = course.json()["id"]

    section_a = client.post(
        "/groups/sections",
        json={"name": "Section A", "course_id": course_id},
        headers=_auth_headers(teacher),
    )
    section_b = client.post(
        "/groups/sections",
        json={"name": "Section B", "course_id": course_id},
        headers=_auth_headers(teacher),
    )
    assert section_a.status_code == 201
    assert section_b.status_code == 201

    section_a_id = section_a.json()["id"]
    section_b_id = section_b.json()["id"]

    enroll = client.post(
        f"/groups/sections/{section_a_id}/students/{student.id}",
        headers=_auth_headers(teacher),
    )
    assert enroll.status_code == 200

    due_date = (datetime.utcnow() + timedelta(days=3)).isoformat()
    create_a = client.post(
        "/assignments",
        json={
            "title": "A1",
            "description": "For section A",
            "due_date": due_date,
            "section_id": section_a_id,
        },
        headers=_auth_headers(teacher),
    )
    create_b = client.post(
        "/assignments",
        json={
            "title": "B1",
            "description": "For section B",
            "due_date": due_date,
            "section_id": section_b_id,
        },
        headers=_auth_headers(teacher),
    )
    assert create_a.status_code == 201
    assert create_b.status_code == 201

    assignments = client.get("/assignments", headers=_auth_headers(student))
    assert assignments.status_code == 200
    payload = assignments.json()
    assert payload["meta"]["total"] == 1
    assert payload["data"][0]["section_id"] == section_a_id
    assert payload["data"][0]["title"] == "A1"


def test_teacher_cannot_grade_other_teachers_assignment(client: TestClient, db_session: Session) -> None:
    teacher_1 = _create_user(db_session, "Teacher One", "teacher.one@example.com", "teacher")
    teacher_2 = _create_user(db_session, "Teacher Two", "teacher.two@example.com", "teacher")
    student = _create_user(db_session, "Student One", "student.one@example.com", "student")

    course_response = client.post(
        "/groups/courses",
        json={"name": "Networks", "code": "CS450"},
        headers=_auth_headers(teacher_1),
    )
    assert course_response.status_code == 201

    section_response = client.post(
        "/groups/sections",
        json={"name": "Section A", "course_id": course_response.json()["id"]},
        headers=_auth_headers(teacher_1),
    )
    assert section_response.status_code == 201
    section_id = section_response.json()["id"]

    enroll_response = client.post(
        f"/groups/sections/{section_id}/students/{student.id}",
        headers=_auth_headers(teacher_1),
    )
    assert enroll_response.status_code == 200

    due_date = (datetime.utcnow() + timedelta(days=5)).isoformat()
    assignment_response = client.post(
        "/assignments",
        json={
            "title": "Midterm Assignment",
            "description": "Upload your solution",
            "due_date": due_date,
            "section_id": section_id,
        },
        headers=_auth_headers(teacher_1),
    )
    assert assignment_response.status_code == 201
    assignment_id = assignment_response.json()["id"]

    upload_response = client.post(
        f"/upload/submissions/{assignment_id}",
        files={"file": ("answer.pdf", b"%PDF-1.4 test", "application/pdf")},
        headers=_auth_headers(student),
    )
    assert upload_response.status_code == 200
    submission_id = upload_response.json()["id"]

    grade_response = client.patch(
        f"/submissions/{submission_id}/grade",
        json={"grade": 90, "feedback": "Good work"},
        headers=_auth_headers(teacher_2),
    )
    assert grade_response.status_code == 403
