from tkinter import *
from tkinter import messagebox
import json
import random
import string
from pathlib import Path

# ---------------------------- PATH SETUP ------------------------------- #

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data.json"
LOGO_FILE = BASE_DIR / "logo.png"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = string.ascii_letters
    numbers = string.digits
    symbols = "!@#$%^&*()"

    password_characters = (
        random.choices(letters, k=8) +
        random.choices(numbers, k=4) +
        random.choices(symbols, k=2)
    )

    random.shuffle(password_characters)
    password = "".join(password_characters)

    password_entry.delete(0, END)
    password_entry.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    if not website or not password:
        messagebox.showerror("Error", "Website and Password cannot be empty!")
        return

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    try:
        if DATA_FILE.exists():
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
        else:
            data = {}

        data.update(new_data)

        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)

    except json.JSONDecodeError:
        messagebox.showerror("Error", "Data file corrupted!")
        return

    messagebox.showinfo("Success", "Password saved successfully!")

    website_entry.delete(0, END)
    password_entry.delete(0, END)

# ---------------------------- SEARCH PASSWORD ------------------------------- #

def search():
    website = website_entry.get().strip()

    if not DATA_FILE.exists():
        messagebox.showerror("Error", "No data file found!")
        return

    with open(DATA_FILE, "r") as file:
        data = json.load(file)

    if website in data:
        email = data[website]["email"]
        password = data[website]["password"]
        messagebox.showinfo(
            title=website,
            message=f"Email: {email}\nPassword: {password}"
        )
    else:
        messagebox.showerror("Not Found", "No details for the website exists.")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# ---------- CENTER WINDOW ----------
WINDOW_WIDTH = 520
WINDOW_HEIGHT = 450

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width // 2) - (WINDOW_WIDTH // 2)
y = (screen_height // 2) - (WINDOW_HEIGHT // 2)

window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
window.resizable(False, False)
# ------------------------------------

canvas = Canvas(height=200, width=200)
if LOGO_FILE.exists():
    logo_img = PhotoImage(file=LOGO_FILE)
    canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
Label(text="Website:").grid(row=1, column=0)
Label(text="Email/Username:").grid(row=2, column=0)
Label(text="Password:").grid(row=3, column=0)

# Entries
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "Sairaj@gmail.com")

password_entry = Entry(width=21, show="*")
password_entry.grid(row=3, column=1)

# Buttons
Button(text="Search", width=13, command=search).grid(row=1, column=2)
Button(text="Generate", command=generate_password).grid(row=3, column=2)
Button(text="Add", width=36, command=save).grid(row=4, column=1, columnspan=2)

window.mainloop()