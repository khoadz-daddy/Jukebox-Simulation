import json

class LibraryItem:
    def __init__(self, title, singer, rating, link, image_path=None, play_count=0):
        if not isinstance(rating, int) or not (0 <= rating <= 5):
            raise ValueError("Rating must be an integer between 0 and 5.")
        if not isinstance(play_count, int) or play_count < 0:
            raise ValueError("Play count must be a non-negative integer.")
        
        self.title = title
        self.singer = singer
        self.rating = rating
        self.link = link
        self.image_path = image_path
        self.play_count = play_count

    def info(self):
        """Return a tuple with track information."""
        return (self.title, self.singer, self.rating, self.play_count)

# Initialize the library dictionary
library = {}

def load_library_from_json(json_file):
    """Load library data from a JSON file."""
    global library
    library = {}  # Clear existing library
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            songs = json.load(file)
            for index, song in enumerate(songs, start=1):
                key = str(index).zfill(2)  # Create a zero-padded key
                library[key] = LibraryItem(
                    title=song["title"],
                    singer=song["singer"],
                    rating=song["rating"],
                    link=song["link"],
                    image_path=song.get("image_url"),
                    play_count=song.get("play_count")  # Load play count directly from JSON
                )
    except FileNotFoundError:
        print(f"Error: The file {json_file} was not found.")
    except json.JSONDecodeError as e:
        print(f"Error: JSON Decode Error - {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def list_all():
    """Returns a formatted string of all tracks in the library."""
    return "\n".join(f"{key}: {item.title}" for key, item in library.items())

def get_all_artists():
    """Returns a list of unique artist names from the library."""
    return list(set(item.singer for item in library.values()))

def list_by_artist(artist):
    """Returns a formatted string of tracks by a specific artist."""
    track_list = [
        f"{key}: {track.title} by {track.singer}"
        for key, track in library.items() if artist in track.singer
    ]
    return "\n".join(track_list) if track_list else f"No songs found for {artist}."

def reload_library():
    load_library_from_json('/Users/mk183/Documents/GREENWICH/JukeBox/song.json')  # Adjust path as needed

def list_all():
    """Returns a formatted string of all tracks in the library."""
    track_list = [f"{key}: {track.title}" for key, track in library.items()]
    return "\n".join(track_list)

def get_song(key):
    """Returns the song name for the given track key."""
    return library.get(key).title if key in library else None

def get_singer(key):
    """Returns the singer for the given track key."""
    return library.get(key).singer if key in library else None

def get_rating(key):
    """Returns the rating for the given track key."""
    return library.get(key).rating if key in library else None

def set_rating(key, new_rating):
    """Updates the rating for the song based on the key."""
    if key in library:
        library[key].rating = new_rating
    else:
        print(f"Track {key} not found.")

def get_play_count(key):
    """Returns the play count for the given track key."""
    return library.get(key).play_count if key in library else None

def update_play_count(key, new_play_count):
    """Updates the play count for the song based on the key."""
    if key in library:
        library[key].play_count = new_play_count
    else:
        print(f"Track {key} not found.")

def display_track_details(key):
    """Displays the details of a track including the image path."""
    if key in library:
        track = library[key]
        details = (
            f"Title: {track.title}\n"
            f"Singer: {track.singer}\n"
            f"Rating: {track.rating}\n"
            f"Link: {track.link}\n"
            f"Image Path: {track.image_path}\n"
            f"Play Count: {track.play_count}\n"
        )
        print(details)
    else:
        print(f"Track {key} not found.")

# Load data from song.json
load_library_from_json(r'/Users/mk183/Documents/GREENWICH/JukeBox/song.json')
print("Library loaded:", library)

# Example usage:
print(list_all())  # List all songs
display_track_details("01")  # Display details of the first track
