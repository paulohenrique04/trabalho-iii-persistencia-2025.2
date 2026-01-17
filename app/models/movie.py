from datetime import date
from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel
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
    imdb: float = None

    actors: list[Link[Actor]] = Field(default_factory=list)
    genres: list[Link[Genre]] = Field(default_factory=list)

    class Settings:
        name = "movies"
        indexes = [
            [
                ("title", "text"),
            ]
        ]


class MovieCreate(BaseModel):
    title: str
    synopsis: str = None
    release_date: date
    duration_minutes: int
    age_rating: str = None
    director: str = None
    original_title: str = None
    imdb: float = None

    actors: list[PydanticObjectId] = []
    genres: list[PydanticObjectId] = []

class MovieByGenreItem(BaseModel):
    title: str
    original_title: str = None
    imdb: float = None

class MoviesByGenreResponse(BaseModel):
    genre: str
    total_movies: int
    movies: list[MovieByGenreItem]
