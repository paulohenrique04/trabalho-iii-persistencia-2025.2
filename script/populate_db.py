import asyncio
from datetime import date, datetime
from random import choice, uniform

from app.core.database import init_db, close_db
from app.models.actor import Actor
from app.models.genre import Genre
from app.models.movie import Movie
from app.models.user import User
from app.models.review import Review
from app.models.watchlist import Watchlist


async def seed_database():
    await init_db()

    # =====================================================
    # GÊNEROS
    # =====================================================
    genres_data = [
        "Drama",
        "Ação",
        "Comédia",
        "Crime",
        "Suspense",
        "Romance",
        "Ficção Científica",
        "Terror",
        "Documentário",
        "Animação",
    ]

    genres = []
    for name in genres_data:
        genre = Genre(name=name)
        await genre.insert()
        genres.append(genre)

    # =====================================================
    # ATORES (todos os campos preenchidos)
    # =====================================================
    actors_data = [
        {
            "name": "Leonardo DiCaprio",
            "birth_date": "1974-11-11",
            "nationality": "Americano",
            "biography": "Ator e produtor americano vencedor do Oscar.",
            "height_cm": 183,
            "awards": ["Oscar", "Globo de Ouro", "BAFTA"],
            "instagram": "https://www.instagram.com/leonardodicaprio",
            "know_for": "Titanic",
            "indications": ["Oscar", "Globo de Ouro"],
        },
        {
            "name": "Brad Pitt",
            "birth_date": "1963-12-18",
            "nationality": "Americano",
            "biography": "Ator e produtor americano.",
            "height_cm": 180,
            "awards": ["Oscar", "Globo de Ouro"],
            "instagram": "https://www.instagram.com/bradpittofficial",
            "know_for": "Clube da Luta",
            "indications": ["Oscar"],
        },
        {
            "name": "Morgan Freeman",
            "birth_date": "1937-06-01",
            "nationality": "Americano",
            "biography": "Ator e narrador americano.",
            "height_cm": 188,
            "awards": ["Oscar"],
            "instagram": "",
            "know_for": "Um Sonho de Liberdade",
            "indications": ["Oscar"],
        },
        {
            "name": "Christian Bale",
            "birth_date": "1974-01-30",
            "nationality": "Britânico",
            "biography": "Ator britânico conhecido por papéis intensos.",
            "height_cm": 183,
            "awards": ["Oscar"],
            "instagram": "",
            "know_for": "Batman",
            "indications": ["Oscar", "BAFTA"],
        },
        {
            "name": "Robert De Niro",
            "birth_date": "1943-08-17",
            "nationality": "Americano",
            "biography": "Ator americano lendário.",
            "height_cm": 177,
            "awards": ["Oscar"],
            "instagram": "",
            "know_for": "Taxi Driver",
            "indications": ["Oscar"],
        },
        {
            "name": "Al Pacino",
            "birth_date": "1940-04-25",
            "nationality": "Americano",
            "biography": "Ator americano consagrado.",
            "height_cm": 170,
            "awards": ["Oscar"],
            "instagram": "",
            "know_for": "O Poderoso Chefão",
            "indications": ["Oscar"],
        },
        {
            "name": "Fernanda Montenegro",
            "birth_date": "1929-10-16",
            "nationality": "Brasileira",
            "biography": "Atriz brasileira reconhecida internacionalmente.",
            "height_cm": 165,
            "awards": ["Emmy Internacional"],
            "instagram": "",
            "know_for": "Central do Brasil",
            "indications": ["Oscar"],
        },
        {
            "name": "Selton Mello",
            "birth_date": "1972-12-30",
            "nationality": "Brasileiro",
            "biography": "Ator e diretor brasileiro.",
            "height_cm": 173,
            "awards": ["Grande Prêmio do Cinema Brasileiro"],
            "instagram": "https://www.instagram.com/seltonmello",
            "know_for": "O Auto da Compadecida",
            "indications": ["Grande Prêmio do Cinema Brasileiro"],
        },
        {
            "name": "Matheus Nachtergaele",
            "birth_date": "1969-01-03",
            "nationality": "Brasileiro",
            "biography": "Ator brasileiro de teatro e cinema.",
            "height_cm": 172,
            "awards": ["Grande Prêmio do Cinema Brasileiro"],
            "instagram": "",
            "know_for": "O Auto da Compadecida",
            "indications": ["Grande Prêmio do Cinema Brasileiro"],
        },
        {
            "name": "Wagner Moura",
            "birth_date": "1976-06-27",
            "nationality": "Brasileiro",
            "biography": "Ator brasileiro com carreira internacional.",
            "height_cm": 180,
            "awards": ["Festival de Cannes"],
            "instagram": "",
            "know_for": "Tropa de Elite",
            "indications": ["Emmy"],
        },
    ]

    actors = []
    for data in actors_data:
        actor = Actor(**data)
        await actor.insert()
        actors.append(actor)

    # =====================================================
    # FILMES (todos os campos preenchidos)
    # =====================================================
    movies_data = [
        {
            "title": "Cidade de Deus",
            "original_title": "Cidade de Deus",
            "synopsis": "A ascensão do crime organizado em uma favela carioca.",
            "release_date": date(2002, 8, 30),
            "duration_minutes": 130,
            "age_rating": "18",
            "director": "Fernando Meirelles",
            "imdb": 8.6,
        },
        {
            "title": "Central do Brasil",
            "original_title": "Central do Brasil",
            "synopsis": "Uma viagem transformadora pelo interior do Brasil.",
            "release_date": date(1998, 4, 3),
            "duration_minutes": 113,
            "age_rating": "12",
            "director": "Walter Salles",
            "imdb": 8.0,
        },
        {
            "title": "Tropa de Elite",
            "original_title": "Tropa de Elite",
            "synopsis": "A rotina do BOPE no Rio de Janeiro.",
            "release_date": date(2007, 10, 12),
            "duration_minutes": 115,
            "age_rating": "18",
            "director": "José Padilha",
            "imdb": 8.0,
        },
        {
            "title": "Clube da Luta",
            "original_title": "Fight Club",
            "synopsis": "Um homem cria um clube secreto de lutas.",
            "release_date": date(1999, 10, 15),
            "duration_minutes": 139,
            "age_rating": "18",
            "director": "David Fincher",
            "imdb": 8.8,
        },
        {
            "title": "O Poderoso Chefão",
            "original_title": "The Godfather",
            "synopsis": "A saga da família Corleone.",
            "release_date": date(1972, 3, 24),
            "duration_minutes": 175,
            "age_rating": "18",
            "director": "Francis Ford Coppola",
            "imdb": 9.2,
        },
    ]

    movies = []
    for data in movies_data:
        movie = Movie(
            **data,
            actors=[choice(actors) for _ in range(3)],
            genres=[choice(genres) for _ in range(2)],
        )
        await movie.insert()
        movies.append(movie)

    # =====================================================
    # USUÁRIOS (todos os campos preenchidos)
    # =====================================================
    users = []
    for i in range(10):
        user = User(
            username=f"user{i}",
            email=f"user{i}@example.com",
            password="senha123",
            bio="Usuário fictício para testes",
            birthdate=datetime(1995, 1, 1),
            gender="Outro",
            country="Brasil",
            telephone=f"+55 11 99999-00{i}",
            city="São Paulo",
        )
        await user.insert()
        users.append(user)

    # =====================================================
    # REVIEWS
    # =====================================================
    for _ in range(10):
        review = Review(
            movie=choice(movies),
            user=choice(users),
            rating=round(uniform(3.0, 5.0), 1),
            title="Ótimo filme",
            content="História envolvente e excelente atuação.",
            spoiler=False,
        )
        await review.insert()

    # =====================================================
    # WATCHLIST
    # =====================================================
    for _ in range(10):
        watchlist = Watchlist(
            user=choice(users),
            movie=choice(movies),
            notes="Assistir no final de semana",
        )
        await watchlist.insert()

    await close_db()
    print("✅ Seed completo executado com sucesso!")


if __name__ == "__main__":
    asyncio.run(seed_database())
