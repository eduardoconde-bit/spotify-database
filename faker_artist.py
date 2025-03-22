from faker import Faker
import random
import datetime

# Inicializa o gerador de dados falsos
fake = Faker()

# Configurações
num_artists = 1000  # Número de artistas a serem gerados
country_list = ['BR', 'US', 'FR', 'DE', 'IT', 'AF', 'CA', 'GB', 'ES', 'JP', 'CN', 'IN', 'AU', 'RU', 'MX', 'AR', 'ZA', 'PT', 'NL', 'SE', 'CH', 'KR', 'TR', 'NZ', 'AE', 'SA', 'EG', 'TH', 'SG', 'MY', 'ID', 'PH', 'VN', 'CL', 'CO', 'PE', 'PL', 'GR', 'HU', 'AT', 'DK', 'NO', 'FI', 'BE', 'CZ', 'IE', 'IL', 'HK', 'TW', 'PK', 'BD', 'IR', 'IQ', 'KW', 'QA', 'OM', 'NG', 'KE', 'GH', 'UG', 'TZ', 'ET', 'MA', 'DZ', 'JO', 'LB', 'SY', 'YE', 'LY', 'TN', 'CM', 'CI', 'SN', 'MG', 'MU', 'KM', 'SC', 'RW', 'BI', 'SS', 'ZW', 'ZM', 'AO', 'NA', 'BW', 'LS', 'SZ', 'MZ', 'CG', 'GA', 'GQ', 'BJ', 'NE', 'ML', 'BF', 'LR', 'SL', 'GN', 'GW', 'CV', 'ST', 'TD', 'CF', 'SO', 'DJ', 'ER', 'GM', 'LR', 'TG', 'BJ', 'MW', 'MZ', 'BW', 'NA', 'SZ', 'LS', 'ZW', 'ZM', 'AO', 'MZ', 'BW', 'NA', 'SZ', 'LS', 'ZW', 'ZM']  # Exemplos de países
genres = [num for num in range(1, 177)]  # IDs de gênero (exemplo: 1: Rock, 2: Pop, etc.)

#Global Counters
album_id_count = 0
music_id_count = 0

def fake_song(genre_id, artist_id):
    with open('insert_song.txt', 'a+') as file:
        for _ in range(random.choice([10, 15, 17, 25])):
            global album_id_count
            song_id = None
            title = (
                random.choice([fake.word(), ' ']) +  
                fake.color_name() +  
                random.choice([fake.word(), ' '])
            ).strip()
            duration = random.randint(60000, 600000)
            artist_id = artist_id
            genre_id = genre_id
            album_id = album_id_count
            streams = random.randint(0, 1000000)

            # Cria a linha de insert
            insert_statement = (
                f"INSERT INTO songs (title, duration, artist_id, genre_id, album_id, streams) VALUES ("
                f"'{title}', {duration}, {artist_id}, {genre_id}, {album_id}, {streams});\n"
            )

            # Escreve a linha no arquivo
            file.write(insert_statement)



def fake_album(genre_id, artist_id):
    for _ in range(random.choice([1, 2, 3])):
        global album_id_count
        album_id_count += 1
        album_id = None
        title = (
            random.choice([fake.word(), ' ']) +  
            fake.color_name() +  
            random.choice([fake.word(), ''])
        ).strip()
        release_date = fake.date_of_birth(minimum_age=18, maximum_age=65)
        type = 'album'
        image = fake.url()
        genre_id = genre_id
        artist_id = artist_id

        # Cria a linha de insert
        insert_statement = (
            f"INSERT INTO albums (title, release_date, type, image,genre_id, artist_id) VALUES ("
            f"'{title}', '{release_date}', '{type}', '{image}', {genre_id}, {artist_id});\n"
        )

        # Escreve a linha no arquivo
        file.write(insert_statement)
        fake_song(genre_id=genre_id, artist_id=artist_id)

# Abre o arquivo para escrita
with open('insert_artists.txt', 'w') as file:
    for _ in range(1, num_artists+1):
        print(_)
        artist_id = _  # AUTO_INCREMENT será gerado pelo banco de dados
        name = fake.name()
        bio = fake.text(max_nb_chars=50)  # Geração de biografia curta
        country = random.choice(country_list)
        date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=100)  # Idade mínima de 18 anos
        genre_id = random.choice(genres)  # Seleciona um gênero aleatório

        # Cria a linha de insert
        insert_statement = (
            f"INSERT INTO artists (artist_id, name, bio, country, date_of_birth, genre_id) VALUES ("
            f"'{artist_id}', '{name}', '{bio}', '{country}', '{date_of_birth}', {genre_id});\n"
        )

        # Escreve a linha no arquivo
        file.write(insert_statement)
        fake_album(genre_id=genre_id, artist_id=artist_id)

        #GERAR LOGO O ARTISTA -> ALBUM (RANDOM) -> MÚSICAS SEQUENCIALMENTE

print(f"{'-'*50}\n{num_artists} artistas foram gerados e salvos em 'insert_artists.txt'. \n{'-'*50}")



'''
# Creating albums table
CREATE TABLE IF NOT EXISTS albums (
	album_id INT PRIMARY KEY AUTO_INCREMENT,
	title VARCHAR(255) NOT NULL,
	release_date DATE NOT NULL,
	type ENUM('album', 'single', 'compilation'),
	image VARCHAR(255) DEFAULT NULL,
	genre_id INT NOT NULL,
	artist_id INT NOT NULL, 
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT fk_genre_album FOREIGN KEY (genre_id) REFERENCES genres(genre_id),
	CONSTRAINT fk_artist_album FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
);
'''