from beanie import Document


class Actor(Document):
    name: str
    birth_date: str = None
    nationality: str = None
    biography: str = None
    height_cm: float = None
    awards: list[str] = []
    instagram: str = None
    know_for: str = None
    indications: list[str] = []
    
    class Settings:
        name = "actors"