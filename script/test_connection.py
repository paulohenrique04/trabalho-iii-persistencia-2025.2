import asyncio
from datetime import date, datetime
from app.core.database import init_db, close_db
from app.models.actor import Actor
from app.models.genre import Genre
from app.models.movie import Movie
from app.models.user import User
from app.models.review import Review
from app.models.watchlist import Watchlist
import hashlib


async def populate_actors():
    """Popula a tabela de atores com dados reais"""
    actors_data = [
        Actor(
            name="Leonardo DiCaprio",
            birth_date="1974-11-11",
            nationality="Americano",
            biography="Leonardo Wilhelm DiCaprio é um ator, produtor cinematográfico e ambientalista americano.",
            height_cm=183.0,
            awards=["Oscar de Melhor Ator", "Globo de Ouro", "BAFTA"],
            instagram="leonardodicaprio",
            know_for="Titanic, O Lobo de Wall Street, O Regresso",
            indications=["Oscar", "Globo de Ouro", "BAFTA"]
        ),
        Actor(
            name="Meryl Streep",
            birth_date="1949-06-22",
            nationality="Americana",
            biography="Mary Louise Streep é uma atriz americana, frequentemente descrita como a melhor atriz de sua geração.",
            height_cm=168.0,
            awards=["3 Oscars", "8 Globos de Ouro", "2 Emmys"],
            instagram="merylstreep",
            know_for="A Dama de Ferro, O Diabo Veste Prada, Kramer vs. Kramer",
            indications=["21 indicações ao Oscar"]
        ),
        Actor(
            name="Tom Hanks",
            birth_date="1956-07-09",
            nationality="Americano",
            biography="Thomas Jeffrey Hanks é um ator, produtor, roteirista e diretor americano.",
            height_cm=183.0,
            awards=["2 Oscars", "4 Globos de Ouro", "7 Emmys"],
            instagram="tomhanks",
            know_for="Forrest Gump, Náufrago, O Resgate do Soldado Ryan",
            indications=["Oscar", "Globo de Ouro"]
        ),
        Actor(
            name="Scarlett Johansson",
            birth_date="1984-11-22",
            nationality="Americana",
            biography="Scarlett Ingrid Johansson é uma atriz e cantora americana.",
            height_cm=160.0,
            awards=["BAFTA", "Tony Award", "Saturn Awards"],
            instagram="scarlett.johansson.fan",
            know_for="Viúvas Negras, Casamento Grego, Lucy",
            indications=["2 indicações ao Oscar"]
        ),
        Actor(
            name="Joaquin Phoenix",
            birth_date="1974-10-28",
            nationality="Americano",
            biography="Joaquin Rafael Phoenix é um ator, produtor, ativista e ambientalista americano.",
            height_cm=173.0,
            awards=["Oscar de Melhor Ator", "Globo de Ouro", "BAFTA"],
            instagram="joaquinphoenix",
            know_for="Coringa, Gladiador, Ela",
            indications=["Oscar", "Globo de Ouro"]
        )
    ]
    
    for actor in actors_data:
        await actor.insert()
    
    print(f"✅ {len(actors_data)} atores inseridos com sucesso!")
    return actors_data


async def populate_genres():
    """Popula a tabela de gêneros"""
    genres_data = [
        Genre(name="Ação"),
        Genre(name="Drama"),
        Genre(name="Comédia"),
        Genre(name="Ficção Científica"),
        Genre(name="Terror"),
        Genre(name="Romance"),
        Genre(name="Aventura"),
        Genre(name="Suspense"),
        Genre(name="Fantasia"),
        Genre(name="Documentário")
    ]
    
    for genre in genres_data:
        await genre.insert()
    
    print(f"✅ {len(genres_data)} gêneros inseridos com sucesso!")
    return genres_data


async def populate_users():
    """Popula a tabela de usuários"""
    users_data = [
        User(
            username="maria_silva",
            email="maria.silva@email.com",
            password=hashlib.sha256("Senha123".encode()).hexdigest(),
            bio="Apaixonada por cinema clássico e filmes independentes.",
            birthdate=datetime(1990, 5, 15),
            gender="Feminino",
            country="Brasil",
            telephone="+55 11 99999-8888",
            city="São Paulo"
        ),
        User(
            username="joao_santos",
            email="joao.santos@email.com",
            password=hashlib.sha256("Senha456".encode()).hexdigest(),
            bio="Cinéfilo e crítico amador, especialista em filmes de ficção científica.",
            birthdate=datetime(1985, 8, 22),
            gender="Masculino",
            country="Portugal",
            telephone="+351 912 345 678",
            city="Lisboa"
        ),
        User(
            username="ana_oliveira",
            email="ana.oliveira@email.com",
            password=hashlib.sha256("Senha789".encode()).hexdigest(),
            bio="Adoro filmes de comédia romântica e documentários.",
            birthdate=datetime(1995, 3, 10),
            gender="Feminino",
            country="Brasil",
            telephone="+55 21 98888-7777",
            city="Rio de Janeiro"
        ),
        User(
            username="pedro_fernandes",
            email="pedro.fernandes@email.com",
            password=hashlib.sha256("Senha101".encode()).hexdigest(),
            bio="Fascinado por cinema europeu e diretores autorais.",
            birthdate=datetime(1988, 11, 30),
            gender="Masculino",
            country="Espanha",
            telephone="+34 600 123 456",
            city="Madrid"
        ),
        User(
            username="carla_martins",
            email="carla.martins@email.com",
            password=hashlib.sha256("Senha202".encode()).hexdigest(),
            bio="Crítica de cinema profissional, especializada em animação.",
            birthdate=datetime(1992, 7, 18),
            gender="Feminino",
            country="França",
            telephone="+33 6 12 34 56 78",
            city="Paris"
        )
    ]
    
    for user in users_data:
        await user.insert()
    
    print(f"✅ {len(users_data)} usuários inseridos com sucesso!")
    return users_data


async def populate_movies(actors, genres):
    """Popula a tabela de filmes"""
    movies_data = [
        Movie(
            title="Titanic",
            synopsis="Um romance épico entre uma jovem aristocrata e um artista pobre a bordo do navio Titanic.",
            release_date=date(1997, 12, 19),
            duration_minutes=195,
            age_rating="12",
            director="James Cameron",
            original_title="Titanic",
            language="Inglês",
            actors=[actors[0]],  # Leonardo DiCaprio
            genres=[genres[1], genres[5]]  # Drama, Romance
        ),
        Movie(
            title="O Diabo Veste Prada",
            synopsis="Uma jovem jornalista começa a trabalhar como assistente da temida editora de uma revista de moda.",
            release_date=date(2006, 6, 30),
            duration_minutes=109,
            age_rating="10",
            director="David Frankel",
            original_title="The Devil Wears Prada",
            language="Inglês",
            actors=[actors[1]],  # Meryl Streep
            genres=[genres[1], genres[2]]  # Drama, Comédia
        ),
        Movie(
            title="Forrest Gump",
            synopsis="A história de um homem simples que testemunha e influencia eventos históricos nos EUA.",
            release_date=date(1994, 7, 6),
            duration_minutes=142,
            age_rating="12",
            director="Robert Zemeckis",
            original_title="Forrest Gump",
            language="Inglês",
            actors=[actors[2]],  # Tom Hanks
            genres=[genres[1], genres[2]]  # Drama, Comédia
        ),
        Movie(
            title="Coringa",
            synopsis="A transformação de um comediante fracassado em um criminoso psicótico em Gotham City.",
            release_date=date(2019, 10, 4),
            duration_minutes=122,
            age_rating="16",
            director="Todd Phillips",
            original_title="Joker",
            language="Inglês",
            actors=[actors[4]],  # Joaquin Phoenix
            genres=[genres[1], genres[7]]  # Drama, Suspense
        ),
        Movie(
            title="Vingadores: Ultimato",
            synopsis="Os Vingadores restantes tentam desfazer as ações de Thanos para restaurar a ordem no universo.",
            release_date=date(2019, 4, 26),
            duration_minutes=181,
            age_rating="12",
            director="Anthony Russo, Joe Russo",
            original_title="Avengers: Endgame",
            language="Inglês",
            actors=[actors[3]],  # Scarlett Johansson
            genres=[genres[0], genres[3], genres[8]]  # Ação, Ficção Científica, Fantasia
        )
    ]
    
    for movie in movies_data:
        await movie.insert()
    
    print(f"✅ {len(movies_data)} filmes inseridos com sucesso!")
    return movies_data


async def populate_reviews(users, movies):
    """Popula a tabela de reviews"""
    reviews_data = [
        Review(
            movie=movies[0],  # Titanic
            user=users[0],    # maria_silva
            rating=4.5,
            content="Um clássico atemporal! A química entre os protagonistas é incrível.",
            title="Romance inesquecível",
            spoiler=False
        ),
        Review(
            movie=movies[1],  # O Diabo Veste Prada
            user=users[1],    # joao_santos
            rating=4.0,
            content="Meryl Streep está brilhante como sempre. Um filme divertido e inteligente.",
            title="Excelente atuação",
            spoiler=False
        ),
        Review(
            movie=movies[2],  # Forrest Gump
            user=users[2],    # ana_oliveira
            rating=5.0,
            content="Um dos melhores filmes já feitos. Tom Hanks é perfeito!",
            title="Obra-prima",
            spoiler=True
        ),
        Review(
            movie=movies[3],  # Coringa
            user=users[3],    # pedro_fernandes
            rating=4.8,
            content="Joaquin Phoenix entrega uma atuação magistral. Filme perturbador e necessário.",
            title="Atuação impressionante",
            spoiler=True
        ),
        Review(
            movie=movies[4],  # Vingadores: Ultimato
            user=users[4],    # carla_martins
            rating=4.2,
            content="Um final épico para a saga. Momentos emocionantes e muita ação.",
            title="Final satisfatório",
            spoiler=True
        ),
        # Mais algumas reviews para diversificar
        Review(
            movie=movies[0],  # Titanic
            user=users[2],    # ana_oliveira
            rating=4.0,
            content="Linda história de amor, mas um pouco longa demais.",
            title="Bonito mas extenso",
            spoiler=False
        ),
        Review(
            movie=movies[3],  # Coringa
            user=users[0],    # maria_silva
            rating=4.5,
            content="Filme intenso que faz refletir sobre a sociedade.",
            title="Profundo e inquietante",
            spoiler=False
        )
    ]
    
    for review in reviews_data:
        await review.insert()
    
    print(f"✅ {len(reviews_data)} reviews inseridos com sucesso!")
    return reviews_data


async def populate_watchlists(users, movies):
    """Popula a tabela de watchlists"""
    watchlists_data = [
        Watchlist(
            user=users[0],    # maria_silva
            movie=movies[1],  # O Diabo Veste Prada
            notes="Assistir com as amigas no fim de semana"
        ),
        Watchlist(
            user=users[1],    # joao_santos
            movie=movies[4],  # Vingadores: Ultimato
            notes="Reassistir antes do próximo filme do MCU"
        ),
        Watchlist(
            user=users[2],    # ana_oliveira
            movie=movies[0],  # Titanic
            notes="Clássico para ver novamente"
        ),
        Watchlist(
            user=users[3],    # pedro_fernandes
            movie=movies[3],  # Coringa
            notes="Estudar a atuação de Joaquin Phoenix"
        ),
        Watchlist(
            user=users[4],    # carla_martins
            movie=movies[2],  # Forrest Gump
            notes="Para aula de cinema"
        ),
        # Adicionando mais filmes na watchlist de alguns usuários
        Watchlist(
            user=users[0],    # maria_silva
            movie=movies[3],  # Coringa
            notes="Ver com atenção"
        ),
        Watchlist(
            user=users[1],    # joao_santos
            movie=movies[0],  # Titanic
            notes="Para entender referências culturais"
        )
    ]
    
    for watchlist in watchlists_data:
        await watchlist.insert()
    
    print(f"✅ {len(watchlists_data)} watchlists inseridas com sucesso!")
    return watchlists_data


async def main():
    """Função principal para popular o banco de dados"""
    try:
        # Inicializar conexão com o banco
        print("🔄 Inicializando conexão com o banco de dados...")
        await init_db()
        
        print("🚀 Iniciando população do banco de dados...")
        
        # Popular cada coleção
        actors = await populate_actors()
        genres = await populate_genres()
        users = await populate_users()
        movies = await populate_movies(actors, genres)
        reviews = await populate_reviews(users, movies)
        watchlists = await populate_watchlists(users, movies)
        
        print("\n" + "="*50)
        print("🎉 População do banco de dados concluída!")
        print("="*50)
        print(f"📊 Estatísticas:")
        print(f"   • Atores: {len(actors)}")
        print(f"   • Gêneros: {len(genres)}")
        print(f"   • Usuários: {len(users)}")
        print(f"   • Filmes: {len(movies)}")
        print(f"   • Reviews: {len(reviews)}")
        print(f"   • Watchlists: {len(watchlists)}")
        
    except Exception as e:
        print(f"❌ Erro durante a população do banco: {e}")
    finally:
        # Fechar conexão
        await close_db()


if __name__ == "__main__":
    asyncio.run(main())