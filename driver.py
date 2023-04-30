"""
Author: Austin Lee 5/2/2023
Title: Harry Potter Characters App

This Python app creates a GUI application using tkinter and PIL libraries to display information about Harry Potter characters.
The data is stored in an SQLite database, which is queried to populate the app's dropdown menu and display relevant information.

Dependencies:

Python 3.x
tkinter
sqlite3
Pillow (PIL fork)
How to run:

Install the required dependencies.
Make sure you have a valid SQLite database file named "harry_potter_characters.db" with the required schema.
Run the script using python script_name.py.
"""

import sqlite3
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class HarryPotterCharactersApp(tk.Tk):
    """
    The main class for the Harry Potter Characters application, which inherits from tkinter's Tk class.
    This class initializes the app's UI and handles database interactions.
    """
    def __init__(self, database_file):
        super().__init__()
        self.database_file = database_file
        self.characters = self.get_characters()
        self.character_var = tk.StringVar()
        self.image_label = tk.Label(self)

        self.title("Harry Potter Characters App")
        self.geometry("800x600")

        title_label = tk.Label(self, text="Harry Potter Characters", font=("Helvetica", 20))
        title_label.pack(side="top", pady=10)

        self.character_var.set('Pick a character.')
        self.dropdown = ttk.Combobox(self, textvariable=self.character_var, state="readonly")
        self.dropdown["values"] = [f"{c[0]}, {c[1]}" for c in self.characters]
        self.dropdown.bind('<<ComboboxSelected>>', self.on_character_selected)
        self.dropdown.pack(pady=10)

        self.image_label.pack()

    def get_characters(self):
        """
        Retrieves the list of characters from the SQLite database.

        Returns:
            characters (list): A list of tuples containing character last_name and first_name.
        """
        connection = sqlite3.connect(self.database_file)
        cursor = connection.cursor()
        cursor.execute('SELECT last_name, first_name FROM characters')
        characters = cursor.fetchall()
        connection.close()
        return characters

    def on_character_selected(self, event):
        """
        Event handler for when a character is selected in the dropdown menu.
        It updates the character's image and information displayed in the application.

        Args:
            event (tkinter.Event): The event object generated when a character is selected.
        """
        selected_index = self.dropdown.current()
        selected_character_last_name = self.characters[selected_index][0]
        selected_character_first_name = self.characters[selected_index][1]
        connection = sqlite3.connect(self.database_file)
        cursor = connection.cursor()
        cursor.execute('SELECT last_name, first_name, occupation, image_path FROM characters WHERE last_name=? AND first_name=?', (selected_character_last_name, selected_character_first_name))
        character_info = cursor.fetchall()[0]
        connection.close()

        image = Image.open(character_info[3])
        image.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo
        
        if hasattr(self, "info_label"):
            self.info_label.destroy()

        last_name, first_name, occupation, image_path = character_info
        self.info_label = tk.Label(self, text=f'Name: {first_name} {last_name}\nOccuopation: {occupation}')
        self.info_label.pack(side="top", pady=10)



if __name__ == '__main__':
    app = HarryPotterCharactersApp("harry_potter_characters.db")
    app.mainloop()
