import tkinter as tk
from tkinter import Entry, Button, Label, messagebox, scrolledtext
import mysql.connector
from functionality import login, setup_login_interface ,setup_registration_interface

# Tkinter setup
root = tk.Tk()
root.title("Login")
# Set background color
root.configure(bg="lightblue")
root.state("zoomed")  # Maximize the main window




# Call the function to set up the login interface
setup_login_interface(root)
# Function to switch to the registration interface
def switch_to_registration():
    for widget in root.winfo_children():
        widget.destroy()
    setup_registration_interface(root)

# Create a button to switch to the registration interface
register_button = tk.Button(root, text="Register", command=switch_to_registration)
register_button.pack(pady=10)

root.mainloop()

