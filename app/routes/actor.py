from typing import List, Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Query, status

from app.models import Actor, Movie

router = APIRouter(prefix="/actors", tags=["Atores"])


@router.post("/", response_model=Actor, status_code=status.HTTP_201_CREATED)
async def create_actor(actor: Actor):
    """Cria um novo ator"""
    await actor.insert()
    return actor


@router.get("/{actor_id}", response_model=Actor)
async def get_actor(actor_id: PydanticObjectId):
    """Busca ator por ID"""
    actor = await Actor.get(actor_id)
    if not actor:
        raise HTTPException(status_code=404, detail="Ator não encontrado")
    return actor


@router.get("/", response_model=List[Actor])
async def list_actors(
    name: Optional[str] = Query(
        None, description="Busca parcial case-insensitive no nome"
    ),
    birth_year: Optional[int] = Query(None, description="Filtro por ano de nascimento"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
):
    """Lista atores com filtros e paginação"""
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if birth_year:
        query["birth_year"] = birth_year

    actors = await Actor.find(query).skip(skip).limit(limit).to_list()
    return actors


@router.put("/{actor_id}", response_model=Actor)
async def update_actor(actor_id: PydanticObjectId, actor_update: Actor):
    """Atualiza ator (parcial)"""
    actor = await Actor.get(actor_id)
    if not actor:
        raise HTTPException(status_code=404, detail="Ator não encontrado")

    update_data = actor_update.model_dump(exclude_unset=True)
    await actor.set(update_data)
    return actor


@router.delete("/{actor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_actor(actor_id: PydanticObjectId):
    """Deleta ator"""
    actor = await Actor.get(actor_id)
    if not actor:
        raise HTTPException(status_code=404, detail="Ator não encontrado")
    await actor.delete()
    return None


@router.get("/{actor_id}/movies", response_model=List[Movie])
async def get_movies_by_actor(
    actor_id: PydanticObjectId,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
):
    """Lista todos os filmes de um ator (consulta envolvendo múltiplas coleções)"""
    movies = await Movie.find({"actors": actor_id}).skip(skip).limit(limit).to_list()
    return movies
    movies = await Movie.find({"actors": actor_id}).skip(skip).limit(limit).to_list()
    return movies