from typing import Optional
from beanie import Document, Link
from app.models.movie import Movie
from app.models.user import User


class Review(Document):
    movie: Link[Movie]
    user: Link[User]
    rating: float 
    content: Optional[str] = None

    class Settings:
        name = "reviews"