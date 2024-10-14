"""
File: gui.py
Author: Grace Todd
Date: Oct 14, 2024
Description: A test implementation for a GUI to streamline the foliager process.
"""

import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Foliager")

# Set window size
root.geometry("400x200")

# Add a banner with the title "Foliager"
banner = tk.Label(root, text="Foliager", font=("Helvetica", 24), pady=20)
banner.pack()

# Add a text box (Entry widget) for user input
text_box = tk.Entry(root, width=40)
text_box.pack(pady=10)

# Add a check box
checkbox_var = tk.IntVar()  # Variable to store checkbox state
checkbox = tk.Checkbutton(root, text="Enable Feature", variable=checkbox_var)
checkbox.pack(pady=10)

# Start the main loop to display the window
root.mainloop()
