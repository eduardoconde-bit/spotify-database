# Current Date and Time (UTC): 2025-03-22 19:15:31
# Current User's Login: eduardoconde-bit

from faker import Faker
import random

class FollowersGenerator:
    """
    Class responsible for generating relationships between users and artists.
    Generates data for the artists_followers table, representing which users follow which artists.
    """
    
    def __init__(self, num_users=100, num_artists=1000, output_file='insert_followers_artists.txt'):
        """
        Initialize the FollowersGenerator with configuration parameters.
        
        Args:
            num_users (int): Number of users for which to generate relationships
            num_artists (int): Total number of artists available in the database
            output_file (str): File path to save the SQL insert statements
        """
        self.fake = Faker()
        self.num_users = num_users
        self.num_artists = num_artists
        self.output_file = output_file
        
    def generate_user_follows(self, user_id):
        """
        Generate the list of artists that a specific user follows.
        
        Args:
            user_id (int): The ID of the user
            
        Returns:
            set: A set of artist IDs that the user follows
        """
        # Determine how many artists this user will follow (1 to 5)
        num_artists_to_follow = random.randint(1, 5)
        
        # Generate a set of unique artist IDs to follow
        artist_list = set()
        while len(artist_list) < num_artists_to_follow:
            artist_list.add(random.randint(1, self.num_artists))
            
        print(f"User {user_id} follows artists: {artist_list}")
        return artist_list
    
    def create_insert_statement(self, user_id, artist_id):
        """
        Create an SQL INSERT statement for a user-artist follow relationship.
        
        Args:
            user_id (int): The ID of the user
            artist_id (int): The ID of the artist being followed
            
        Returns:
            str: SQL INSERT statement
        """
        return (
            f"INSERT INTO artists_followers (user_id, artist_id) VALUES ("
            f"{user_id}, {artist_id});\n"
        )
    
    def generate_all_follows(self):
        """
        Generate follow relationships for all users and write INSERT statements to a file.
        """
        # Open file for writing (or create it if it doesn't exist)
        with open(self.output_file, 'w') as file:
            # For each user
            for user_id in range(1, self.num_users + 1):
                # Get the set of artists this user follows
                followed_artists = self.generate_user_follows(user_id)
                
                # Create and write insert statements for each relationship
                for artist_id in followed_artists:
                    insert_statement = self.create_insert_statement(user_id, artist_id)
                    file.write(insert_statement)
    
    def run(self):
        """Execute the followers generation process."""
        print(f"Generating artist follow relationships for {self.num_users} users...")
        self.generate_all_follows()
        print(f"Completed! Follow relationships saved to '{self.output_file}'.")


if __name__ == "__main__":
    # Create an instance of FollowersGenerator and run it
    generator = FollowersGenerator()
    generator.run()