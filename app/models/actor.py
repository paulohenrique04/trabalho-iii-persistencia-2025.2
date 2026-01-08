from typing import Optional
from beanie import Document


class Actor(Document):
    name: str
    birth_date: Optional[str] = None
    nationality: Optional[str] = None
    biography: Optional[str] = None

    class Settings:
        name = "actors"