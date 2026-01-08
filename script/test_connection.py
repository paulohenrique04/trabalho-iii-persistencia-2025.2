import asyncio
from datetime import date

from app.core.database import init_db
from app.models.actor import Actor
from app.models.movie import Movie
from app.models.genre import Genre


async def main():
    await init_db()

    genre = Genre(name="Ficção Científica")
    await genre.insert()

    actor = Actor(
        name="Keanu Reeves",
        birth_date="1964-09-02",
        nationality="Canadense",
        biography="Ator canadense conhecido por seus papéis em filmes de ação e ficção científica.",
    )
    await actor.insert()

    movie = Movie(
        title="Matrix",
        synopsis="Um hacker descobre a verdadeira natureza da realidade.",
        release_date=date(1999, 3, 31),
        duration_minutes=136,
        age_rating="16",
        director="Lana Wachowski",
        actors=[actor],
        genres=[genre],
    )

    await movie.insert()

    print("Conexão bem-sucedida e dados inseridos! 🚀")


if __name__ == "__main__":
    asyncio.run(main())
