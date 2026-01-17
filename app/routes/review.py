from typing import List, Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Query, status

from app.models import Movie, Review

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", response_model=Review, status_code=status.HTTP_201_CREATED)
async def create_review(review: Review):
    """Cria uma nova review (valida existência do filme)"""
    movie = await Movie.get(review.movie.ref.id)
    if not movie:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    await review.insert()
    return review


@router.get("/{review_id}", response_model=Review)
async def get_review(review_id: PydanticObjectId):
    """Busca review por ID"""
    review = await Review.get(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review não encontrada")
    return review


@router.get("/", response_model=List[Review])
async def list_reviews(
    movie_id: Optional[PydanticObjectId] = Query(None),
    min_rating: Optional[float] = Query(None, ge=1.0, le=10.0),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
):
    """Lista reviews com filtros e paginação"""
    query = {}
    if movie_id:
        query["movie.id"] = movie_id
    if min_rating:
        query["rating"] = {"$gte": min_rating}

    reviews = await Review.find(query).skip(skip).limit(limit).to_list()
    return reviews


@router.put("/{review_id}", response_model=Review)
async def update_review(review_id: PydanticObjectId, review_update: Review):
    """Atualiza review"""
    review = await Review.get(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review não encontrada")

    update_data = review_update.model_dump(exclude_unset=True)
    await review.set(update_data)
    return review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(review_id: PydanticObjectId):
    """Deleta review"""
    review = await Review.get(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review não encontrada")
    await review.delete()
    return None
    await review.delete()
    return None