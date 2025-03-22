from faker import Faker
import random

fake = Faker()

#Faker Playlist gera tanto as playlists quanto as músicas relacionadas a elas em playlist_songs

#Número de Usuários no Banco de Dados
users = 100
playlist_count = 1

def fake_liked_songs():
    for _ in range(1, users+1):
        #Número de playlists pra 1 usuário
        for pl in range(1, random.randint(1, 5)+1):
            with open('insert_playlist.txt', 'a+') as file:
                global playlist_count
                songs = set()

                #Playlist dados
                name = random.choice([fake.color_name(), fake.language_name()])
                user_id = _
                visibility = random.choice(["public", "private"])

                # Cria a linha de insert
                insert_statement = (f"INSERT INTO playlists (name, user_id, visibility) VALUES ('{name}' , {user_id}, '{visibility}');\n")
                # Escreve a linha no arquivo
                file.write(insert_statement)

                # Cria a lista de canções relacionadas a 1 playlist com quantidades aleatórias de músicas
                for ns in range(1, random.choice([5, 10, 15, 20])):
                    songs.add(random.randint(1, 33454))

                with open('insert_playlist_songs.txt', 'a+') as file:
                    playlist = playlist_count
                    for song in songs:
                        # Cria a linha de insert
                        insert_statement = (f"INSERT INTO playlist_songs (playlist_id, song_id) VALUES ({playlist}, {song});\n")
                        # Escreve a linha no arquivo
                        file.write(insert_statement)
                    playlist_count += 1

fake_liked_songs()