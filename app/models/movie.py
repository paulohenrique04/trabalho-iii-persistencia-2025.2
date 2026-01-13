from datetime import date
from beanie import Document, Link
from pydantic import Field
from app.models.actor import Actor
from app.models.genre import Genre


class Movie(Document):
    title: str
    synopsis: str = None
    release_date: date
    duration_minutes: int
    age_rating: str = None
    director: str = None
    original_title: str = None
    language: str = None

    actors: list[Link[Actor]] = Field(default_factory=list)
    genres: list[Link[Genre]] = Field(default_factory=list)

    class Settings:
        name = "movies"