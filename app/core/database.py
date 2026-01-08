from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models.actor import Actor
from app.models.movie import Movie
from app.models.genre import Genre
from app.models.user import User
from app.models.review import Review
from app.models.watchlist import Watchlist

client = AsyncIOMotorClient(settings.MONGODB_URL)

db = client[settings.MONGODB_DATABASE]

async def init_db() -> None:
    """
    Inicializa o Beanie com os Documents registrados
    """
    await init_beanie(
        database=db,
        document_models=[
            Actor,
            Movie,
            Genre,
            User,
            Review,
            Watchlist
        ],
    )
