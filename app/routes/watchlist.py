from datetime import datetime
from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate
from typing import Optional

from app.models.watchlist import Watchlist, WatchlistCreate
from app.models.user import User
from app.models.movie import Movie

router = APIRouter(prefix="/watchlists", tags=["Watchlists"])

@router.post("/", response_model=WatchlistCreate)
async def create_watchlist(watchlist_data: WatchlistCreate):
    """Adiciona filme à watchlist"""
    watchlist_data.user = await User.get(watchlist_data.user)
    watchlist_data.movie = await Movie.get(watchlist_data.movie)

    if not watchlist_data.user or not watchlist_data.movie:
        raise HTTPException(status_code=404, detail="Usuário ou Filme não encontrado")
    
    watchlist = Watchlist.model_validate(watchlist_data)
    await watchlist.insert()

    watchlist_inserted = await Watchlist.get(watchlist.id, fetch_links=True)
    if not watchlist_inserted:
        raise HTTPException(status_code=500, detail="Erro ao adicionar à watchlist")
    return watchlist_inserted

@router.get("/{watchlist_id}", response_model=Watchlist)
async def get_watchlist_by_id(watchlist_id: PydanticObjectId):
    """a) Consulta por ID"""
    watchlist = await Watchlist.get(watchlist_id, fetch_links=True)
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist não encontrada")
    return watchlist

@router.get("/", response_model=Page[Watchlist])
async def get_watchlists(user_id: Optional[str] = None):
    """Lista watchlists"""
    query = {}
    if user_id:
        query["user_id"] = user_id
    return await apaginate(Watchlist.find(query))

@router.delete("/{watchlist_id}")
async def delete_watchlist(watchlist_id: PydanticObjectId):
    """Remove da watchlist"""
    watchlist = await Watchlist.get(watchlist_id)
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist não encontrada")
    
    await watchlist.delete()
    return {"message": "Removido da watchlist"}

# CONSULTAS REQUERIDAS
@router.get("/user/{user_id}/movies")
async def get_user_watchlist(user_id: str):
    """b) Listagem por relacionamento"""
    watchlists = await Watchlist.find(Watchlist.user_id == user_id).to_list()
    return watchlists

@router.get("/movie/{movie_id}/count")
async def count_movie_in_watchlists(movie_id: str):
    """e) Contagem de watchlists por filme"""
    count = await Watchlist.find(Watchlist.movie_id == movie_id).count()
    return {"movie_id": movie_id, "total_watchlists": count}

@router.get("/statistics/popular-movies")
async def get_popular_movies_in_watchlists(limit: int = 10):
    """e) Agregação - Filmes mais populares"""
    pipeline = [
        {"$group": {
            "_id": "$movie_id",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]
    
    result = await Watchlist.aggregate(pipeline).to_list()
    return result

@router.get("/search/notes")
async def search_notes(text: str):
    """c) Busca textual nas notas"""
    watchlists = await Watchlist.find(
        {"notes": {"$regex": text, "$options": "i"}}
    ).to_list()
    return watchlists
