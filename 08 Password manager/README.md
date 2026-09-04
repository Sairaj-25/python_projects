# 🔐 Secure Password Manager (Tkinter GUI)

A professional desktop-based **Password Manager** built using Python and Tkinter.

This application allows users to securely generate, store, and retrieve credentials for websites using structured JSON storage. Designed with clean UI, validation handling, and modular architecture — making it portfolio-ready and production-improvable.

---

## 🚀 Features

- 🖥️ Clean GUI built with Tkinter
- 🔑 Strong random password generator
- 💾 JSON-based structured storage
- 🔍 Search functionality for saved credentials
- 🔒 Hidden password input field
- 📂 Automatic file creation
- 🖼️ Logo support
- 🧭 Window opens centered on screen
- ⚠️ Input validation & error handling

---

## 🧰 Tech Stack

| Technology | Purpose |
|------------|----------|
| Python 3.x | Core language |
| Tkinter | GUI Framework |
| JSON | Structured data storage |
| Pathlib | Cross-platform path handling |
| Random & String | Secure password generation |
| Messagebox | User feedback & alerts |

---

## 📂 Project Structure

```

08 Password manager/
│
├── main.py
├── data.json
├── logo.png
└── README.md

```


---

## 🔐 How It Works

### 1️⃣ Generate Password
- Creates a strong password using:
  - Letters (uppercase + lowercase)
  - Numbers
  - Special symbols
- Automatically inserts into password field.

---

### 2️⃣ Save Credentials
- Validates website & password fields
- Stores credentials in structured JSON format:

```
json
{
    "google.com": {
        "email": "user@gmail.com",
        "password": "Xy@93#kLp1"
    }
}

```
=======
# 🔐 Python Password Manager

A simple **Password Manager** built with Python to securely generate and manage credentials for websites and services.

This project allows users to **store, search, and retrieve passwords** using a clean interface. It focuses on simplicity, usability, and learning core Python concepts.

---

##  Features

-  Generate strong and secure passwords
-  Save website credentials locally
-  Search and retrieve saved credentials
-  Store data using JSON file handling
-  Beginner-friendly project structure
-  Simple and clean interface (CLI or Tkinter based)
>>>>>>> bc99efbceb55c2bcb0856db2773434fe58f30a0f

---


<<<<<<< HEAD
### 3️⃣ Search Credentials

- Enter website name

- Retrieves stored email and password instantly


---

## Security Notes

- Passwords are stored locally in JSON format (plain text).

#### For production-level security improvements:

- Implement AES encryption

- Add Master Password authentication

- Add password strength meter

- Implement clipboard copy feature

- Convert into executable (.exe)

- Add logging & audit trail

---


## Learning Outcomes

- This project demonstrates:

- GUI development using Tkinter

- File handling & JSON manipulation

- Exception handling

- Password generation algorithms

- Path management using pathlib

- Professional UI structuring

---


## Future Enhancements

- Master password protection

- OOP-based architecture

- Encrypted storage

- Copy to clipboard feature

- Modern UI styling (ttk theme)

- Desktop packaging using PyInstaller

---


👨‍💻 Author

Sairaj Jadhav
GitHub: https://github.com/Sairaj-25


---

