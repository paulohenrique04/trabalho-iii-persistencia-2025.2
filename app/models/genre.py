# genre.py
from beanie import Document

class Genre(Document):
    name: str

    class Settings:
        name = "genres"