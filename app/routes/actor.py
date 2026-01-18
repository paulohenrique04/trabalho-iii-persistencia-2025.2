from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Query, status
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate
from bson import ObjectId

from app.models import Actor, Movie
from app.models.actor import ActorUpdate, ActorCreate

router = APIRouter(prefix="/actors", tags=["Atores"])


@router.post("/", response_model=Actor, status_code=status.HTTP_201_CREATED)
async def create_actor(actor: ActorCreate) -> Actor:
    """Cria um novo ator"""
    actor_model = Actor(**actor.model_dump())
    await actor_model.insert()

    actor_inserted = await Actor.get(actor_model.id, fetch_links=True)

    if not actor_inserted:
        raise HTTPException(status_code=500, detail="Erro ao criar o ator")
    
    return actor_inserted


@router.get("/{actor_id}", response_model=Actor)
async def get_actor_by_id(actor_id: PydanticObjectId) -> Actor:
    """Retorna um ator pelo seu ID"""
    actor = await Actor.get(actor_id, fetch_links=True)
    if not actor:
        raise HTTPException(status_code=404, detail="Ator não encontrado")
    return actor


@router.get("/", response_model=Page[Actor])
async def get_actors(name: str | None = Query(None, description="Busca parcial case-insensitive no nome"), birth_year: int | None = Query(None, description="Filtro por ano de nascimento")) -> Page[Actor]:
    """
    Retorna uma lista paginada de atores com filtros opcionais.
    """
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if birth_year:
        query["birth_year"] = birth_year
    
    return await apaginate(Actor.find(query))


@router.put("/{actor_id}", response_model=Actor)
async def update_actor(actor_id: PydanticObjectId, actor_data: ActorUpdate) -> Actor:
    """
    Atualiza um ator existente.
    """
    actor = await Actor.get(actor_id)
    if not actor:
        raise HTTPException(status_code=404, detail="Ator não encontrado")

    for key, value in actor_data.dict(exclude_unset=True).items():
        setattr(actor, key, value)

    await actor.save()
    return actor


@router.delete("/{actor_id}")
async def delete_actor(actor_id: PydanticObjectId) -> dict:
    """
    Deleta um ator existente.
    """
    actor = await Actor.get(actor_id)
    if not actor:
        raise HTTPException(status_code=404, detail="Ator não encontrado")
    
    await actor.delete()
    return {"mensagem": "Ator deletado com sucesso"}

@router.get("/{actor_id}/movies")
async def get_movies_by_actor(actor_id: PydanticObjectId):
    actor = await Actor.get(actor_id)
    if not actor:
        raise HTTPException(status_code=404, detail="Ator não encontrado")

    pipeline = [
        {
            "$match": {
                "actors.$id": ObjectId(actor_id)
            }
        },
        {
            "$project": {
                "id": { "$toString": "$_id" },
                "_id": 0,
                "title": 1,
                "synopsis": 1,
                "duration_minutes": 1,
                "age_rating": 1,
                "director": 1,
                "original_title": 1,
                "release_date": 1,
                "imdb": 1
            }
        },
        {
            "$group": {
                "_id": None,
                "movies": { "$push": "$$ROOT" },
                "total_movies": { "$sum": 1 }
            }
        }
    ]

    collection = Movie.get_pymongo_collection()
    cursor = await collection.aggregate(pipeline)

    result = None
    async for doc in cursor:
        result = doc

    return {
        "actor": actor,
        "total_movies": result["total_movies"] if result else 0,
        "movies": result["movies"] if result else []
    }