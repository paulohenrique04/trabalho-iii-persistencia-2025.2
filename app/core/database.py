from dotenv import load_dotenv
from pymongo import AsyncMongoClient
from beanie import init_beanie
import os
import logging
from app.models.actor import Actor
from app.models.movie import Movie
from app.models.genre import Genre
from app.models.user import User
from app.models.review import Review
from app.models.watchlist import Watchlist

load_dotenv()
DATABASE_URL = os.getenv("MONGODB_URL")
DBNAME = os.getenv("MONGODB_DATABASE")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
)

logger = logging.getLogger(__name__)
_client: AsyncMongoClient | None = None

async def init_db() -> None:
    """
    Inicializa o Beanie com os Documents registrados
    """

    global _client
    _client = AsyncMongoClient(DATABASE_URL)
    db = _client[DBNAME]

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

async def close_db():
    global _client
    if _client is not None:
        _client.close()
        logger.info(f"Conexão com o banco de dados {DATABASE_URL} fechada.")
        _client = None
