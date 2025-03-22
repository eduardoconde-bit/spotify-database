import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Substitua pelos seus próprios valores

CLIENT_ID = 'de8b4d22821f4c559b16499ee94b89d9'
CLIENT_SECRET = '7f8e04fd82704454b640577a4b4d99f4'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Lista de gêneros obtida do endpoint /recommendations/available-genre-seeds
GENRE_SEEDS = [
    "acoustic", "afrobeat", "alt-rock", "alternative", "ambient", "anime", "black-metal", "bluegrass", "blues",
    "bossanova", "brazil", "breakbeat", "british", "cantopop", "chicago-house", "children", "chill", "classical",
    "club", "comedy", "country", "dance", "dancehall", "death-metal", "deep-house", "detroit-techno", "disco",
    "drum-and-bass", "dub", "dubstep", "edm", "electro", "electronic", "emo", "folk", "forro", "french", "funk",
    "garage", "german", "gospel", "goth", "grindcore", "groove", "grunge", "guitar", "happy", "hard-rock", "hardcore",
    "hardstyle", "heavy-metal", "hip-hop", "holidays", "honky-tonk", "house", "idm", "indian", "indie", "indie-pop",
    "industrial", "iranian", "j-dance", "j-idol", "j-pop", "j-rock", "jazz", "k-pop", "kids", "latin", "latino",
    "malay", "mandopop", "metal", "metal-misc", "metalcore", "minimal-techno", "movies", "mpb", "new-age", "new-release",
    "opera", "pagode", "party", "philippines-opm", "piano", "pop", "pop-film", "post-dubstep", "power-pop",
    "progressive-house", "psych-rock", "punk", "punk-rock", "r-n-b", "rainy-day", "reggae", "reggaeton", "road-trip",
    "rock", "rock-n-roll", "rockabilly", "romance", "sad", "salsa", "samba", "sertanejo", "show-tunes",
    "singer-songwriter", "ska", "sleep", "songwriter", "soul", "soundtracks", "spanish", "study", "summer", "swedish",
    "synth-pop", "tango", "techno", "trance", "trip-hop", "turkish", "work-out", "world-music"
]

def collect_genres_from_artists():
    """Coleta gêneros associados a artistas populares."""
    genres_set = set()
    results = sp.search(q='*', type="artist", limit=50)  # Primeira busca
    for _ in range(20):  # Loop 10 vezes
        artists = results["artists"]["items"]
        for artist in artists:
            genres = artist.get("genres", [])
            genres_set.update(genres)
        if results["artists"]["next"]:
            results = sp.next(results["artists"])  # Buscar a próxima página
        else:
            break
    return genres_set

def generate_sql(genres):
    """Gera instruções SQL para inserir gêneros na tabela `genres`."""
    sql_statements = []
    for idx, genre_name in enumerate(genres, start=1):
        description = f"Gênero musical: {genre_name}"
        sql = f"INSERT INTO genres (name, description) VALUES ('{genre_name}', '{description}');"
        sql_statements.append(sql)
    return sql_statements

def main():
    # Passo 1: Coletar gêneros disponíveis via /recommendations/available-genre-seeds
    genre_seeds = set(GENRE_SEEDS)
    print(f"{len(genre_seeds)} gêneros coletados do endpoint /recommendations/available-genre-seeds.")
    
    # Passo 2: Coletar gêneros associados a artistas populares
    artist_genres = collect_genres_from_artists()
    print(f"{len(artist_genres)} gêneros coletados de artistas populares.")
    
    # Passo 3: Combinar ambos os conjuntos de gêneros
    all_genres = genre_seeds.union(artist_genres)
    print(f"{len(all_genres)} gêneros únicos após combinação.")
    
    # Passo 4: Filtrar gêneros inválidos ou muito longos
    valid_genres = [genre for genre in all_genres if len(genre) <= 25]
    print(f"{len(valid_genres)} gêneros válidos após filtragem.")
    
    # Passo 5: Organizar os gêneros em ordem alfabética
    sorted_genres = sorted(valid_genres)
    print(f"{len(sorted_genres)} gêneros organizados alfabeticamente.")
    
    # Passo 6: Gerar instruções SQL
    sql_statements = generate_sql(sorted_genres)
    
    # Passo 7: Salvar as instruções SQL em um arquivo
    with open("insert_genres.txt", "w", encoding="utf-8") as f:
        f.write("-- Instruções SQL para inserir gêneros na tabela `genres`\n")
        f.write("\n".join(sql_statements))
    
    print(f"{len(sorted_genres)} gêneros salvos em 'sql.txt'.")

# Chamar a função principal
main()
