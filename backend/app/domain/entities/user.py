from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserEntity:
    id: int | None
    name: str
    email: str
    password: str
    role: str
    created_at: datetime | None
