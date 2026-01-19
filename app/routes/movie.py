from datetime import date
import re
from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate
from app.models.movie import Movie, MovieCreate, MoviesByGenreResponse, MovieUpdate
from app.models.actor import Actor
from app.models.genre import Genre

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)

@router.get("/", response_model=Page[Movie])
async def get_movies() -> Page[Movie]:
    """
    Retorna uma lista paginada de filmes.
    """
    page = await apaginate(Movie.find())

    for movie in page.items:
        await movie.fetch_all_links()
    
    return page

@router.get("/{movie_id}", response_model=Movie)
async def get_movie_by_id(movie_id: PydanticObjectId) -> Movie:
    """
    Retorna um filme pelo seu ID.
    """
    movie = await Movie.get(movie_id, fetch_links=True)
    if not movie:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return movie

@router.post("/", response_model=Movie, status_code=201)
async def create_movie(movie: MovieCreate) -> Movie:
    """
    Cria um novo filme.
    """
    movie_obj = Movie(**movie.model_dump())
    await movie_obj.insert()
    movie_inserted = await Movie.get(movie_obj.id, fetch_links=True)

    if not movie_inserted:
        raise HTTPException(status_code=500, detail="Erro ao criar o filme")

    return movie_inserted

@router.put("/{movie_id}", response_model=Movie)
async def update_movie(movie_id: PydanticObjectId, movie_data: MovieUpdate) -> Movie:
    movie = await Movie.get(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Filme não encontrado")

    data = movie_data.model_dump(exclude_unset=True)

    # Campos simples
    for key, value in data.items():
        if key not in {"actors", "genres"}:
            setattr(movie, key, value)

    # Atualiza atores
    if "actors" in data:
        actors = await Actor.find(
            {"_id": {"$in": data["actors"]}}
        ).to_list()
        movie.actors = actors

    # Atualiza gêneros
    if "genres" in data:
        genres = await Genre.find(
            {"_id": {"$in": data["genres"]}}
        ).to_list()
        movie.genres = genres

    await movie.save()
    return movie


@router.delete("/{movie_id}")
async def delete_movie(movie_id: PydanticObjectId) -> dict:
    """
    Deleta um filme pelo seu ID.
    """
    movie = await Movie.get(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    
    await movie.delete()
    return {"mensagem": "Filme deletado com sucesso"}

@router.get("/by-year/{year}", response_model=Page[Movie])
async def get_movies_by_year(year: int) -> Page[Movie]:
    """"
    Retorna uma lista paginada de filmes lançados em um ano específico.
    """
    start = date(year, 1, 1)
    end = date(year, 12, 31)

    return await apaginate(
        Movie.find(
            Movie.release_date >= start,
            Movie.release_date <= end,
            fetch_links=True
        )
    )

@router.get("/search/", response_model=Page[Movie])
async def search_movies(query: str) -> Page[Movie]:
    """
    Retorna uma lista paginada de filmes cujo título contenha a string de consulta.
    """
    regex = re.compile(query, re.IGNORECASE)

    return await apaginate(
        Movie.find(
            {"title": {"$regex": regex}},
            fetch_links=True
        )
    )

@router.get("/count/total")
async def get_total_movie_count() -> dict:
    """
    Retorna o número total de filmes na coleção.
    """
    count = await Movie.count()
    return {"total_filmes": count}

@router.get("/count/by-genre/", response_model=list[MoviesByGenreResponse])
async def get_movie_count_by_genre() -> list[MoviesByGenreResponse]:
    pipeline = [
        { "$unwind": "$genres" },
        {
            "$group": {
                "_id": "$genres.$id",
                "total_movies": { "$sum": 1 },
                "movies": {
                    "$push": {
                        "title": "$title",
                        "original_title": "$original_title",
                        "imdb": "$imdb"
                    }
                }
            }
        },
        {
            "$lookup": {
                "from": "genres",
                "localField": "_id",
                "foreignField": "_id",
                "as": "genre"
            }
        },
        { "$unwind": "$genre" },
        {
            "$project": {
                "_id": 0,
                "genre": "$genre.name",
                "total_movies": 1,
                "movies": 1
            }
        },
        { "$sort": { "total_movies": -1 } }
    ]


    return await Movie.aggregate(pipeline).to_list()

