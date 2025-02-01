# functionality.py
import tkinter as tk
from tkinter import messagebox, scrolledtext , ttk
import mysql.connector
import matplotlib.pyplot as plt

# Define global database credentials
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Maha@1983"
DB_DATABASE = "dbms1"

# Define global variables
add_window = None
user_id = None

def setup_registration_interface(root):
    # Create a title label
    title_label = tk.Label(root, text="Register for Personal Finance Tracker", font=("Arial", 16))
    title_label.pack(pady=20)  # Adjust the padding as needed

    # Create entry fields for registration details
    name_label = tk.Label(root, text="Name:")
    name_label.pack()
    name_entry = tk.Entry(root)
    name_entry.pack()

    email_label = tk.Label(root, text="Email:")
    email_label.pack()
    email_entry = tk.Entry(root)
    email_entry.pack()

    phone_label = tk.Label(root, text="Phone:")
    phone_label.pack()
    phone_entry = tk.Entry(root)
    phone_entry.pack()

    dob_label = tk.Label(root, text="Date of Birth (YYYY-MM-DD):")
    dob_label.pack()
    dob_entry = tk.Entry(root)
    dob_entry.pack()

    user_id_label = tk.Label(root, text="User ID:")
    user_id_label.pack()
    user_id_entry = tk.Entry(root)
    user_id_entry.pack()

    password_label = tk.Label(root, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(root, show="*")  # Show '*' for password entry
    password_entry.pack()

    # Create register button
    register_button = tk.Button(root, text="Register", command=lambda: register(name_entry, email_entry, phone_entry, dob_entry, user_id_entry, password_entry, root))
    register_button.pack(pady=10)

    # Create a button to go back to the login page
    back_button = tk.Button(root, text="Back to Login", command=lambda: back_to_login(root))
    back_button.pack(pady=10)


# Function to perform user registration
def register(name_entry, email_entry, phone_entry, dob_entry, user_id_entry, password_entry, root):
    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    dob = dob_entry.get()
    user_id = user_id_entry.get()
    password = password_entry.get()

    # Validate inputs (you can add your validation logic here)

    # Connect to MySQL database
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
    cursor = db.cursor()

    # Check if the user ID already exists
    cursor.execute("SELECT * FROM user WHERE user_id = %s", (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        messagebox.showerror("Error", "User ID already exists. Please choose a different one.")
    else:
        # Execute query to add new user
        query = "INSERT INTO user (name, user_email, user_num, user_dob, user_id, password) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (name, email, phone, dob, user_id, password))
        db.commit()

        messagebox.showinfo("Success", "Registration successful. You can now log in.")

    db.close()
    
# Function to set up the login interface
def setup_login_interface(root):
    # Create a title label
    title_label = tk.Label(root, text="Personal Finance Tracker", font=("Arial", 16))
    title_label.pack(pady=20)  # Adjust the padding as needed

    # Create user ID and password entry fields
    user_id_label = tk.Label(root, text="User ID:")
    user_id_label.pack()
    user_id_entry = tk.Entry(root)
    user_id_entry.pack()

    password_label = tk.Label(root, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(root, show="*")  # Show '*' for password entry
    password_entry.pack()

    # Create login button
    login_button = tk.Button(root, text="Login", command=lambda: login(user_id_entry, password_entry, root))
    login_button.pack(pady=10)

# Function to perform the login
def login(user_id_entry, password_entry, root):
    global user_id
    user_id = user_id_entry.get()
    password = password_entry.get()

    # Connect to MySQL database
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
    cursor = db.cursor()

    # Execute login query
    query = "SELECT * FROM user WHERE user_id = %s AND password = %s"
    cursor.execute(query, (user_id, password))
    user = cursor.fetchone()

    if user:
        show_dashboard(user_id, user[1], root, cursor)  # Pass user ID and name to dashboard
        root.withdraw()  # Hide the login window
    else:
        messagebox.showerror("Error", "Invalid user ID or password")

    db.close()


def show_dashboard(user_id, name, root, cursor):
    dashboard = tk.Toplevel(root)
    dashboard.title("Dashboard")
    dashboard.configure(bg="black")
    # Get screen width for positioning
    screen_width = root.winfo_screenwidth()

    # Set window size to maximize
    dashboard.geometry(f"{screen_width}x600+0+0")

    # Create a notebook (tabs container) for different sections of the dashboard
    notebook = ttk.Notebook(dashboard)
    notebook.pack(fill="both", expand=True)

    # Home tab
    home_frame = ttk.Frame(notebook)
    notebook.add(home_frame, text="Home")

    # Dashboard header
    header_label = tk.Label(home_frame, text=f"Welcome User Id {user_id} \n Name:{name}", font=("Arial", 16))
    header_label.pack(pady=20)
    # Label for recent transactions
    recent_transactions_label = tk.Label(home_frame, text="Recent Transactions", font=("Arial", 14))
    recent_transactions_label.pack()
    # Dashboard content
    # Get user transaction logs
    transaction_logs = get_user_transactions(user_id, cursor)

    # Create a scrolled text widget for navigable content
    text_area = scrolledtext.ScrolledText(home_frame, wrap=tk.WORD, width=100, height=20)
    text_area.pack(pady=20)

    # Display transaction logs in the text area
    for log in transaction_logs:
        text_area.insert(tk.END, f"{log[2]} - {log[3]}\n")  # Assuming log_description and log_date are in position 2 and 3

    # Add a button to show user balance and credentials
    show_records_button = tk.Button(home_frame, text="Show Records & Balance", command=lambda: show_user_credentials(user_id))
    show_records_button.pack(pady=10)

    # Second tab for adding entries
    add_entry_frame = ttk.Frame(notebook)
    notebook.add(add_entry_frame, text="Add Entry")

    # Button to add entry
    add_entry_button = tk.Button(add_entry_frame, text="Add Entry", command=add_entry)
    add_entry_button.pack(pady=20)

    # Button to show pie chart
    show_pie_chart_button = tk.Button(home_frame, text="Show Pie Chart", command=lambda : show_pie_chart(user_id))
    show_pie_chart_button.pack(pady=10)

    # Button to return to login
    return_to_login_button = tk.Button(home_frame, text="Return to Login", command=lambda: back_to_login(dashboard, root))
    return_to_login_button.pack(pady=10)


def back_to_login(window, root):
    window.destroy()
    root.deiconify()

def get_user_balance(user_id, cursor):
    # Execute query to get user balance
    query = "SELECT available_balance FROM balance WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    balance = cursor.fetchone()[0]  # Fetch the balance value from the result

    return balance


def show_user_balance(user_id):
    # Function to show user balance in a temporary window
    balance_window = tk.Toplevel()
    balance_window.title("User Balance")
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
    cursor = db.cursor()
    # Get user balance
    balance = get_user_balance(user_id, cursor)

    # Display user balance
    balance_label = tk.Label(balance_window, text=f"User ID: {user_id}\nBalance: {balance}")
    balance_label.pack(padx=20, pady=20)

    # Button to close the window
    close_button = tk.Button(balance_window, text="Close", command=balance_window.destroy)
    close_button.pack(pady=10)
    cursor.close()

def get_user_transactions(user_id, cursor):
    # Call the stored procedure to generate transaction logs
    cursor.callproc("GenerateTransactionLogs", (user_id,))
    
    # Fetch all transaction logs for the user
    cursor.execute("SELECT * FROM transaction_logs WHERE user_id = %s", (user_id,))
    return cursor.fetchall()


def add_entry():
    global add_window

    def save_transaction():
        # Get values from entry fields
        description = description_entry.get()
        amount = amount_entry.get()
        trans_date = trans_date_entry.get()
        label_id = label_id_entry.get()
        tran_type = tran_type_var.get()  # Get the selected transaction type (credit or debit)

        # Validate inputs (you can add your validation logic here)

        # Insert transaction into the database
        # For label_id, you might need to convert it to int if it's coming as a string
        save_entry(description, amount, trans_date, tran_type, int(label_id) if label_id else None)

        # Close the add_entry window
        add_window.destroy()

    # Functionality for adding an entry
    add_window = tk.Toplevel()
    add_window.title("Add Entry")

    # Entry fields for the new entry
    description_label = tk.Label(add_window, text="Description:")
    description_label.pack()
    description_entry = tk.Entry(add_window, width=50)
    description_entry.pack()

    amount_label = tk.Label(add_window, text="Amount:")
    amount_label.pack()
    amount_entry = tk.Entry(add_window)
    amount_entry.pack()

    trans_date_label = tk.Label(add_window, text="Transaction Date:")
    trans_date_label.pack()
    trans_date_entry = tk.Entry(add_window)
    trans_date_entry.pack()

    label_id_label = tk.Label(add_window, text="Label ID:")
    label_id_label.pack()
    label_id_entry = tk.Entry(add_window)
    label_id_entry.pack()

    # Transaction type selection
    tran_type_var = tk.StringVar()
    tran_type_label = tk.Label(add_window, text="Transaction Type:")
    tran_type_label.pack()
    tran_type_dropdown = ttk.Combobox(add_window, textvariable=tran_type_var, values=["credit", "debit"])
    tran_type_dropdown.pack()

    # Submit button to add the entry
    submit_button = tk.Button(add_window, text="Submit", command=save_transaction)
    submit_button.pack()

from datetime import datetime

def save_entry(description, amount, trans_date, tran_type, label_id):
    # Convert trans_date to the correct format (YYYY-MM-DD)
    trans_date_obj = datetime.strptime(trans_date, "%d-%m-%Y")
    trans_date_formatted = trans_date_obj.strftime("%Y-%m-%d")

    # Function to save the new entry to the database
    global user_id
    # Connect to MySQL database
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
    cursor = db.cursor()

    # Execute query to add new entry
    query = "INSERT INTO transaction (user_id, tran_type, amount, trans_date, label_id) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (user_id, tran_type, amount, trans_date_formatted, label_id))
    db.commit()

    db.close()

    # Close the add entry window
    add_window.destroy()

def show_user_credentials(user_id):
    # Connect to MySQL database
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
    cursor = db.cursor()

    # Get user credentials
    cursor.execute("SELECT * FROM user WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()

    # Get user balance
    cursor.execute("SELECT available_balance FROM balance WHERE user_id = %s", (user_id,))
    balance = cursor.fetchone()[0]

    # Close the database connection
    db.close()

    # Create a pop-up window to display user details and balance
    popup_window = tk.Toplevel()
    popup_window.title("User Details & Balance")

    # Display user details
    user_details_label = tk.Label(popup_window, text=f"User ID: {user[0]}\nName: {user[1]}\nEmail: {user[2]}\nPhone: {user[3]}\nBalance: {balance}")
    user_details_label.pack(padx=20, pady=20)

    # Button to close the pop-up window
    close_button = tk.Button(popup_window, text="Close", command=popup_window.destroy)
    close_button.pack(pady=10)


def show_pie_chart(user_id):
    # Connect to MySQL database
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
    cursor = db.cursor()

    # Get user spending information
    cursor.execute("SELECT tran_type, SUM(amount) FROM transaction WHERE user_id = %s GROUP BY tran_type", (user_id,))
    spending_data = cursor.fetchall()

    # Close the database connection
    db.close()

    # Create the pie chart
    labels = [data[0] for data in spending_data]
    amounts = [data[1] for data in spending_data]

    plt.figure(figsize=(6, 6))
    plt.pie(amounts, labels=labels, autopct="%1.1f%%")
    plt.title("Spending Distribution")
    plt.axis("equal")
    plt.show()
