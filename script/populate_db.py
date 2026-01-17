import asyncio
from datetime import date, datetime
from app.core.database import init_db, close_db
from app.models.actor import Actor
from app.models.genre import Genre
from app.models.movie import Movie
from app.models.user import User
from app.models.review import Review
from app.models.watchlist import Watchlist


async def seed_genres():
    genres = [
        "Drama", "Ação", "Comédia", "Suspense", "Terror",
        "Ficção Científica", "Romance", "Animação",
        "Documentário", "Crime"
    ]
    docs = [Genre(name=g) for g in genres]
    await Genre.insert_many(docs)
    return docs


async def seed_actors():
    actors_data = [
        # Brasileiros
        ("Wagner Moura", "Brasil"),
        ("Sônia Braga", "Brasil"),
        ("Seu Jorge", "Brasil"),
        ("Matheus Nachtergaele", "Brasil"),
        ("Fernanda Montenegro", "Brasil"),
        ("Rodrigo Santoro", "Brasil"),

        # Internacionais
        ("Joaquin Phoenix", "Estados Unidos"),
        ("Leonardo DiCaprio", "Estados Unidos"),
        ("Brad Pitt", "Estados Unidos"),
        ("Natalie Portman", "Estados Unidos"),
        ("Christian Bale", "Reino Unido"),
        ("Heath Ledger", "Austrália"),
        ("Meryl Streep", "Estados Unidos"),
        ("Tom Hanks", "Estados Unidos"),
        ("Al Pacino", "Estados Unidos"),
        ("Robert De Niro", "Estados Unidos"),
        ("Scarlett Johansson", "Estados Unidos"),
        ("Keanu Reeves", "Canadá"),
        ("Charlize Theron", "África do Sul"),
        ("Denzel Washington", "Estados Unidos"),
    ]

    docs = [
        Actor(
            name=name,
            nationality=country,
            biography=f"{name} é um ator renomado.",
            awards=[],
            indications=[]
        )
        for name, country in actors_data
    ]

    await Actor.insert_many(docs)
    return docs


async def seed_users():
    users = [
        ("paulo", "paulo@email.com", "Brasil", "Fortaleza"),
        ("ana", "ana@email.com", "Brasil", "São Paulo"),
        ("joao", "joao@email.com", "Brasil", "Rio de Janeiro"),
        ("maria", "maria@email.com", "Portugal", "Lisboa"),
        ("lucas", "lucas@email.com", "Estados Unidos", "New York"),
        ("carla", "carla@email.com", "França", "Paris"),
        ("pedro", "pedro@email.com", "Brasil", "Recife"),
        ("julia", "julia@email.com", "Canadá", "Toronto"),
        ("marcos", "marcos@email.com", "Brasil", "Salvador"),
        ("laura", "laura@email.com", "Alemanha", "Berlim"),
    ]

    docs = [
        User(
            username=u,
            email=e,
            password="hashedpassword",
            country=c,
            city=city,
            created_at=datetime.utcnow()
        )
        for u, e, c, city in users
    ]

    await User.insert_many(docs)
    return docs


async def seed_movies(actors, genres):
    movies_data = [
        ("Cidade de Deus", date(2002, 8, 30), 130, "Fernando Meirelles"),
        ("Tropa de Elite", date(2007, 10, 12), 115, "José Padilha"),
        ("Central do Brasil", date(1998, 4, 3), 113, "Walter Salles"),
        ("Carandiru", date(2003, 3, 28), 145, "Hector Babenco"),
        ("O Auto da Compadecida", date(2000, 9, 15), 104, "Guel Arraes"),

        ("Joker", date(2019, 10, 3), 122, "Todd Phillips"),
        ("The Dark Knight", date(2008, 7, 18), 152, "Christopher Nolan"),
        ("Inception", date(2010, 7, 16), 148, "Christopher Nolan"),
        ("Fight Club", date(1999, 10, 15), 139, "David Fincher"),
        ("The Matrix", date(1999, 3, 31), 136, "Lana Wachowski"),
        ("Forrest Gump", date(1994, 7, 6), 142, "Robert Zemeckis"),
        ("Pulp Fiction", date(1994, 10, 14), 154, "Quentin Tarantino"),
        ("Gladiator", date(2000, 5, 5), 155, "Ridley Scott"),
        ("The Godfather", date(1972, 3, 24), 175, "Francis Ford Coppola"),
        ("Se7en", date(1995, 9, 22), 127, "David Fincher"),
        ("Black Swan", date(2010, 12, 17), 108, "Darren Aronofsky"),
        ("Interstellar", date(2014, 11, 7), 169, "Christopher Nolan"),
        ("The Shawshank Redemption", date(1994, 9, 23), 142, "Frank Darabont"),
        ("Whiplash", date(2014, 10, 10), 106, "Damien Chazelle"),
        ("Parasite", date(2019, 5, 30), 132, "Bong Joon-ho"),
    ]

    docs = []
    for title, release, duration, director in movies_data:
        movie = Movie(
            title=title,
            synopsis=f"{title} é um filme aclamado pela crítica.",
            release_date=release,
            duration_minutes=duration,
            director=director,
            imdb=8.0,
            actors=actors[:3],
            genres=genres[:2],
        )
        docs.append(movie)

    await Movie.insert_many(docs)
    return docs


async def seed_reviews(users, movies):
    reviews = []
    for i in range(10):
        reviews.append(
            Review(
                user=users[i],
                movie=movies[i],
                rating=4.5,
                title="Excelente filme",
                content="Uma obra-prima do cinema.",
                spoiler=False,
            )
        )

    await Review.insert_many(reviews)


async def seed_watchlists(users, movies):
    watchlists = []
    for i in range(10):
        watchlists.append(
            Watchlist(
                user=users[i],
                movie=movies[-(i + 1)],
                notes="Quero assistir novamente",
            )
        )

    await Watchlist.insert_many(watchlists)


async def main():
    await init_db()

    genres = await seed_genres()
    actors = await seed_actors()
    users = await seed_users()
    movies = await seed_movies(actors, genres)

    await seed_reviews(users, movies)
    await seed_watchlists(users, movies)

    await close_db()
    print("✅ Banco de dados populado com sucesso!")


if __name__ == "__main__":
    asyncio.run(main())
