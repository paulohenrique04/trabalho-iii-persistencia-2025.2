from beanie import Document
from datetime import datetime
from pydantic import Field
from typing import Optional, List

class Watchlist(Document):
    name: str  
    user_id: str  
    movie_ids: List[str] = Field(default_factory=list)
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Settings:
        name = "watchlists"
