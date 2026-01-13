from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate
from app.models.movie import Movie

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)

@router.get("/", response_model=Page[Movie])
async def get_movies() -> Page[Movie]:
    """
    Retorna uma lista paginada de filmes.
    """
    return await apaginate(Movie.find_all())

@router.get("/{movie_id}", response_model=Movie)
async def get_movie_by_id(movie_id: PydanticObjectId) -> Movie:
    """
    Retorna um filme pelo seu ID.
    """
    movie = await Movie.get(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return movie

@router.post("/", response_model=Movie, status_code=201)
async def create_movie(movie: Movie) -> Movie:
    """
    Cria um novo filme.
    """
    await movie.insert()
    return movie

@router.put("/{movie_id}", response_model=Movie)
async def update_movie(movie_id: PydanticObjectId, movie_data: dict) -> Movie:
    """
    Atualiza um filme existente.
    """ 
    movie = await Movie.get(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    
    for key, value in movie_data.items():
        setattr(movie, key, value)
    
    await movie.save()
    return movie

@router.delete("/{movie_id}")
async def delete_movie(movie_id: PydanticObjectId) -> dict:

    movie = await Movie.get(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    
    await movie.delete()
    return {"mensagem": "Filme deletado com sucesso"}