from faker import Faker
import random
import datetime

class MusicEntity:
    """Base class for music-related entities"""
    def __init__(self):
        self.fake = Faker()
    
    def create_insert_statement(self):
        """Method to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement this method")

class Song(MusicEntity):
    """Class representing a song entity"""
    def __init__(self, artist_id, genre_id, album_id):
        super().__init__()
        self.title = self._generate_title()
        self.duration = random.randint(60000, 600000)  # Duration in milliseconds
        self.artist_id = artist_id
        self.genre_id = genre_id
        self.album_id = album_id
        self.streams = random.randint(0, 1000000)
    
    def _generate_title(self):
        """Generate a creative song title"""
        return (
            random.choice([self.fake.word(), ' ']) +
            self.fake.color_name() +
            random.choice([self.fake.word(), ' '])
        ).strip()
    
    def create_insert_statement(self):
        """Create SQL INSERT statement for this song"""
        return (
            f"INSERT INTO songs (title, duration, artist_id, genre_id, album_id, streams) VALUES ("
            f"'{self.title}', {self.duration}, {self.artist_id}, {self.genre_id}, {self.album_id}, {self.streams});\n"
        )

class Album(MusicEntity):
    """Class representing an album entity"""
    def __init__(self, album_id, artist_id, genre_id):
        super().__init__()
        self.album_id = album_id
        self.title = self._generate_title()
        self.release_date = self.fake.date_of_birth(minimum_age=18, maximum_age=65)
        self.type = 'album'
        self.image = self.fake.url()
        self.genre_id = genre_id
        self.artist_id = artist_id
        self.songs = []
    
    def _generate_title(self):
        """Generate a creative album title"""
        return (
            random.choice([self.fake.word(), ' ']) +
            self.fake.color_name() +
            random.choice([self.fake.word(), ''])
        ).strip()
    
    def generate_songs(self, num_songs=None):
        """Generate songs for this album"""
        if num_songs is None:
            num_songs = random.choice([3, 4, 5, 8])
        
        for _ in range(num_songs):
            song = Song(self.artist_id, self.genre_id, self.album_id)
            self.songs.append(song)
        
        return self.songs
    
    def create_insert_statement(self):
        """Create SQL INSERT statement for this album"""
        return (
            f"INSERT INTO albums (title, release_date, type, image, genre_id, artist_id) VALUES ("
            f"'{self.title}', '{self.release_date}', '{self.type}', '{self.image}', {self.genre_id}, {self.artist_id});\n"
        )

class Artist(MusicEntity):
    """Class representing an artist entity"""
    def __init__(self, artist_id, country_list, genres):
        super().__init__()
        self.artist_id = artist_id
        self.name = self.fake.name()
        self.bio = self.fake.text(max_nb_chars=50)
        self.country = random.choice(country_list)
        self.date_of_birth = self.fake.date_of_birth(minimum_age=18, maximum_age=100)
        self.genre_id = random.choice(genres)
        self.albums = []
    
    def generate_albums(self, num_albums=None):
        """Generate albums for this artist"""
        if num_albums is None:
            num_albums = random.choice([1, 2, 3])
        
        album_ids = []
        for i in range(num_albums):
            album_id = MusicDataGenerator.get_next_album_id()
            album = Album(album_id, self.artist_id, self.genre_id)
            self.albums.append(album)
            album_ids.append(album_id)
        
        return self.albums
    
    def create_insert_statement(self):
        """Create SQL INSERT statement for this artist"""
        return (
            f"INSERT INTO artists (artist_id, name, bio, country, date_of_birth, genre_id) VALUES ("
            f"'{self.artist_id}', '{self.name}', '{self.bio}', '{self.country}', '{self.date_of_birth}', {self.genre_id});\n"
        )

class MusicDataGenerator:
    """Class that manages generation of music data and writing to files"""
    
    _album_id_counter = 0
    
    @classmethod
    def get_next_album_id(cls):
        """Get the next album ID in sequence"""
        cls._album_id_counter += 1
        return cls._album_id_counter
    
    def __init__(self, num_artists=1000):
        """
        Initialize the MusicDataGenerator with configuration parameters.
        
        Args:
            num_artists (int): Number of artists to generate
        """
        self.num_artists = num_artists
        self.artists = []
        self.country_list = ['BR', 'US', 'FR', 'DE', 'IT', 'AF', 'CA', 'GB', 'ES', 'JP', 'CN', 'IN', 'AU', 'RU', 'MX', 
                            'AR', 'ZA', 'PT', 'NL', 'SE', 'CH', 'KR', 'TR', 'NZ', 'AE', 'SA', 'EG', 'TH', 'SG', 'MY', 
                            'ID', 'PH', 'VN', 'CL', 'CO', 'PE', 'PL', 'GR', 'HU', 'AT', 'DK', 'NO', 'FI', 'BE', 'CZ', 
                            'IE', 'IL', 'HK', 'TW', 'PK', 'BD', 'IR', 'IQ', 'KW', 'QA', 'OM', 'NG', 'KE', 'GH', 'UG', 
                            'TZ', 'ET', 'MA', 'DZ', 'JO', 'LB', 'SY', 'YE', 'LY', 'TN', 'CM', 'CI', 'SN', 'MG', 'MU', 
                            'KM', 'SC', 'RW', 'BI', 'SS', 'ZW', 'ZM', 'AO', 'NA', 'BW', 'LS', 'SZ', 'MZ', 'CG', 'GA', 
                            'GQ', 'BJ', 'NE', 'ML', 'BF', 'LR', 'SL', 'GN', 'GW', 'CV', 'ST', 'TD', 'CF', 'SO', 'DJ', 
                            'ER', 'GM', 'LR', 'TG', 'BJ', 'MW', 'MZ', 'BW', 'NA', 'SZ', 'LS', 'ZW', 'ZM', 'AO', 'MZ', 
                            'BW', 'NA', 'SZ', 'LS', 'ZW', 'ZM']
        self.genres = [num for num in range(1, 177)]
        
        # File paths for insert statements
        self.artists_file = 'insert_artists.txt'
        self.albums_file = 'insert_albums.txt'
        self.songs_file = 'insert_songs.txt'
    
    def generate_artists(self):
        """Generate artists data"""
        self.artists = []
        for artist_id in range(1, self.num_artists + 1):
            artist = Artist(artist_id, self.country_list, self.genres)
            self.artists.append(artist)
            print(f"Generated artist {artist_id}/{self.num_artists}")
        return self.artists
    
    def save_all_data(self):
        """Save all generated data to files"""
        # Initialize files
        with open(self.artists_file, 'w') as f:
            pass
        with open(self.albums_file, 'w') as f:
            pass
        with open(self.songs_file, 'w') as f:
            pass
        
        # Generate and save data for each artist
        for artist in self.artists:
            # Save artist data
            with open(self.artists_file, 'a') as f:
                f.write(artist.create_insert_statement())
            
            # Generate albums for this artist
            albums = artist.generate_albums()
            
            # Save album data and generate songs
            for album in albums:
                with open(self.albums_file, 'a') as f:
                    f.write(album.create_insert_statement())
                
                # Generate songs for this album
                songs = album.generate_songs()
                
                # Save song data
                with open(self.songs_file, 'a') as f:
                    for song in songs:
                        f.write(song.create_insert_statement())
    
    def run(self):
        """Execute the entire data generation process"""
        print(f"Starting generation of {self.num_artists} artists...")
        self.generate_artists()
        self.save_all_data()
        print(f"{'-'*50}")
        print(f"{self.num_artists} artists were generated and saved to '{self.artists_file}'.")
        print(f"Albums were saved to '{self.albums_file}'.")
        print(f"Songs were saved to '{self.songs_file}'.")
        print(f"{'-'*50}")


if __name__ == "__main__":
    # Create an instance of MusicDataGenerator and run it
    generator = MusicDataGenerator(num_artists=1000)
    generator.run()