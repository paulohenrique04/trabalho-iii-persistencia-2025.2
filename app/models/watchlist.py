from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel
from app.models.movie import Movie
from app.models.user import User

class Watchlist(Document):
    user: Link[User]
    movie: Link[Movie]
    notes: str = None

    class Settings:
        name = "watchlists"

class WatchlistCreate(BaseModel):
    user: PydanticObjectId
    movie: PydanticObjectId
    notes: str = None
