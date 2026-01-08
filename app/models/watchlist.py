from typing import Optional
from beanie import Document, Link
from pydantic import Field
from app.models.movie import Movie
from app.models.user import User


class Watchlist(Document):
    user: Link[User]
    movie: Link[Movie]
    notes: Optional[str] = None

    class Settings:
        name = "watchlists"