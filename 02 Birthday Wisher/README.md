# 🎉 Birthday Wisher

A simple and fun Python project that automatically sends birthday wishes via email 🎂✉️.  
Designed to remove the hassle of remembering birthdays — just schedule it once and let the script do the rest!

---

## 🧠 Project Overview

This project reads birthdays from a data file and sends customized email wishes when the date matches.  
It uses Python’s built-in libraries and SMTP for email delivery.

✅ Works with Gmail (or any SMTP-based email provider)  
✅ Sends personalized messages based on templates  
✅ Easy to customize and extend

---

## 📦 Features

- 🎁 Reads `birthdays.csv` with names and emails  
- ✉️ Sends email wishes automatically if today matches a birthday  
- 📌 Uses multiple letter templates  
- 🛠 Easy to customize message content

---

## 📁 Project Structure

```
Birthday Wisher/
├── Birthday_Bot.py
├── birthdays.csv
├── main_secured_info.py
├── quotes.txt
├── requirements.txt
└── README.md
```

---

## 🛠 Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Core scripting language |
| `smtplib` | Sending emails |
| `datetime` | Date handling |
| CSV file | Birthday data store |
| Text templates | Email content personalization |

---

## 🚀 How It Works

1. The script reads `birthdays.csv`.  
2. It compares each birthday to the current date.  
3. If a match is found, it picks a random letter template.  
4. It customizes the message and sends an email.

---

## 📥 Setup & Installation

### Requirements

✔ Python 3.x  
✔ Internet connection  
✔ Email account (Gmail, Outlook, etc.)

### Steps

1. Clone the repository:

```bash
git clone https://github.com/Sairaj-25/python_projects.git
cd "02 Birthday Wisher"
