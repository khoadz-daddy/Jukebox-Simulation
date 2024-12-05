import tkinter as tk  # Import the tkinter library for GUI creation
import tracks_library as lib  # Import the library for track data management
import font_manager as fonts  # Import custom font manager for consistent font styles
from PIL import Image, ImageTk  # Import Pillow for image handling
import requests  # Import requests for fetching images from URLs
from io import BytesIO  # Import BytesIO for handling image data in memory
import json  # Import json for working with JSON data

class Viewtracks:
    def __init__(self, window, shared_play_counts):
        """Initialize the Viewtracks class."""
        self.window = window  # Reference to the main window
        self.shared_play_counts = shared_play_counts  # Shared play counts dictionary
        window.title("View Tracks")  # Set the window title

        # Dropdown for selecting an artist
        self.artist_var = tk.StringVar(window)  # Variable to hold the selected artist
        self.artist_var.set("All Artists")  # Default value for the dropdown

        # Create the dropdown menu for artist selection
        self.artist_menu = tk.OptionMenu(window, self.artist_var, *lib.get_all_artists(), command=self.filter_tracks)
        self.artist_menu.grid(row=0, column=0, padx=10, pady=10)  # Position the dropdown in the grid

        # Button to list all tracks
        list_tracks_btn = tk.Button(window, text="List All Tracks", command=self.list_tracks_clicked)
        list_tracks_btn.grid(row=0, column=1, padx=10, pady=10)  # Position the button in the grid

        # Label and Entry for inputting track number
        enter_lbl = tk.Label(window, text="Enter Track Number")
        enter_lbl.grid(row=0, column=2, padx=10, pady=10)  # Position the label

        self.input_txt = tk.Entry(window, width=3)  # Entry field for track number input
        self.input_txt.grid(row=0, column=3, padx=10, pady=10)  # Position the entry field

        # Button to check specific track details
        check_track_btn = tk.Button(window, text="View Track", command=self.check_track_clicked)
        check_track_btn.grid(row=0, column=4, padx=10, pady=10)  # Position the button in the grid

        # Listbox for displaying the list of tracks
        self.listbox = tk.Listbox(window, width=50, height=15)  # Create a listbox for tracks
        self.listbox.grid(row=1, column=0, columnspan=4, padx=10, pady=10)  # Position the listbox

        # Text area for displaying individual track details
        self.tracks_txt = tk.Text(window, width=24, height=4, wrap="none")  # Create a text area for track details
        self.tracks_txt.grid(row=1, column=4, sticky="NW", padx=10, pady=10)  # Position the text area

        # Image label for displaying the song cover
        self.image_label = tk.Label(window)  # Create a label for the image
        self.image_label.grid(row=1, column=5, sticky="NW", padx=10, pady=10)  # Position the image label

        # Status label for displaying messages
        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))  # Create a status label
        self.status_lbl.grid(row=2, column=0, columnspan=6, sticky="W", padx=10, pady=10)  # Position the status label

        # Bind the Listbox selection event to a handler method
        self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

        # Resize the window to fit its content
        self.resize_window()

    def resize_window(self):
        """Resize the window to fit the content."""
        self.window.update_idletasks()  # Update the window to reflect changes
        self.window.geometry('')  # Reset geometry to fit the content

    def filter_tracks(self, artist):
        """Filters tracks based on the selected artist."""
        self.listbox.delete(0, tk.END)  # Clear existing items in the listbox
        if artist == "All Artists":
            self.list_tracks_clicked()  # Show all tracks if "All Artists" is selected
        else:
            tracks_list = lib.list_by_artist(artist)  # Fetch tracks by the selected artist
            if tracks_list.strip():  # Check if the list is not empty
                for line in tracks_list.split("\n"):  # Split the list into lines
                    self.listbox.insert(tk.END, line)  # Add each line to the listbox
            else:
                self.listbox.insert(tk.END, "No tracks found for this artist!")  # Inform the user if no tracks found
                self.status_lbl.configure(text="No tracks available for the selected artist.")  # Update status

    def list_tracks_clicked(self):
        """Displays all tracks in the Listbox widget."""
        self.listbox.delete(0, tk.END)  # Clear existing items in the listbox
        tracks_list = lib.list_all()  # Fetch all tracks from the library
        if tracks_list.strip():  # If the list is not empty
            for line in tracks_list.split("\n"):  # Split the list into lines
                self.listbox.insert(tk.END, line)  # Add each line to the listbox
        else:
            self.listbox.insert(tk.END, "No tracks found!")  # Inform the user if no tracks found
            self.status_lbl.configure(text="No tracks available to display.")  # Update status

    def check_track_clicked(self):
        """Displays track details when a track is checked."""
        key = self.input_txt.get().strip()  # Get the input track number
        self.display_track_details(key)  # Display details for the specified track

    def on_listbox_select(self, event):
        """Handles the selection of a track from the Listbox."""
        try:
            selected_item = self.listbox.get(self.listbox.curselection())  # Get the selected item
            key = selected_item.split(":")[0]  # Extract the track key from the selection
            self.display_track_details(key)  # Display details for the selected track
        except IndexError:
            self.status_lbl.configure(text="No track selected!")  # Inform the user if no track is selected

    def display_track_details(self, key):
        """Displays details of the selected track and updates the play count."""
        if key in lib.library:  # Check if the track key exists in the library
            track = lib.library[key]  # Retrieve the track object from the library

            # Increase play count and update JSON
            self.update_play_count(track)  # Increment play count for the track

            # Prepare track details to display
            track_details = (
                f"Song: {track.title}\n"  # Display the song title
                f"Singer: {track.singer}\n"  # Display the singer's name
                f"Rating: {track.rating}\n"  # Display the track's rating
                f"Plays: {track.play_count}\n"  # Display the play count
                f"Link: {track.link}"  # Display the link to the track
            )
            self.tracks_txt.delete("1.0", tk.END)  # Clear previous details in the text area
            self.tracks_txt.insert("1.0", track_details)  # Insert the new track details

            # Check for image path and display if available
            if track.image_path:
                self.display_image(track.image_path)  # Display track cover image
            else:
                self.image_label.config(image='')  # Clear image if no URL provided
        else:
            self.tracks_txt.delete("1.0", tk.END)  # Clear text area if track not found
            self.tracks_txt.insert("1.0", "Track not found!")  # Inform user track not found
            self.image_label.config(image='')  # Clear image if track not found
            self.status_lbl.configure(text="")  # Clear any previous error message

    def update_play_count(self, track):
        """Increases the play count and updates the JSON file."""
        track.play_count += 1  # Increment the play count for the track
        self.save_play_count_to_json(track)  # Save the updated play count to the JSON file

    def save_play_count_to_json(self, track):
        """Saves the updated play count back to the JSON file."""
        try:
            with open('/Users/mk183/Documents/GREENWICH MATERIALS/Lê Anh Khoa/song.json', 'r+', encoding='utf-8') as file:
                songs = json.load(file)  # Load existing songs from JSON file
                # Update the play count in the list
                for song in songs:
                    if song["title"] == track.title and song["singer"] == track.singer:
                        song["play_count"] = track.play_count  # Update the play count for the matching song
                        break
                # Move to the beginning of the file and overwrite it
                file.seek(0)  
                json.dump(songs, file, indent=4)  # Write the updated songs list back to the file
                file.truncate()  # Remove any leftover data in the file
            self.status_lbl.configure(text="Play count updated successfully.")  # Inform user of success
        except Exception as e:
            print(f"Error saving play count: {e}")  # Print error message
            self.status_lbl.configure(text="Error updating play count.")  # Inform user of the error

    def display_image(self, image_url):
        """Fetch and display an image from a URL."""
        try:
            response = requests.get(image_url)  # Fetch the image from the URL
            response.raise_for_status()  # Raise an exception for bad responses
            image_data = Image.open(BytesIO(response.content))  # Open the image from the fetched data
            photo = ImageTk.PhotoImage(image_data)  # Convert the image for Tkinter

            # Update the image label with the new image
            self.image_label.config(image=photo)
            self.image_label.image = photo  # Keep a reference to prevent garbage collection
            
            # Clear any previous error message
            self.status_lbl.configure(text="")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching image: {e}")  # Print error message
            self.status_lbl.configure(text="Error fetching image.")  # Inform user of the error
            self.image_label.config(image='')  # Clear image on error

if __name__ == "__main__":
    shared_play_counts = {}  # Shared dictionary for play counts (if needed)
    window = tk.Tk()  # Create the main window
    fonts.configure()  # Configure fonts using the custom font manager
    app = Viewtracks(window, shared_play_counts)  # Instantiate the Viewtracks class
    window.mainloop()  # Start the Tkinter event loop