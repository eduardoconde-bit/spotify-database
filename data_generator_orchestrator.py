#!/usr/bin/env python3
# Current Date and Time (UTC): 2025-03-22 20:39:19
# Current User's Login: eduardoconde-bit

import os
import random
from faker import Faker

# Import all the generator classes
from user_generator import UserGenerator
from music_data_generator import MusicDataGenerator
from follower_generator import FollowersGenerator
from playlist_generator import PlaylistGenerator
from liked_songs_generator import LikedSongsGenerator

class GenreGenerator:
    """Class responsible for generating genre data"""
    
    def __init__(self, num_genres=177, output_file='insert_genres.txt'):
        """
        Initialize the GenreGenerator with configuration parameters.
        
        Args:
            num_genres (int): Number of genres to generate
            output_file (str): File path to save the SQL insert statements
        """
        self.fake = Faker()
        self.num_genres = num_genres
        self.output_file = output_file
        
        # Music genre names to use
        self.genre_names = [
            'Rock', 'Pop', 'Hip Hop', 'Rap', 'Electronic', 'Classical', 'Jazz', 'Blues', 'R&B', 
            'Soul', 'Country', 'Folk', 'Reggae', 'Punk', 'Metal', 'Alternative', 'Indie', 
            'Funk', 'Disco', 'Techno', 'House', 'Ambient', 'Trance', 'Dubstep', 'Trap', 
            'Instrumental', 'Orchestra', 'Soundtrack', 'World', 'Latin', 'K-Pop', 'J-Pop', 
            'Gospel', 'Christian', 'New Age', 'Experimental', 'Grunge', 'Post-Rock', 
            'Psychedelic', 'Garage', 'Hardcore', 'Death Metal', 'Black Metal', 'Thrash Metal', 
            'Heavy Metal', 'Glam Metal', 'Progressive Metal', 'Doom Metal', 'Gothic Metal', 
            'Symphonic Metal', 'Folk Metal', 'Power Metal', 'Industrial Metal', 'Nu Metal', 
            'Metalcore', 'Deathcore', 'Grindcore', 'Punk Rock', 'Pop Punk', 'Ska Punk', 
            'Hardcore Punk', 'Post-Punk', 'Emo', 'Screamo', 'Post-Hardcore', 'Hard Rock', 
            'Soft Rock', 'Progressive Rock', 'Psychedelic Rock', 'Surf Rock', 'Garage Rock', 
            'Art Rock', 'Math Rock', 'Noise Rock', 'Space Rock', 'Pop Rock', 'Folk Rock', 
            'Country Rock', 'Blues Rock', 'Funk Rock', 'Rap Rock', 'Electronic Rock'
        ]
        
        # If we need more genres than names, we'll add numbered varieties
        while len(self.genre_names) < self.num_genres:
            base_name = random.choice(self.genre_names[:50])
            self.genre_names.append(f"{base_name} Fusion")
            self.genre_names.append(f"Modern {base_name}")
            self.genre_names.append(f"Alternative {base_name}")
            self.genre_names.append(f"Classic {base_name}")
            self.genre_names.append(f"{base_name} Revival")
    
    def create_insert_statement(self, genre_id, name, description):
        """Create SQL INSERT statement for a genre"""
        return f"INSERT INTO genres (genre_id, name, description) VALUES ({genre_id}, '{name}', '{description}');\n"
    
    def generate_genres(self):
        """Generate genre data and write to file"""
        with open(self.output_file, 'w') as file:
            for genre_id in range(1, self.num_genres + 1):
                if genre_id <= len(self.genre_names):
                    name = self.genre_names[genre_id - 1]
                else:
                    name = f"Genre {genre_id}"
                
                description = self.fake.sentence(nb_words=10)
                
                insert_statement = self.create_insert_statement(genre_id, name, description)
                file.write(insert_statement)
    
    def run(self):
        """Execute the genre generation process"""
        print(f"Generating {self.num_genres} music genres...")
        self.generate_genres()
        print(f"Genres saved to '{self.output_file}'")


class MusicDataTrackerMixin:
    """Mixin class to track and count the songs generated"""
    
    @classmethod
    def count_songs_in_file(cls, filename):
        """Count the number of INSERT statements in a songs file"""
        if not os.path.exists(filename):
            return 0
            
        try:
            with open(filename, 'r') as file:
                return sum(1 for line in file if line.strip().startswith("INSERT INTO songs"))
        except Exception as e:
            print(f"Error counting songs: {e}")
            return 0


class DataGeneratorOrchestrator(MusicDataTrackerMixin):
    """
    Main class that orchestrates the sequential execution of all data generators.
    Ensures that data is generated in the correct order to maintain referential integrity.
    """
    
    def __init__(self, config=None):
        """
        Initialize the orchestrator with configuration parameters.
        
        Args:
            config (dict, optional): Configuration dictionary with customizable parameters
        """
        # Default configuration
        self.config = {
            'num_genres': 177,
            'num_users': 100,
            'num_artists': 1000,
            'output_dir': 'generated_data',
            'create_output_dir': True
        }
        
        # Override defaults with provided config
        if config:
            self.config.update(config)
        
        # Ensure output directory exists
        if self.config['create_output_dir'] and not os.path.exists(self.config['output_dir']):
            os.makedirs(self.config['output_dir'])
    
    def get_output_path(self, filename):
        """Get full path for an output file"""
        return os.path.join(self.config['output_dir'], filename)
    
    def generate_all_data(self):
        """Execute all data generators in the correct sequence"""
        # Track timing and progress
        print(f"\n{'='*80}")
        print(f"Starting data generation with configuration:")
        print(f"  - Genres: {self.config['num_genres']}")
        print(f"  - Users: {self.config['num_users']}")
        print(f"  - Artists: {self.config['num_artists']}")
        print(f"  - Output directory: {self.config['output_dir']}")
        print(f"{'='*80}\n")
        
        # Step 1: Generate Genres
        print(f"\n{'-'*40}")
        print("STEP 1: Generating Genres")
        print(f"{'-'*40}")
        genre_generator = GenreGenerator(
            num_genres=self.config['num_genres'],
            output_file=self.get_output_path('insert_genres.txt')
        )
        genre_generator.run()
        
        # Step 2: Generate Users
        print(f"\n{'-'*40}")
        print("STEP 2: Generating Users")
        print(f"{'-'*40}")
        user_generator = UserGenerator(
            num_users=self.config['num_users'],
            output_file=self.get_output_path('insert_users.txt')
        )
        user_generator.run()
        
        # Step 3: Generate Artists, Albums and Songs
        print(f"\n{'-'*40}")
        print("STEP 3: Generating Artists, Albums and Songs")
        print(f"{'-'*40}")
        
        music_generator = MusicDataGenerator(num_artists=self.config['num_artists'])
        # Adjust file paths to use our output directory
        music_generator.artists_file = self.get_output_path('insert_artists.txt')
        music_generator.albums_file = self.get_output_path('insert_albums.txt')
        music_generator.songs_file = self.get_output_path('insert_songs.txt')
        music_generator.run()
        
        # Get the actual number of songs by counting the INSERT statements in the songs file
        actual_songs = self.count_songs_in_file(music_generator.songs_file)
        print(f"Actual number of songs generated: {actual_songs}")
        
        # Step 4: Generate Artist Followers
        print(f"\n{'-'*40}")
        print("STEP 4: Generating Artist Followers")
        print(f"{'-'*40}")
        followers_generator = FollowersGenerator(
            num_users=self.config['num_users'],
            num_artists=self.config['num_artists'],
            output_file=self.get_output_path('insert_followers_artists.txt')
        )
        followers_generator.run()
        
        # Step 5: Generate Playlists and Playlist Songs
        print(f"\n{'-'*40}")
        print("STEP 5: Generating Playlists and Playlist Songs")
        print(f"{'-'*40}")
        
        # Modified PlaylistGenerator class that respects song ID limits
        class SafePlaylistGenerator(PlaylistGenerator):
            def generate_playlist_songs(self, playlist_id):
                """Modified to ensure song IDs are within valid range"""
                num_playlist_songs = min(random.choice([5, 10, 15, 20]), self.num_songs)
                
                songs = set()
                while len(songs) < num_playlist_songs and len(songs) < self.num_songs:
                    # Ensure we only use song IDs that exist
                    songs.add(random.randint(1, self.num_songs))
                
                return songs
        
        playlist_generator = SafePlaylistGenerator(
            num_users=self.config['num_users'],
            num_songs=actual_songs,  # Use actual count of songs
            playlist_file=self.get_output_path('insert_playlist.txt'),
            playlist_songs_file=self.get_output_path('insert_playlist_songs.txt')
        )
        playlist_generator.run()
        
        # Step 6: Generate Liked Songs
        print(f"\n{'-'*40}")
        print("STEP 6: Generating Liked Songs")
        print(f"{'-'*40}")
        
        # Modified LikedSongsGenerator class that respects song ID limits
        class SafeLikedSongsGenerator(LikedSongsGenerator):
            def generate_user_likes(self, user_id):
                """Modified to ensure song IDs are within valid range"""
                num_songs_to_like = min(random.randint(1, 7), self.num_songs)
                
                liked_songs = set()
                while len(liked_songs) < num_songs_to_like and len(liked_songs) < self.num_songs:
                    # Ensure we only use song IDs that exist
                    liked_songs.add(random.randint(1, self.num_songs))
                    
                return liked_songs
        
        liked_songs_generator = SafeLikedSongsGenerator(
            num_users=self.config['num_users'],
            num_songs=actual_songs,  # Use actual count of songs
            output_file=self.get_output_path('insert_liked_songs.txt')
        )
        liked_songs_generator.run()
        
        # Final summary
        print(f"\n{'='*80}")
        print("DATA GENERATION COMPLETE!")
        print(f"{'='*80}")
        print("Generated files:")
        for file in os.listdir(self.config['output_dir']):
            if file.startswith('insert_'):
                file_path = os.path.join(self.config['output_dir'], file)
                file_size = os.path.getsize(file_path) / 1024  # size in KB
                print(f"  - {file:<30} {file_size:.2f} KB")
        print(f"{'='*80}\n")


if __name__ == "__main__":
    # Example custom configuration
    custom_config = {
        'num_genres': 177,     # Number of music genres
        'num_users': 100,      # Number of users
        'num_artists': 500,   # Number of artists
        'output_dir': 'spotify_db_data',  # Output directory for all generated files
        'create_output_dir': True  # Create the output directory if it doesn't exist
    }
    
    # Create and run the orchestrator
    orchestrator = DataGeneratorOrchestrator(config=custom_config)
    orchestrator.generate_all_data()