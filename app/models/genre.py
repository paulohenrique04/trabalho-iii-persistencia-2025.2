from beanie import Document
from pydantic import BaseModel

class Genre(Document):
    name: str

    class Settings:
        name = "genres"

class GenreCreate(BaseModel):
    name: str