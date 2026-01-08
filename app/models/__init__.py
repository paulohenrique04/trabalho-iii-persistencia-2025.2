from app.models.actor import Actor
from app.models.movie import Movie
from app.models.genre import Genre
from app.models.user import User
from app.models.review import Review
from app.models.watchlist import Watchlist

Actor.model_rebuild()
Movie.model_rebuild()
Genre.model_rebuild()
User.model_rebuild()
Review.model_rebuild()
Watchlist.model_rebuild()
