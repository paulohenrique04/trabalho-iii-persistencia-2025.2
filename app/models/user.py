
from datetime import datetime
from beanie import Document
from pydantic import BaseModel, Field
from typing import Optional

class User(Document):
    username: str
    email: str
    password: str
    
    
    class Settings:
        name = "users"

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    bio: Optional[str] = None
    birthdate: Optional[datetime] = None
    

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    

