import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

SONG_FILE = 'song.json'

class Updatetracks:
    @staticmethod
    def load_list():
        """Load the list of songs from the JSON file."""
        if not os.path.exists(SONG_FILE):
            return []
        with open(SONG_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def save_list(tracks):
        """Save the list of songs to the JSON file."""
        with open(SONG_FILE, 'w', encoding='utf-8') as file:
            json.dump(tracks, file, indent=4)

    @staticmethod
    def update_rating(track_number, new_rating):
        """Update the rating of a song."""
        tracks = Updatetracks.load_list()
        try:
            index = int(track_number) - 1  # Convert to zero-based index
            if 0 <= index < len(tracks):
                track = tracks[index]
                old_rating = track.get("rating", "Not rated")
                track["rating"] = new_rating
                Updatetracks.save_list(tracks)
                messagebox.showinfo("Success", f"Track: {track['title']}\nNew Rating: {new_rating}\nOld Rating: {old_rating}")
            else:
                messagebox.showerror("Error", "Invalid track number.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

class UpdateTracksWindow:
    def __init__(self, root):
        """Initialize the UpdateTracks window."""
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        """Set up the UI for updating track ratings."""
        self.window = tk.Toplevel(self.root)
        self.window.title("Update Track Rating")

        frame = ttk.Frame(self.window, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Track Number:").grid(row=0, column=0, sticky=tk.W)
        self.track_number_entry = ttk.Entry(frame)
        self.track_number_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

        ttk.Label(frame, text="New Rating:").grid(row=1, column=0, sticky=tk.W)

        # Create a style for the star buttons
        style = ttk.Style()
        style.configure('StarButton.TButton', font=('Arial', 20), foreground='gray')
        style.configure('StarButtonSelected.TButton', font=('Arial', 20), foreground='gold')

        # Create star buttons for rating
        self.star_buttons = []
        self.selected_rating = tk.IntVar(value=0)

        def set_rating(rating):
            """Set the selected star rating and update button styles."""
            self.selected_rating.set(rating)
            for i in range(5):
                if i < rating:
                    self.star_buttons[i].config(style='StarButtonSelected.TButton')
                else:
                    self.star_buttons[i].config(style='StarButton.TButton')

        for i in range(1, 6):
            button = ttk.Button(frame, text='★', command=lambda i=i: set_rating(i), width=3, style='StarButton.TButton')
            button.grid(row=1, column=i - 1, sticky=(tk.W, tk.E), padx=2)
            self.star_buttons.append(button)

        # Create the update button
        ttk.Button(frame, text="Update Rating", command=self.update_rating).grid(row=2, column=0, columnspan=5, pady=5)

    def update_rating(self):
        """Get the input and call the update_rating method from Updatetracks."""
        track_number = self.track_number_entry.get().strip()
        new_rating = self.selected_rating.get()
        
        # Call the update function
        Updatetracks.update_rating(track_number, new_rating)

        # Close the update window after updating
        self.window.destroy()

def main():
    """Main function to run the update tracks window standalone."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    update_window = UpdateTracksWindow(root)  # Create an instance of UpdateTracksWindow
    root.mainloop()  # Start the Tkinter main loop

if __name__ == "__main__":
    main()
