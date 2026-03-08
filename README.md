# University Assignment Manager

University Assignment Manager is a full-stack system for managing university assignments between teachers and students, with course and section isolation.

## What The System Does

- Teachers can create courses and sections.
- Teachers can enroll students into sections.
- Teachers can search students by name/email before enrollment.
- Teachers create assignments for a specific section.
- Students only see assignments for sections they are enrolled in.
- Students submit text/file solutions.
- Teachers review and grade submissions with feedback.

## Main Features

- JWT authentication and role-based access (`teacher`, `student`, `admin`)
- Course -> Section -> Enrollment structure
- Assignment visibility isolation by section
- Teacher-friendly student enrollment flow (search + picker)
- Submission upload and grading flow
- Rate limiting for API and auth endpoints
- Alembic database migrations for schema versioning
- API integration tests for role-based access control
- Flutter app with BLoC state management

## Tech Stack

### Backend

- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- Python-JOSE + Passlib (JWT + password hashing)
- SQLite (default), Docker support

### Frontend

- Flutter
- Dart
- flutter_bloc
- Dio
- flutter_secure_storage

## Project Structure

```text
University Assignment Manager/
|-- backend/
|   |-- alembic/
|   |   `-- versions/
|   |-- tests/
|   |-- app/
|   |   |-- core/
|   |   |   |-- config.py
|   |   |   |-- database.py
|   |   |   |-- dependencies.py
|   |   |   |-- logging_config.py
|   |   |   |-- rate_limiter.py
|   |   |   `-- security.py
|   |   |-- data/
|   |   |   |-- models/
|   |   |   |   |-- assignment_model.py
|   |   |   |   |-- course_model.py
|   |   |   |   |-- enrollment_model.py
|   |   |   |   |-- section_model.py
|   |   |   |   |-- submission_model.py
|   |   |   |   `-- user_model.py
|   |   |   `-- repositories/
|   |   |       |-- assignment_repository_impl.py
|   |   |       |-- course_repository_impl.py
|   |   |       |-- enrollment_repository_impl.py
|   |   |       |-- section_repository_impl.py
|   |   |       |-- submission_repository_impl.py
|   |   |       `-- user_repository_impl.py
|   |   |-- domain/
|   |   |   `-- entities/
|   |   |-- presentation/
|   |   |   |-- routers/
|   |   |   |   |-- assignment_router.py
|   |   |   |   |-- auth_router.py
|   |   |   |   |-- group_router.py
|   |   |   |   |-- submission_router.py
|   |   |   |   |-- upload_router.py
|   |   |   |   `-- user_router.py
|   |   |   `-- schemas/
|   |   |       |-- assignment_schema.py
|   |   |       |-- auth_schema.py
|   |   |       |-- group_schema.py
|   |   |       |-- submission_schema.py
|   |   |       `-- user_schema.py
|   |   |-- repositories/
|   |   |-- services/
|   |   |-- usecases/
|   |   `-- main.py
|   |-- requirements.txt
|   |-- alembic.ini
|   |-- pytest.ini
|   |-- Dockerfile
|   `-- uploads/
|-- frontend/
|   |-- assets/
|   |   `-- icons/
|   |-- lib/
|   |   |-- core/
|   |   |   |-- api/
|   |   |   |   |-- api_config.dart
|   |   |   |   `-- dio_client.dart
|   |   |   |-- storage/
|   |   |   `-- theme/
|   |   |-- features/
|   |   |   |-- auth/
|   |   |   |-- assignments/
|   |   |   |-- groups/
|   |   |   `-- submissions/
|   |   |-- widgets/
|   |   `-- main.dart
|   |-- android/
|   |-- ios/
|   |-- web/
|   |-- windows/
|   |-- linux/
|   |-- macos/
|   `-- test/
|-- deploy.ps1
|-- update-api-url.ps1
`-- docker-compose.yml
```

## Run Locally

### 1) Backend

```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2) Frontend

```bash
cd frontend
flutter pub get
flutter run
```

### Optional Helpers

- `update-api-url.ps1`: updates Flutter API base URL for localhost/LAN/custom URL.
- `deploy.ps1`: quick menu for APK build, backend run, combined flow, or Docker deploy.

## Database Migrations

Use Alembic for schema changes:

```bash
cd backend
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

For existing databases created before Alembic:

```bash
cd backend
alembic stamp head
```

## Run API Tests

```bash
cd backend
pytest -q
```

Current tests validate:

- Teacher can create courses/sections.
- Student cannot create courses/sections.
- Student sees only assignments from enrolled sections.
- Teacher cannot grade submissions for another teacher's assignments.

## API Health Check

- `GET /api/v1/health`

Expected response contains status, service name, and version.

