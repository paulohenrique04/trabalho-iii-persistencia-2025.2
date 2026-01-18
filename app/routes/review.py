from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Query, status
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate

from app.models import Movie, Review, User
from app.models.review import ReviewUpdate, ReviewCreate

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", response_model=Review, status_code=status.HTTP_201_CREATED)
async def create_review(review: ReviewCreate) -> Review:
    """Cria uma nova review (valida existência do filme)"""
    movie = await Movie.get(review.movie)
    if not movie:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    
    user = await User.get(review.user)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    review_insert = Review(
        **review.model_dump(exclude={"movie", "user"}),
        movie=movie,
        user=user
    )

    await review_insert.insert()
    return review_insert


@router.get("/{review_id}", response_model=Review)
async def get_review_by_id(review_id: PydanticObjectId) -> Review:
    """Retorna uma review pelo seu ID"""
    review = await Review.get(review_id, fetch_links=True)
    if not review:
        raise HTTPException(status_code=404, detail="Review não encontrada")
    return review

@router.get("/", response_model=Page[Review])
async def get_reviews(
    movie_id: PydanticObjectId | None = Query(None),
    min_rating: float | None = Query(None, ge=1.0, le=10.0),
) -> Page[Review]:

    query = {}

    if movie_id:
        query["movie.$id"] = movie_id

    if min_rating:
        query["rating"] = {"$gte": min_rating}

    page = await apaginate(Review.find(query))

    for p in page.items:
        await p.fetch_all_links()

    return page 


@router.put("/{review_id}", response_model=Review)
async def update_review(review_id: PydanticObjectId, review_data: ReviewUpdate) -> Review:
    """Atualiza uma review existente"""
    review = await Review.get(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review não encontrada")

    for key, value in review_data.model_dump(exclude_unset=True).items():
        if key == "movie" and value is not None:
            movie = await Movie.get(value)
            if not movie:
                raise HTTPException(status_code=404, detail="Filme não encontrado")
            review.movie = movie
        elif key == "user" and value is not None:
            user = await User.get(value)
            if not user:
                raise HTTPException(status_code=404, detail="Usuário não encontrado")
            review.user = user
        else:
            setattr(review, key, value)

    await review.save()
    return await Review.get(review_id, fetch_links=True)


@router.delete("/{review_id}")
async def delete_review(review_id: PydanticObjectId) -> dict:
    """Deleta uma review existente"""
    review = await Review.get(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review não encontrada")
    
    await review.delete()
    return {"mensagem": "Review deletada com sucesso"}