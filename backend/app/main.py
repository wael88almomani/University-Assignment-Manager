import logging
from time import perf_counter

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy import inspect, text
from starlette import status

from app.core.config import settings
from app.core.database import Base, engine
from app.core.logging_config import setup_logging
from app.core.rate_limiter import InMemoryRateLimiter, rate_limit_middleware
from app.data.models.assignment_model import Assignment
from app.data.models.course_model import Course
from app.data.models.enrollment_model import Enrollment
from app.data.models.section_model import Section
from app.data.models.submission_model import Submission
from app.data.models.user_model import User
from app.presentation.routers.assignment_router import router as assignment_router
from app.presentation.routers.auth_router import router as auth_router
from app.presentation.routers.group_router import router as group_router
from app.presentation.routers.submission_router import router as submission_router
from app.presentation.routers.upload_router import router as upload_router
from app.presentation.routers.user_router import router as user_router


User
Assignment
Submission
Course
Section
Enrollment


def apply_safe_schema_updates() -> None:
    inspector = inspect(engine)
    try:
        columns = {col["name"] for col in inspector.get_columns("assignments")}
    except NoSuchTableError:
        return
    if "section_id" not in columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE assignments ADD COLUMN section_id INTEGER"))


apply_safe_schema_updates()

Base.metadata.create_all(bind=engine)

setup_logging(settings.log_level)
logger = logging.getLogger("uam.api")

rate_limiter = InMemoryRateLimiter(
    max_requests=settings.rate_limit_max_requests,
    window_seconds=settings.rate_limit_window_seconds,
)

route_rate_limiters = {
    "/auth/login": InMemoryRateLimiter(
        max_requests=settings.rate_limit_login_max_requests,
        window_seconds=settings.rate_limit_login_window_seconds,
    ),
    "/auth/register": InMemoryRateLimiter(
        max_requests=settings.rate_limit_register_max_requests,
        window_seconds=settings.rate_limit_register_window_seconds,
    ),
}

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_middleware(request: Request, call_next):
    start = perf_counter()
    response = await rate_limit_middleware(
        request,
        call_next,
        limiter=rate_limiter,
        route_limiters=route_rate_limiters,
    )
    elapsed_ms = (perf_counter() - start) * 1000
    logger.info(
        "%s %s -> %s (%.2fms)",
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
    )
    return response


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception):
    logger.exception("Unhandled server error: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(assignment_router)
app.include_router(group_router)
app.include_router(submission_router)
app.include_router(upload_router)


@app.get("/")
def root():
    return {"message": "University Assignment Manager API"}


@app.get("/api/v1/health")
def health_check():
    """Health check endpoint for monitoring and Docker healthcheck"""
    return {
        "status": "healthy",
        "service": "University Assignment Manager API",
        "version": "1.0.0",
    }
