import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
import os

class TrackListApp:
    def __init__(self, master, shared_play_counts=None):
        self.master = master
        self.master.title("Create Track List")
        
        self.shared_play_counts = shared_play_counts  # Optional shared parameter
        self.load_tracks()  # Load track data from JSON file
        self.create_widgets()  # Create GUI widgets
        self.playlist = []  # Initialize an empty playlist

    def load_tracks(self):
        """Load track data from JSON file."""
        try:
            file_path = '/Users/mk183/Documents/GREENWICH/JukeBox/song.json'  # Specify the file path
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"{file_path} does not exist.")
            with open(file_path, 'r') as file:
                self.tracks = json.load(file)  # Load tracks into a list
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tracks: {e}")
            self.tracks = []  # Initialize an empty list if loading fails

    def create_widgets(self):
        """Create GUI widgets."""
        instruction_label = tk.Label(self.master, text="Enter Track Number to Add to Playlist", font=("Helvetica", 12))
        instruction_label.pack(pady=(10, 5))

        self.track_number_entry = tk.Entry(self.master, width=10)
        self.track_number_entry.pack(pady=5)

        add_button = tk.Button(self.master, text="Add Track", command=self.add_track)
        add_button.pack(pady=5)

        self.playlist_text = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=40, height=10)
        self.playlist_text.pack(pady=10)
        self.playlist_text.config(state=tk.DISABLED)  # Disable text area to prevent manual editing

        play_button = tk.Button(self.master, text="Play Playlist", command=self.play_playlist)
        play_button.pack(pady=5)

        reset_button = tk.Button(self.master, text="Reset Playlist", command=self.reset_playlist)
        reset_button.pack(pady=5)

    def add_track(self):
        """Add track to the playlist."""
        try:
            track_number = int(self.track_number_entry.get())  # Get track number from entry
            if 1 <= track_number <= len(self.tracks):
                track_info = self.tracks[track_number - 1]  # Get track information based on track number
                self.playlist.append(track_info['title'])  # Add track title to the playlist
                self.update_playlist_display()  # Update playlist display
                messagebox.showinfo("Success", f"Added: {track_info['title']} by {track_info['singer']}")
            else:
                messagebox.showerror("Error", "Invalid track number.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer.")

    def update_playlist_display(self):
        """Update the displayed playlist."""
        self.playlist_text.config(state=tk.NORMAL)
        self.playlist_text.delete(1.0, tk.END)  # Clear the text area
        for track in self.playlist:
            self.playlist_text.insert(tk.END, f"{track}\n")  # Insert each track into the text area
        self.playlist_text.config(state=tk.DISABLED)

    def play_playlist(self):
        """Simulate playing the playlist and increment play counts."""
        if not self.playlist:
            messagebox.showwarning("Warning", "Playlist is empty. Please add tracks first.")
            return

        for track_title in self.playlist:
            for track in self.tracks:
                if track['title'] == track_title:
                    track['play_count'] += 1  # Increment the play count
                    break
        
        # Save updated play counts back to song.json
        try:
            with open('song.json', 'w') as file:
                json.dump(self.tracks, file, indent=4)  # Save the updated tracks list
            messagebox.showinfo("Info", "Playlist played! (Counts updated)")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save play counts: {e}")

    def reset_playlist(self):
        """Reset the playlist."""
        self.playlist.clear()  # Clear the playlist
        self.playlist_text.config(state=tk.NORMAL)
        self.playlist_text.delete(1.0, tk.END)  # Clear the text area
        self.playlist_text.config(state=tk.DISABLED)
        messagebox.showinfo("Info", "Playlist reset.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrackListApp(root)
    root.mainloop()
