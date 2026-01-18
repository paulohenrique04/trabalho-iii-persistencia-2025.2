from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel

from app.models.movie import Movie
from app.models.user import User


class Review(Document):
    movie: Link[Movie]
    user: Link[User]
    rating: float
    content: str = None
    title: str = None
    spoiler: bool = False

    class Settings:
        name = "reviews"


class ReviewUpdate(BaseModel):
    movie: PydanticObjectId | None = None
    user: PydanticObjectId | None = None
    rating: float | None = None
    content: str | None = None
    title: str | None = None
    spoiler: bool | None = None
