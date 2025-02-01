import tkinter as tk
from tkinter import messagebox, scrolledtext
import mysql.connector

def login():
    user_id = user_id_entry.get()
    password = password_entry.get()

    # Connect to MySQL database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Maha@1983",
        database="dbms1"
    )
    cursor = db.cursor()

    # Execute login query
    query = "SELECT * FROM user WHERE user_id = %s AND password = %s"
    cursor.execute(query, (user_id, password))
    user = cursor.fetchone()

    if user:
        show_dashboard(user_id, user[1])  # Pass user ID and name to dashboard
        root.withdraw()  # Hide the login window
    else:
        messagebox.showerror("Error", "Invalid user ID or password")

    db.close()

def show_dashboard(user_id, name):
    dashboard = tk.Toplevel(root)
    dashboard.title("Dashboard")

    # Get screen width for positioning
    screen_width = root.winfo_screenwidth()
    
    # Set window size to maximize
    dashboard.geometry(f"{screen_width}x600+0+0")

    # Dashboard header
    header_label = tk.Label(dashboard, text=f"Welcome User {name} \n {user_id} ", font=("Arial", 16))
    header_label.pack(pady=20)

    # Dashboard content
    # You can display the user balance and other content here
    balance_label = tk.Label(dashboard, text="User Balance: $1000", font=("Arial", 14))
    balance_label.pack(side="right", padx=20)

    # Create a scrolled text widget for navigatable content
    text_area = scrolledtext.ScrolledText(dashboard, wrap=tk.WORD, width=100, height=20)
    text_area.pack(pady=20)

    # Example content
    for i in range(1, 101):
        text_area.insert(tk.END, f"This is line {i}\n")

    # Add a button to go back to the login window
    back_button = tk.Button(dashboard, text="Back to Login", command=lambda: back_to_login(dashboard))
    back_button.pack(pady=20)

def back_to_login(window):
    window.destroy()
    root.deiconify


# Tkinter setup
root = tk.Tk()
root.title("Login")

# Set window size to maximize
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")

# Increase font size
font_style = ("Arial", 16)  # Font family and size
label_style = {"font": font_style}

user_id_label = tk.Label(root, text="User ID:", **label_style)
user_id_label.pack()
user_id_entry = tk.Entry(root, font=font_style)
user_id_entry.pack()

password_label = tk.Label(root, text="Password:", **label_style)
password_label.pack()
password_entry = tk.Entry(root, show="*", font=font_style)
password_entry.pack()

login_button = tk.Button(root, text="Login", command=login, font=font_style)
login_button.pack()

root.mainloop()