import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import close_db, init_db
from app.routes import actor, genre, movie, review
from fastapi_pagination import add_pagination

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    # Startup
    logger.info("Iniciando aplicação...")
    await init_db()
    logger.info("Banco de dados inicializado com sucesso!")
    yield
    # Shutdown
    logger.info("Encerrando aplicação...")
    await close_db()
    logger.info("Conexão com banco de dados fechada!")


# Configuração da aplicação FastAPI
app = FastAPI(
    title="API de Filmes e Atores",
    description="API robusta para gerenciamento de filmes, atores, usuários e reviews com MongoDB",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(actor.router)
app.include_router(genre.router)
app.include_router(movie.router)
app.include_router(review.router)
# app.include_router(user.router)
# app.include_router(watchlist.router)

add_pagination(app)

@app.get("/")
async def root():
    """Rota raiz da API"""
    return {
        "message": "Bem-vindo à API de Filmes ",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


@app.get("/health")
async def health_check():
    """Health check para verificar se a API está rodando"""
    return {"status": "healthy", "service": "API de Filmes"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)