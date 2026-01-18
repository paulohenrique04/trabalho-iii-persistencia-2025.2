from datetime import datetime
from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Query, status
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate
from typing import Optional

from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=User)
async def create_user(user_data: dict):
    """Cria um novo usuário"""
    user = User(**user_data)
    await user.insert()
    return user

@router.get("/{user_id}", response_model=User)
async def get_user_by_id(user_id: PydanticObjectId):
    """a) Consulta por ID"""
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

@router.get("/", response_model=Page[User])
async def get_users(country: Optional[str] = None):
    """Lista paginada de usuários"""
    query = {}
    if country:
        query["country"] = country
    return await apaginate(User.find(query))

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: PydanticObjectId, user_data: dict):
    """Atualiza usuário"""
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    for key, value in user_data.items():
        if hasattr(user, key):
            setattr(user, key, value)
    
    await user.save()
    return user

@router.delete("/{user_id}")
async def delete_user(user_id: PydanticObjectId):
    """Deleta usuário"""
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    await user.delete()
    return {"message": "Usuário deletado"}

# CONSULTAS REQUERIDAS
@router.get("/search/email")
async def search_by_email(email_part: str):
    """c) Busca parcial no email"""
    users = await User.find({"email": {"$regex": email_part, "$options": "i"}}).to_list()
    return users

@router.get("/country/{country}/count")
async def count_users_by_country(country: str):
    """ Contagem por país"""
    count = await User.find(User.country == country).count()
    return {"country": country, "total_users": count}

@router.get("/statistics/summary")
async def get_users_summary():
    """ Agregação simples"""
    pipeline = [
        {
            "$group": {
                "_id": None,
                "total_users": {"$sum": 1},
                "countries": {"$addToSet": "$country"},
                "cities": {"$addToSet": "$city"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "total_users": 1,
                "unique_countries": {"$size": "$countries"},
                "unique_cities": {"$size": "$cities"}
            }
        }
    ]  
    result = await User.aggregate(pipeline).to_list()
    return result[0] if result else {"total_users": 0, "unique_countries": 0, "unique_cities": 0}
