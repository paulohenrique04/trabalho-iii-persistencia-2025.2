from datetime import date
from typing import Optional, List
from beanie import Document, Link
from pydantic import Field
from app.models.actor import Actor
from app.models.genre import Genre


class Movie(Document):
    title: str
    synopsis: Optional[str] = None
    release_date: date
    duration_minutes: int
    age_rating: Optional[str] = None
    director: Optional[str] = None

    actors: List[Link[Actor]] = Field(default_factory=list)
    genres: List[Link[Genre]] = Field(default_factory=list)

    class Settings:
        name = "movies"