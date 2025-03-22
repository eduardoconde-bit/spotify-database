# Current Date and Time (UTC): 2025-03-22 19:22:34
# Current User's Login: eduardoconde-bit

from faker import Faker
import random

class PlaylistGenerator:
    """
    Class responsible for generating user playlists and playlist-song relationships.
    Creates data for both playlists table and playlist_songs table.
    """
    
    def __init__(self, num_users=100, num_songs=33454, 
                 playlist_file='insert_playlist.txt', 
                 playlist_songs_file='insert_playlist_songs.txt'):
        """
        Initialize the PlaylistGenerator with configuration parameters.
        
        Args:
            num_users (int): Total number of users in the database
            num_songs (int): Total number of songs available in the database
            playlist_file (str): File path to save playlist INSERT statements
            playlist_songs_file (str): File path to save playlist_songs INSERT statements
        """
        self.fake = Faker()
        self.num_users = num_users
        self.num_songs = num_songs
        self.playlist_file = playlist_file
        self.playlist_songs_file = playlist_songs_file
        self.playlist_count = 1  # Counter for playlist IDs
    
    def generate_playlist_name(self):
        """Generate a random playlist name based on colors or languages"""
        return random.choice([self.fake.color_name(), self.fake.language_name()])
    
    def create_playlist_insert(self, name, user_id, visibility):
        """Create SQL INSERT statement for a playlist"""
        return f"INSERT INTO playlists (name, user_id, visibility) VALUES ('{name}', {user_id}, '{visibility}');\n"
    
    def create_playlist_song_insert(self, playlist_id, song_id):
        """Create SQL INSERT statement for a playlist-song relationship"""
        return f"INSERT INTO playlist_songs (playlist_id, song_id) VALUES ({playlist_id}, {song_id});\n"
    
    def generate_playlist_songs(self, playlist_id):
        """
        Generate a set of songs to be included in a playlist.
        
        Args:
            playlist_id (int): The ID of the playlist
            
        Returns:
            set: A set of song IDs for this playlist
        """
        # Determine number of songs in this playlist
        num_playlist_songs = random.choice([5, 10, 15, 20])
        
        # Generate a set of unique song IDs
        songs = set()
        while len(songs) < num_playlist_songs:
            songs.add(random.randint(1, self.num_songs))
        
        return songs
    
    def generate_user_playlists(self, user_id):
        """
        Generate playlists for a specific user.
        
        Args:
            user_id (int): The ID of the user
            
        Returns:
            list: List of playlist IDs created for this user
        """
        # Determine number of playlists for this user (1 to 5)
        num_playlists = random.randint(1, 5)
        playlist_ids = []
        
        for _ in range(num_playlists):
            # Generate playlist data
            name = self.generate_playlist_name()
            visibility = random.choice(["public", "private"])
            
            # Record the current playlist ID
            current_playlist_id = self.playlist_count
            playlist_ids.append(current_playlist_id)
            
            # Create playlist INSERT statement
            with open(self.playlist_file, 'a') as file:
                insert_statement = self.create_playlist_insert(name, user_id, visibility)
                file.write(insert_statement)
            
            # Generate songs for this playlist
            songs = self.generate_playlist_songs(current_playlist_id)
            
            # Create playlist_songs INSERT statements
            with open(self.playlist_songs_file, 'a') as file:
                for song_id in songs:
                    insert_statement = self.create_playlist_song_insert(current_playlist_id, song_id)
                    file.write(insert_statement)
            
            # Increment playlist counter for next playlist
            self.playlist_count += 1
        
        return playlist_ids
    
    def initialize_files(self):
        """Initialize output files by creating them empty"""
        with open(self.playlist_file, 'w') as file:
            pass
        with open(self.playlist_songs_file, 'w') as file:
            pass
    
    def generate_all_playlists(self):
        """Generate playlists for all users"""
        # Initialize files
        self.initialize_files()
        
        # Generate playlists for each user
        for user_id in range(1, self.num_users + 1):
            playlist_ids = self.generate_user_playlists(user_id)
            
            # Print progress periodically
            if user_id % 10 == 0 or user_id == self.num_users:
                print(f"Generated playlists for {user_id}/{self.num_users} users...")
    
    def run(self):
        """Execute the playlist generation process"""
        print(f"Starting playlist generation for {self.num_users} users...")
        self.generate_all_playlists()
        print(f"Completed! Generated {self.playlist_count - 1} playlists.")
        print(f"Playlist data saved to '{self.playlist_file}'")
        print(f"Playlist-song relationships saved to '{self.playlist_songs_file}'")


if __name__ == "__main__":
    # Create an instance of PlaylistGenerator and run it
    generator = PlaylistGenerator()
    generator.run()