from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import movie, genre
from app.core.database import init_db, close_db
from fastapi_pagination import add_pagination

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

app = FastAPI(lifespan=lifespan)

app.include_router(movie.router)
app.include_router(genre.router)
# app.include_router(actor.router)
# app.include_router(user.router)
# app.include_router(review.router)
# app.include_router(watchlist.router)
add_pagination(app)