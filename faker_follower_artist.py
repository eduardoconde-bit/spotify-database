from faker import Faker
import random

fake = Faker()

num_f_a = 100 # Numbers of the artists generated with fake_users.py

#Gera relacionamento de "N usuários seguem N artistas"
def fake_f_a():
    with open('insert_followers_artists.txt', 'a+') as file:
        for _ in range(1, num_f_a+1):
            artist_list = set()
            for ar in range(1, random.randint(1, 5) + 1): #ar - artist range count
                artist_list.add(random.randint(1, 1000))
                print(artist_list)

            # Cria a linha de insert
            for ar in artist_list:
                insert_statement = (
                f"INSERT INTO artists_followers (user_id, artist_id) VALUES ("
                f"{_}, {ar});\n"
                )

                # Escreve a linha no arquivo
                file.write(insert_statement)

fake_f_a()