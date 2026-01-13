# user.py
from datetime import datetime
from beanie import Document
from pydantic import Field


class User(Document):
    username: str
    email: str
    password: str
    bio: str = None
    birthdate: datetime = None
    gender: str = None
    country: str = None
    telephone: str = None
    city: str = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"