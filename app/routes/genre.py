from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate
from app.models.genre import Genre, GenreCreate

router = APIRouter(
    prefix="/genres",
    tags=["Genres"],
)

@router.get("/", response_model=Page[Genre])
async def get_genres() -> Page[Genre]:
    """
    Retorna uma lista paginada de gêneros.
    """
    return await apaginate(Genre.find_all())

@router.get("/{genre_id}", response_model=Genre)
async def get_genre_by_id(genre_id: PydanticObjectId) -> Genre:
    """
    Retorna um gênero pelo seu ID.
    """
    genre = await Genre.get(genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Gênero não encontrado")
    return genre

@router.post("/", response_model=Genre, status_code=201)
async def create_genre(genre: GenreCreate) -> Genre:
    """
    Cria um novo gênero.
    """
    genre_obj = Genre(**genre.model_dump())
    await genre_obj.insert()
    genre_inserted = await Genre.get(genre_obj.id)
    if not genre_inserted:
        raise HTTPException(status_code=500, detail="Erro ao criar o gênero")
    
    return genre_inserted

@router.put("/{genre_id}", response_model=Genre)
async def update_genre(genre_id: PydanticObjectId, genre_data: dict) -> Genre:
    """
    Atualiza um gênero existente.
    """ 
    genre = await Genre.get(genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Gênero não encontrado")
    
    for key, value in genre_data.items():
        setattr(genre, key, value)
    
    await genre.save()
    return genre

@router.delete("/{genre_id}")
async def delete_genre(genre_id: PydanticObjectId) -> dict:
    """
    Deleta um gênero existente.
    """
    genre = await Genre.get(genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Gênero não encontrado")
    
    await genre.delete()
    return {"mensagem": "Gênero deletado com sucesso"}