"""
File: gui.py
Author: Grace Todd
Date: Oct 14, 2024
Description: A test implementation for a GUI to streamline the foliager process.
            Requires Python version 3.12 or greater
"""

import tkinter as tk
from tkinter import filedialog, Toplevel
import os

initial_trees = 100 # initial_trees = forest.num_trees

# Define the function to be called when the button is clicked
def on_button_click():
    # Get the text from the text box
    user_input = text_box.get()
    # Print or process the input (for demonstration, we print it)
    print(f"Location: {user_input}")


# Define a function to open the file dialog
def select_file_path():
    file_path = filedialog.askdirectory()  # Opens a dialog to select a directory
    if file_path:  # If a directory is selected
        # Get the last two directories from the file path
        split_path = file_path.split(os.sep)
        last_two_dirs = os.path.join("..", *split_path[-2:])  # Join the last two directories with "../"
        file_button.config(text=last_two_dirs)  # Update the button text with the last two directories


# Define a function to open the settings window
def open_settings():
    global initial_trees  # Access the global initial_trees variable
    
    # Create a new top-level window (the settings window)
    settings_window = Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("300x200")
    
    # Add some settings options
    tk.Label(settings_window, text="Settings Page", font=("Helvetica", 14)).pack(pady=10)
    
    # Create a frame to hold the label and spinbox on the same row
    settings_frame = tk.Frame(settings_window)
    settings_frame.pack(pady=10)
    
    # Add the Initial Trees label and spinbox in the same row
    tk.Label(settings_frame, text="Initial Trees:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5)
    
    initial_trees_var = tk.IntVar(value=initial_trees)  # Create a variable to store the value
    initial_trees_spinbox = tk.Spinbox(settings_frame, from_=1, to=100000, textvariable=initial_trees_var)
    initial_trees_spinbox.grid(row=0, column=1, padx=5, pady=5)
    
    # Function to save the new value of initial trees
    def save_settings():
        global initial_trees
        initial_trees = initial_trees_var.get()  # Get the value from the Spinbox
        print(f"New Initial Trees: {initial_trees}")
        settings_window.destroy()  # Close the settings window

    # Add a button to save and close the settings window
    tk.Button(settings_window, text="Save", command=save_settings).pack(pady=20)


if __name__ == '__main__':
    # Create the main window
    root = tk.Tk()
    root.title("Foliager")

    # Set window size
    root.geometry("400x300")

    # Add a banner with the title "Foliager"
    banner = tk.Label(root, text="Foliager", font=("Helvetica", 24), pady=20)
    banner.pack()

    # Add an icon/button in the top-left corner to open settings
    settings_icon = tk.Button(root, text="⚙️", font=("Helvetica", 12), command=open_settings)
    settings_icon.place(x=5, y=5)  # Placing the button in the top-left corner

    # Add a label for the text box
    text_box_label = tk.Label(root, text="Choose an area/location/climate for your forest below:", font=("Helvetica", 14))
    text_box_label.pack(pady=5)

    # Add a text box (Entry widget) for user input
    text_box = tk.Entry(root, width=40)
    text_box.pack(pady=10)

    # Add a button to open the file dialog, which will display the path as the button text
    file_button = tk.Button(root, text="Choose Filepath", command=select_file_path)
    file_button.pack(pady=10)

    # Add a button that calls the function when clicked, but only the first time
    button = tk.Button(root, text="Generate", command=on_button_click)
    button.pack(pady=20)

    # Add a check box
    checkbox_var = tk.IntVar()  # Variable to store checkbox state
    checkbox = tk.Checkbutton(root, text="Open Blender", variable=checkbox_var)
    checkbox.pack(pady=10)

    # Start the main loop to display the window
    root.mainloop()
