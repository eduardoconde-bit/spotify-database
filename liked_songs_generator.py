# Current Date and Time (UTC): 2025-03-22 19:20:27
# Current User's Login: eduardoconde-bit

import random
from faker import Faker

class LikedSongsGenerator:
    """
    Class responsible for generating relationships between users and the songs they like.
    Generates data for the liked_songs table, representing which users like which songs.
    """
    
    def __init__(self, num_users=100, num_songs=5135, output_file='insert_liked_songs.txt'):
        """
        Initialize the LikedSongsGenerator with configuration parameters.
        
        Args:
            num_users (int): Total number of users in the database
            num_songs (int): Total number of songs available in the database
            output_file (str): File path to save the SQL insert statements
        """
        self.fake = Faker()
        self.num_users = num_users
        self.num_songs = num_songs
        self.output_file = output_file
        
    def generate_user_likes(self, user_id):
        """
        Generate the set of songs that a specific user likes.
        
        Args:
            user_id (int): The ID of the user
            
        Returns:
            set: A set of song IDs that the user likes
        """
        # Determine how many songs this user will like (1 to 7)
        num_songs_to_like = random.randint(1, 7)
        
        # Generate a set of unique song IDs to like
        liked_songs = set()
        while len(liked_songs) < num_songs_to_like:
            liked_songs.add(random.randint(1, self.num_songs))
            
        return liked_songs
    
    def create_insert_statement(self, user_id, song_id):
        """
        Create an SQL INSERT statement for a user-song like relationship.
        
        Args:
            user_id (int): The ID of the user
            song_id (int): The ID of the song being liked
            
        Returns:
            str: SQL INSERT statement
        """
        return f"INSERT INTO liked_songs (user_id, song_id) VALUES ('{user_id}', '{song_id}');\n"
    
    def generate_all_likes(self):
        """
        Generate like relationships for all users and write INSERT statements to a file.
        """
        # Open file for writing
        with open(self.output_file, 'w') as file:
            # Process each user
            for user_id in range(1, self.num_users + 1):
                # Get the set of songs this user likes
                liked_songs = self.generate_user_likes(user_id)
                
                # Create and write insert statements for each relationship
                for song_id in liked_songs:
                    insert_statement = self.create_insert_statement(user_id, song_id)
                    file.write(insert_statement)
                
                # Print progress every 10 users
                if user_id % 10 == 0:
                    print(f"Generated likes for {user_id}/{self.num_users} users...")
    
    def run(self):
        """Execute the liked songs generation process."""
        print(f"Generating liked songs relationships for {self.num_users} users...")
        self.generate_all_likes()
        print(f"Completed! Liked songs relationships saved to '{self.output_file}'.")


if __name__ == "__main__":
    # Create an instance of LikedSongsGenerator and run it
    generator = LikedSongsGenerator(num_users=100, num_songs=33454)
    generator.run()