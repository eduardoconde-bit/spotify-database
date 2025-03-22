from faker import Faker
import random

class UserGenerator:
    """Class that generates fake user data and creates SQL INSERT statements."""
    
    def __init__(self, num_users=100, output_file='insert_users.txt'):
        """
        Initialize the UserGenerator with configuration parameters.
        
        Args:
            num_users (int): Number of users to generate
            output_file (str): File path to save the SQL insert statements
        """
        # Initialize the fake data generator
        self.fake = Faker()
        
        # Configuration
        self.num_users = num_users
        self.output_file = output_file
        self.country_list = ['BR', 'US', 'FR', 'DE', 'IT', 'AF', 'CA', 'GB', 'ES', 'JP', 'CN', 'IN', 'AU', 'RU', 'MX', 
                            'AR', 'ZA', 'PT', 'NL', 'SE', 'CH', 'KR', 'TR', 'NZ', 'AE', 'SA', 'EG', 'TH', 'SG', 'MY', 
                            'ID', 'PH', 'VN', 'CL', 'CO', 'PE', 'PL', 'GR', 'HU', 'AT', 'DK', 'NO', 'FI', 'BE', 'CZ', 
                            'IE', 'IL', 'HK', 'TW', 'PK', 'BD', 'IR', 'IQ', 'KW', 'QA', 'OM', 'NG', 'KE', 'GH', 'UG', 
                            'TZ', 'ET', 'MA', 'DZ', 'JO', 'LB', 'SY', 'YE', 'LY', 'TN', 'CM', 'CI', 'SN', 'MG', 'MU', 
                            'KM', 'SC', 'RW', 'BI', 'SS', 'ZW', 'ZM', 'AO', 'NA', 'BW', 'LS', 'SZ', 'MZ', 'CG', 'GA', 
                            'GQ', 'BJ', 'NE', 'ML', 'BF', 'LR', 'SL', 'GN', 'GW', 'CV', 'ST', 'TD', 'CF', 'SO', 'DJ', 
                            'ER', 'GM', 'LR', 'TG', 'BJ', 'MW', 'MZ', 'BW', 'NA', 'SZ', 'LS', 'ZW', 'ZM', 'AO', 'MZ', 
                            'BW', 'NA', 'SZ', 'LS', 'ZW', 'ZM']
        self.subscription_types = ['Free', 'Premium', 'Premium Family', 'Premium Student']
    
    def generate_spotify_image_url(self, value=""):
        """
        Generate a URL for a Spotify-related image.
        
        Args:
            value (str): Value to append to the URL
            
        Returns:
            str: Generated image URL
        """
        return f"https://source.unsplash.com/featured/?spotify_{value}.jpeg"
    
    def generate_user(self):
        """
        Generate a single user's data.
        
        Returns:
            dict: Dictionary containing user data
        """
        username = self.fake.user_name()
        return {
            'username': username,
            'email': self.fake.unique.email(),
            'phone': self.fake.phone_number(),
            'password': self.fake.password(),
            'date_of_birth': self.fake.date_of_birth(minimum_age=18, maximum_age=99),
            'country': random.choice(self.country_list),
            'subscription_type': random.choice(self.subscription_types),
            'profile_image': self.generate_spotify_image_url(username)
        }
    
    def create_insert_statement(self, user_data):
        """
        Create an SQL INSERT statement for a user.
        
        Args:
            user_data (dict): Dictionary containing user data
            
        Returns:
            str: SQL INSERT statement
        """
        return (
            f"INSERT INTO users (username, email, phone, password, date_of_birth, "
            f"country, subscription_type, profile_image) VALUES ("
            f"'{user_data['username']}', '{user_data['email']}', '{user_data['phone']}', "
            f"'{user_data['password']}', '{user_data['date_of_birth']}', "
            f"'{user_data['country']}', '{user_data['subscription_type']}', '{user_data['profile_image']}');\n"
        )
    
    def generate_all_users(self):
        """Generate all users and write INSERT statements to a file."""
        with open(self.output_file, 'w') as file:
            for _ in range(self.num_users):
                user_data = self.generate_user()
                insert_statement = self.create_insert_statement(user_data)
                file.write(insert_statement)
        
        print(f"{self.num_users} usuários foram gerados e salvos em '{self.output_file}'.")
    
    def run(self):
        """Execute the user generation process."""
        self.generate_all_users()


if __name__ == "__main__":
    # Create an instance of UserGenerator and run it
    generator = UserGenerator()
    generator.run()