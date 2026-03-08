from dataclasses import dataclass
from datetime import datetime


@dataclass
class SubmissionEntity:
    id: int | None
    assignment_id: int
    student_id: int
    file_path: str
    grade: float | None
    feedback: str | None
    submitted_at: datetime | None
