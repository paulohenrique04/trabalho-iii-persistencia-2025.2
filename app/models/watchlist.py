from beanie import Document, Link
from datetime import datetime
from pydantic import Field
from app.models.movie import Movie
from app.models.user import User


class Watchlist(Document):
    user: Link[User]
    movie: Link[Movie]
    notes: str = None

    class Settings:
        name = "watchlists"