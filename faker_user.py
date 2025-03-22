from faker import Faker
import random

# Inicializa o gerador de dados falsos
fake = Faker()

# Configurações
num_users = 100  # Número de usuários a serem gerados
country_list = ['BR', 'US', 'FR', 'DE', 'IT', 'AF', 'CA', 'GB', 'ES', 'JP', 'CN', 'IN', 'AU', 'RU', 'MX', 'AR', 'ZA', 'PT', 'NL', 'SE', 'CH', 'KR', 'TR', 'NZ', 'AE', 'SA', 'EG', 'TH', 'SG', 'MY', 'ID', 'PH', 'VN', 'CL', 'CO', 'PE', 'PL', 'GR', 'HU', 'AT', 'DK', 'NO', 'FI', 'BE', 'CZ', 'IE', 'IL', 'HK', 'TW', 'PK', 'BD', 'IR', 'IQ', 'KW', 'QA', 'OM', 'NG', 'KE', 'GH', 'UG', 'TZ', 'ET', 'MA', 'DZ', 'JO', 'LB', 'SY', 'YE', 'LY', 'TN', 'CM', 'CI', 'SN', 'MG', 'MU', 'KM', 'SC', 'RW', 'BI', 'SS', 'ZW', 'ZM', 'AO', 'NA', 'BW', 'LS', 'SZ', 'MZ', 'CG', 'GA', 'GQ', 'BJ', 'NE', 'ML', 'BF', 'LR', 'SL', 'GN', 'GW', 'CV', 'ST', 'TD', 'CF', 'SO', 'DJ', 'ER', 'GM', 'LR', 'TG', 'BJ', 'MW', 'MZ', 'BW', 'NA', 'SZ', 'LS', 'ZW', 'ZM', 'AO', 'MZ', 'BW', 'NA', 'SZ', 'LS', 'ZW', 'ZM']  # Exemplos de países

# Função para gerar uma URL de imagem com "spotify"
def generate_spotify_image_url(value=""):
    return f"https://source.unsplash.com/featured/?spotify_{value}.jpeg"

# Abre o arquivo para escrita
with open('insert_users.txt', 'w') as file:
    for _ in range(num_users):
        user_id = None  # AUTO_INCREMENT será gerado pelo banco de dados
        username = fake.user_name()
        email = fake.unique.email()
        phone = fake.phone_number()
        password = fake.password()
        date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=99)  # Idade mínima de 18 anos
        country = random.choice(country_list)
        subscription_type = random.choice(['Free', 'Premium', 'Premium Family', 'Premium Student'])
        profile_image = generate_spotify_image_url(username)  # Gera a URL da imagem do Spotify

        # Cria a linha de insert
        insert_statement = (
            f"INSERT INTO users (username, email, phone, password, date_of_birth, "
            f"country, subscription_type, profile_image) VALUES ("
            f"'{username}', '{email}', '{phone}', '{password}', '{date_of_birth}', "
            f"'{country}', '{subscription_type}', '{profile_image}');\n"
        )

        # Escreve a linha no arquivo
        file.write(insert_statement)

print(f"{num_users} usuários foram gerados e salvos em 'insert_users.txt'.")
