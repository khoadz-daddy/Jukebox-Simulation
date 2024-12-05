import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tkst
import font_manager as fonts  # Custom font manager
import tracks_library as lib  # Custom library for managing tracks
from view_tracks import Viewtracks  # Class to check tracks
from update_tracks import UpdateTracksWindow
from tkinter import messagebox, filedialog
from create_track_list import TrackListApp
import csv
import json

# Initialize a shared dictionary for play counts
shared_play_counts = {}

def play_track(track_key):
    """Simulate playing a track and increment its play count."""
    if track_key in shared_play_counts:
        shared_play_counts[track_key] += 1  # Increment play count
    else:
        shared_play_counts[track_key] = 1  # Initialize if not already present
    print(f"Track {track_key} has been played. New count: {shared_play_counts[track_key]}")

class LibraryItem:
    def __init__(self, song, singer, rating, play_count=0):
        """Initialize a LibraryItem with song title, singer, rating, and play count."""
        self.song = song
        self.singer = singer
        self.rating = rating
        self.play_count = play_count  # Initialize play count

    def info(self):
        """Return a formatted string with track information."""
        return (self.song, self.singer, self.rating, self.play_count)  # Return as tuple

    @staticmethod
    def read_library(file_path):
        """Read songs from a JSON file and return a list of LibraryItem instances."""
        items = []
        with open(file_path, 'r') as jsonfile:
            tracks_data = json.load(jsonfile)
            for track in tracks_data:
                if 'song' in track and 'singer' in track and 'rating' in track and 'play_count' in track:
                    items.append(LibraryItem(track['song'], track['singer'], track['rating'], track['play_count']))
        return items

class TrackPlayer:
    def __init__(self, root):
        """Initialize the ViewTracks GUI component."""
        self.root = root  # Main application window
        self.library_items = []  # List to hold LibraryItem instances
        self.create_widgets()  # Create the GUI components

    def create_widgets(self):
        """Create and layout GUI components for viewing tracks."""
        self.tree = ttk.Treeview(self.root, columns=("Song", "Artist", "Rating", "Play Count"), show='headings', height=15)
        self.tree.heading("Song", text="Song")
        self.tree.heading("Artist", text="Artist")
        self.tree.heading("Rating", text="Rating")
        self.tree.heading("Play Count", text="Play Count")
        self.tree.column("Song", anchor="w", width=200)
        self.tree.column("Artist", anchor="w", width=150)
        self.tree.column("Rating", anchor="center", width=100)
        self.tree.column("Play Count", anchor="center", width=100)
        self.tree.grid(row=4, column=0, columnspan=4, pady=10)
    def create_track_list(self):
        """Create a new TrackListApp instance."""
        TrackListApp(tk.Toplevel(self.root), shared_play_counts)

    def update_tracks(self):
        """Open the UpdateTracksWindow."""
        UpdateTracksWindow(self.root)
    def view_tracks(self):
        """Open the Viewtracks application."""
        Viewtracks(tk.Toplevel(self.root), shared_play_counts)
    def load_library(self):
        """Load tracks from the library JSON file."""
        file_path = "song.json"  # Define the path to the JSON file
        self.library_items = LibraryItem.read_library(file_path)  # Read items from the file
        self.update_library()  # Update the GUI to reflect loaded items

    def update_library(self):
        """Update the Treeview to show current library items."""
        for item in self.tree.get_children():
            self.tree.delete(item)  # Clear the Treeview
        for item in self.library_items:
            self.tree.insert("", tk.END, values=item.info())  # Insert each item's info into the Treeview

def import_track_list(tree, status_lbl):
    """Import a track list from a CSV file and update the Treeview."""
    status_lbl.configure(text="Import Track List button was clicked!")
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])  # Open file dialog
    if file_path:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)  # Read the selected CSV file
            for track in reader:
                if len(track) >= 4:  # Ensure there are enough columns
                    tree.insert("", tk.END, values=track)  # Insert each track into the Treeview
        status_lbl.configure(text="Track list imported successfully.")  # Update status after import

def export_track_list(tree, status_lbl):
    """Export tracks with play_count > 0 to a CSV file without headers."""
    status_lbl.configure(text="Export Track List button was clicked!")
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])  # Save dialog
    if file_path:
        with open(file_path, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)  # Create a CSV writer
            # Write tracks with play_count > 0
            for item in tree.get_children():
                track = tree.item(item)['values']
                if int(track[3]) > 0:  # Check play count
                    writer.writerow([track[0], track[1], track[2], track[3]])  # Write track data
        status_lbl.configure(text="Track list exported successfully.")
    else:
        status_lbl.configure(text="Export cancelled.")

# Main Window setup
window = tk.Tk()  # Create the main application window
window.geometry("800x600")  # Set the size of the window larger for better readability
window.title("JukeBox")  # Set the title of the window

fonts.configure()  # Configure fonts using a custom font manager

# Create a header label
header_lbl = tk.Label(window, text="Select an option by clicking one of the buttons below", font=("Helvetica", 14))
header_lbl.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

track_player = TrackPlayer(window)  # Create an instance of TrackPlayer for managing track views

# Create buttons for various functionalities
check_view_btn = tk.Button(window, text="View Tracks", command=lambda: Viewtracks(tk.Toplevel(window), shared_play_counts), font=("Helvetica", 12))
check_view_btn.grid(row=1, column=0, padx=10, pady=10)

create_track_list_btn = tk.Button(window, text="Create Track List", 
                                    command=lambda: TrackListApp(tk.Toplevel(window), shared_play_counts), 
                                    font=("Helvetica", 12))
create_track_list_btn.grid(row=1, column=1, padx=10, pady=10)

update_tracks_btn = tk.Button(window, text="Update Tracks", command=track_player.update_tracks, font=("Helvetica", 12))
update_tracks_btn.grid(row=1, column=2, padx=10, pady=10)

btn_import_track_list = tk.Button(window, text="Import Track List", command=lambda: import_track_list(track_player.tree, status_lbl), font=("Helvetica", 12))
btn_import_track_list.grid(row=2, column=0, padx=10, pady=10)

btn_export_track_list = tk.Button(window, text="Export Track List", command=lambda: export_track_list(track_player.tree, status_lbl), font=("Helvetica", 12))
btn_export_track_list.grid(row=2, column=1, padx=10, pady=10)

status_lbl = tk.Label(window, text="", font=("Helvetica", 12))  # Label for status messages
status_lbl.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

window.mainloop()  # Start the main event loop