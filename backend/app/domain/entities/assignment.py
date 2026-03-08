from dataclasses import dataclass
from datetime import datetime


@dataclass
class AssignmentEntity:
    id: int | None
    title: str
    description: str
    due_date: datetime
    teacher_id: int
    created_at: datetime | None
