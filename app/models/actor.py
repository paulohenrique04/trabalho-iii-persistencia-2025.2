from beanie import Document
from pydantic import BaseModel


class Actor(Document):
    name: str
    birth_date: str = None
    nationality: str = None
    biography: str = None
    height_cm: float = None
    awards: list[str] = []
    instagram: str = None
    know_for: str = None
    indications: list[str] = []

    class Settings:
        name = "actors"

class ActorCreate(BaseModel):
    name: str
    birth_date: str = None
    nationality: str = None
    biography: str = None
    height_cm: float = None
    awards: list[str] = []
    instagram: str = None
    know_for: str = None
    indications: list[str] = []

class ActorUpdate(BaseModel):
    name: str | None = None
    birth_date: str | None = None
    nationality: str | None = None
    biography: str | None = None
    height_cm: float | None = None
    awards: list[str] | None = None
    instagram: str | None = None
    know_for: str | None = None
    indications: list[str] | None = None
