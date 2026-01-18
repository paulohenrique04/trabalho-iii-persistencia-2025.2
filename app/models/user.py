from datetime import datetime
from beanie import Document
from pydantic import BaseModel

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

    class Settings:
        name = "users"

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    bio: str = None
    birthdate: datetime = None
    gender: str = None
    country: str = None
    telephone: str = None
    city: str = None
    

class UserUpdate(BaseModel):
    username: str
    email: str
    password: str
    bio: str = None
    birthdate: datetime = None
    gender: str = None
    country: str = None
    telephone: str = None
    city: str = None
    

