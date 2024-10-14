"""
File: gui.py
Author: Grace Todd
Date: Oct 14, 2024
Description: A test implementation for a GUI to streamline the foliager process.
            Requires Python version 3.12 or greater
"""

import tkinter as tk

# Define the function to be called when the button is clicked
def on_button_click():
    # Get the text from the text box
    user_input = text_box.get()
    # Print or process the input (for demonstration, we print it)
    print(f"User Input: {user_input}")

# Create the main window
root = tk.Tk()
root.title("Foliager")

# Set window size
root.geometry("400x300")

# Add a banner with the title "Foliager"
banner = tk.Label(root, text="Foliager", font=("Helvetica", 24), pady=20)
banner.pack()

# Add a label for the text box
text_box_label = tk.Label(root, text="Choose an area/location/climate for your forest below:", font=("Helvetica", 14))
text_box_label.pack(pady=5)

# Add a text box (Entry widget) for user input
text_box = tk.Entry(root, width=40)
text_box.pack(pady=10)

# Add a button that calls the function when clicked
button = tk.Button(root, text="Generate", command=on_button_click)
button.pack(pady=20)

# Add a check box
checkbox_var = tk.IntVar()  # Variable to store checkbox state
checkbox = tk.Checkbutton(root, text="Open Blender", variable=checkbox_var)
checkbox.pack(pady=10)

# Start the main loop to display the window
root.mainloop()
