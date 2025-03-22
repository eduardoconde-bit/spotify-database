import faker
import random

fake = faker.Faker()


def fake_liked_songs(users, songs):
    '''
    param: users
    quantidade exatas de usuários cadastradas no banco de dados
    param: songs
    quantidade exata de músicas cadastradas no banco de dados
    '''
    with open('insert_liked_songs.txt', 'w') as file:
        for _ in range(1, users+1):
            number_likes = set()
            #Escolhe aleatoriamente quantos likes e as músicas "likadas" dentro do intervalo de músicas do banco.
            for nl in range(1, random.randint(1, 7)+1):
                number_likes.add(random.randint(1, songs))

            user_id = _
            for song_id in number_likes:
                # Cria a linha de insert
                insert_statement = (f"INSERT INTO liked_songs (user_id, song_id) VALUES ('{user_id}', '{song_id}');\n")
                # Escreve a linha no arquivo
                file.write(insert_statement)

fake_liked_songs(100, 33454)