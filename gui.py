"""
File: gui.py
Author: Grace Todd
Date: Oct 14, 2024
Description: A test implementation for a GUI to streamline the foliager process.
            Requires Python version 3.12 or greater
"""

import tkinter as tk
from tkinter import filedialog, Toplevel
import time
import os

initial_trees = 100 # initial_trees = forest.num_trees

# Define the function to be called when the button is clicked
def on_button_click():
    # Disable the buttons while processing
    generate_button.config(state=tk.DISABLED)
    filepath_button.config(state=tk.DISABLED)
    
    # Simulate a time-consuming operation (replace this with your actual function)
    print("=== Generating forest ===")
    start_trees = initial_trees
    user_location = location.get()

    print(f'Location: {user_location}')
    print(f'Number of trees: {start_trees}')
    
    time.sleep(5)  # Simulating a long-running function with sleep

    # Once the function is complete, re-enable the button
    print("=== Forest generated! ===")
    generate_button.config(state=tk.NORMAL)


# Define a function to open the file dialog
def select_file_path():
    file_path = filedialog.askdirectory()  # Opens a dialog to select a directory
    if file_path:  # If a directory is selected
        # Get the last two directories from the file path
        split_path = file_path.split(os.sep)
        last_two_dirs = os.path.join("..", *split_path[-2:])  # Join the last two directories with "../"
        filepath_button.config(text=last_two_dirs)  # Update the button text with the last two directories
        print(f"Output to: {file_path}")


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


def create_gui():
    global root, generate_button, filepath_button, location

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
    location_label = tk.Label(root, text="Choose an area/location/climate for your forest below:", font=("Helvetica", 14))
    location_label.pack(pady=5)

    # Add a text box (Entry widget) for user input
    location = tk.Entry(root, width=40)
    location.pack(pady=10)

    # Add a button to open the file dialog, which will display the path as the button text
    filepath_button = tk.Button(root, text="Choose Filepath", command=select_file_path)
    filepath_button.pack(pady=10)

    # Add a button that calls the function when clicked, but only the first time
    generate_button = tk.Button(root, text="Generate", command=on_button_click)
    generate_button.pack(pady=20)

    # Add a check box
    checkbox_var = tk.IntVar()  # Variable to store checkbox state
    checkbox = tk.Checkbutton(root, text="Open Blender", variable=checkbox_var)
    checkbox.pack(pady=10)

    # Start the main loop to display the window
    root.mainloop()


if __name__ == '__main__':
    create_gui()