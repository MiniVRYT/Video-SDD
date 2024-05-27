import tkinter as tk  # Import tkinter for GUI
from tkinter import ttk  # Import themed tkinter widgets
from tkinter import filedialog  # Import file dialog from tkinter
import csv  # Import csv module for CSV file handling
from PIL import Image, ImageTk  # type: ignore # Import Image and ImageTk from PIL library
import requests  # type: ignore # Import requests library for making HTTP requests
from imdb import IMDb  # type: ignore # Import IMDb class from imdb module

class MovieSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CineMATE")  # Set window title to "CineMATE"
        self.setup_gui()  # Call the method to set up GUI elements

        self.imdb = IMDb()  # Initialize IMDb object for movie search
        self.watch_later_movies = []  # Initialize list to store movies for watch later

    def setup_gui(self):
        self.root.configure(background='#f0f0f0')  # Set background color to light grey

        # Create label for the application
        cine_label = tk.Label(self.root, text="CineMATE", font=("Arial", 24, "bold"), fg="red", bd=2, relief=tk.SOLID)
        cine_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Create entry widget for movie search
        self.search_entry = ttk.Entry(self.root, width=40)
        self.search_entry.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        # Create search button
        self.search_button = ttk.Button(self.root, text="Search", command=self.search_movie)
        self.search_button.grid(row=1, column=2, padx=5, pady=10)

        # Create button to display watch later list
        self.watch_later_button = ttk.Button(self.root, text="Watch Later", command=self.show_watch_later)
        self.watch_later_button.grid(row=1, column=3, padx=5, pady=10)

        # Create frame to display search results
        self.result_frame = ttk.Frame(self.root)
        self.result_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky=tk.W)

        # Create scrollbar for result listbox
        self.result_scrollbar = ttk.Scrollbar(self.result_frame, orient=tk.VERTICAL)
        self.result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create listbox to display search results
        self.result_listbox = tk.Listbox(self.result_frame, yscrollcommand=self.result_scrollbar.set, width=50, height=25)
        self.result_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.result_scrollbar.config(command=self.result_listbox.yview)

        # Bind click event to display movie info and add button
        self.result_listbox.bind("<ButtonRelease-1>", self.show_movie_info_and_add_button)

        # Create frame to display movie info
        self.movie_info_frame = ttk.Frame(self.root)
        self.movie_info_frame.grid(row=2, column=4, padx=10, pady=10, sticky=tk.N)

        # Create labels for movie info
        self.movie_title_label = ttk.Label(self.movie_info_frame, text="Title:")
        self.movie_title_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.movie_rating_label = ttk.Label(self.movie_info_frame, text="Rating:")
        self.movie_rating_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.movie_length_label = ttk.Label(self.movie_info_frame, text="Length:")
        self.movie_length_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.movie_age_rating_label = ttk.Label(self.movie_info_frame, text="Age Rating:")
        self.movie_age_rating_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.movie_genre_label = ttk.Label(self.movie_info_frame, text="Genre:")
        self.movie_genre_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.movie_image_label = ttk.Label(self.movie_info_frame, text="Movie Image:")
        self.movie_image_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)

        # Create variables to store movie info
        self.movie_title_var = tk.StringVar()
        self.movie_rating_var = tk.StringVar()
        self.movie_length_var = tk.StringVar()
        self.movie_age_rating_var = tk.StringVar()

        # Create entry widgets to display movie info
        self.movie_title_entry = ttk.Entry(self.movie_info_frame, textvariable=self.movie_title_var, state="readonly", width=30)
        self.movie_title_entry.grid(row=0, column=1, padx=5, pady=5)
        self.movie_rating_entry = ttk.Entry(self.movie_info_frame, textvariable=self.movie_rating_var, state="readonly", width=30)
        self.movie_rating_entry.grid(row=1, column=1, padx=5, pady=5)
        self.movie_length_entry = ttk.Entry(self.movie_info_frame, textvariable=self.movie_length_var, state="readonly", width=30)
        self.movie_length_entry.grid(row=2, column=1, padx=5, pady=5)
        self.movie_age_rating_entry = ttk.Entry(self.movie_info_frame, textvariable=self.movie_age_rating_var, state="readonly", width=30)
        self.movie_age_rating_entry.grid(row=3, column=1, padx=5, pady=5)
        self.movie_genre_entry = ttk.Entry(self.movie_info_frame, state="readonly", width=30)
        self.movie_genre_entry.grid(row=4, column=1, padx=5, pady=5)

        # Create canvas to display movie image
        self.movie_image_canvas = tk.Canvas(self.movie_info_frame, width=250, height=350)
        self.movie_image_canvas.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

        # Bind <Return> key event to search_movie function
        self.root.bind("<Return>", lambda event: self.search_movie())

    def search_movie(self, event=None):
        # Clear previous search results
        self.result_listbox.delete(0, tk.END)
        title = self.search_entry.get()  # Get movie title from entry widget
        if title:
            movie_list = self.imdb.search_movie(title)  # Search for movies on IMDb
            if movie_list:
                for movie in movie_list:
                    self.result_listbox.insert(tk.END, movie["title"])  # Insert movie titles into listbox
            else:
                self.result_listbox.insert(tk.END, "No movies found.")  # Display message if no movies found
        else:
            self.result_listbox.insert(tk.END, "Please enter a movie title to search.")  # Prompt user to enter a movie title

    def show_movie_info_and_add_button(self, event):
        selection = self.result_listbox.curselection()  # Get selected movie from listbox
        if selection:
            index = selection[0]
            movie_title = self.result_listbox.get(index)
            movie_list = self.imdb.search_movie(movie_title)  # Search for movies on IMDb
            if movie_list:
                movie_id = movie_list[0].movieID
                movie_details = self.imdb.get_movie(movie_id)
                self.movie_title_var.set(movie_title)
                self.movie_rating_var.set(str(movie_details.get("rating")))
                self.movie_length_var.set(movie_details.get("runtimes")[0])
                age_rating = self.extract_australian_rating(movie_details)
                self.movie_age_rating_var.set(age_rating)
                self.load_movie_image(movie_details)
                self.display_movie_genre(movie_details)  # Display movie genre
                # Create button to add movie to watch later list
                add_to_watch_later_button = ttk.Button(self.movie_info_frame, text="Add to Watch Later", command=lambda: self.add_to_watch_later(movie_title))
                add_to_watch_later_button.grid(row=6, column=1, padx=5, pady=5, sticky=tk.SE)
            else:
                self.show_error_message("Error, requested film not found")  # Show error message if movie not found

    def extract_australian_rating(self, movie_details):
        certificates = movie_details.get("certificates")
        if certificates:
            for certificate in certificates:
                if "Australia" in certificate:
                    return certificate.split(":")[-1]
        return "N/A"

    def load_movie_image(self, movie_details):
        poster_url = movie_details.get("full-size cover url")
        if poster_url:
            try:
                image = Image.open(requests.get(poster_url, stream=True).raw)
                image = image.resize((250, 350))
                self.movie_image = ImageTk.PhotoImage(image)
                self.movie_image_canvas.create_image(0, 0, anchor=tk.NW, image=self.movie_image)
            except Exception as e:
                print(f"Error loading image: {e}")
                self.movie_image_canvas.delete("all")
                self.movie_image_canvas.create_text(125, 175, text="No image found", fill="red", anchor=tk.CENTER)
        else:
            self.movie_image_canvas.delete("all")
            self.movie_image_canvas.create_text(125, 175, text="No image found", fill="red", anchor=tk.CENTER)

    def display_movie_genre(self, movie_details):
        genres = movie_details.get("genres")
        if genres:
            genre_str = ", ".join(genres)
            self.movie_genre_entry.config(state="normal")
            self.movie_genre_entry.delete(0, tk.END)
            self.movie_genre_entry.insert(0, genre_str)
            self.movie_genre_entry.config(state="readonly")

    def show_error_message(self, message):
        error_window = tk.Toplevel(self.root)
        error_window.title("Error")
        error_label = ttk.Label(error_window, text=message)
        error_label.pack(padx=10, pady=10)
        ok_button = ttk.Button(error_window, text="OK", command=error_window.destroy)
        ok_button.pack(padx=10, pady=10)

    def show_watch_later(self):
        # Create window to display watch later list
        watch_later_window = tk.Toplevel(self.root)
        watch_later_window.title("Watch Later List")

        # Create label for watch later list
        watch_later_label = ttk.Label(watch_later_window, text="Movies to Watch Later:")
        watch_later_label.pack(padx=10, pady=10)

        # Create listbox to display watch later list
        self.watch_later_listbox = tk.Listbox(watch_later_window)
        for movie in self.watch_later_movies:
            self.watch_later_listbox.insert(tk.END, movie)
        self.watch_later_listbox.pack(padx=10, pady=10)

        # Create buttons for saving and opening watch later list
        save_csv_button = ttk.Button(watch_later_window, text="Save List as CSV", command=self.save_watch_later_csv)
        save_csv_button.pack(padx=10, pady=10)
        save_txt_button = ttk.Button(watch_later_window, text="Save List as Text", command=self.save_watch_later_txt)
        save_txt_button.pack(padx=10, pady=10)
        open_csv_button = ttk.Button(watch_later_window, text="Open CSV File", command=self.open_watch_later_csv)
        open_csv_button.pack(padx=10, pady=10)

        # Bind double-click event to remove movie from watch later list
        self.watch_later_listbox.bind("<Double-Button-1>", self.remove_from_watch_later)

    def add_to_watch_later(self, movie_title):
        self.watch_later_movies.append(movie_title)  # Add movie to watch later list
        self.watch_later_listbox.insert(tk.END, movie_title)  # Insert movie into listbox
        print(f"Added '{movie_title}' to Watch Later list.")

    def remove_from_watch_later(self, event):
        selection = self.watch_later_listbox.curselection()
        if selection:
            index = selection[0]
            movie_title = self.watch_later_listbox.get(index)
            del self.watch_later_movies[index]  # Remove movie from watch later list
            self.watch_later_listbox.delete(index)  # Delete movie from listbox
            print(f"Removed '{movie_title}' from Watch Later list.")

    def save_watch_later_csv(self):
        # Prompt user to select file location and save watch later list as CSV
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Movie Title'])
                for movie in self.watch_later_movies:
                    writer.writerow([movie])
            print(f"Watch Later list saved as CSV to {file_path}")

    def save_watch_later_txt(self):
        # Prompt user to select file location and save watch later list as text
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, mode='w') as file:
                for movie in self.watch_later_movies:
                    file.write(movie + '\n')
            print(f"Watch Later list saved as text to {file_path}")

    def open_watch_later_csv(self):
        # Prompt user to select CSV file and load watch later list from it
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    self.watch_later_movies.append(row[0])
                    self.watch_later_listbox.insert(tk.END, row[0])
            print(f"Watch Later list loaded from {file_path}")



if __name__ == "__main__":
    root = tk.Tk()  # Create Tkinter root window
    app = MovieSearchApp(root)  # Initialize MovieSearchApp instance
    root.winfo_screenwidth()
    root.winfo_screenheight()
    root.mainloop()  # Run the Tkinter event loop
    
