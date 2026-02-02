from tkinter import *
from tkinter import messagebox

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# ---------------------------- SAVE PASSWORD ------------------------------- #
import os

# Specify the folder and file name
folder_path = r"D:\python code Udemy\python\password_manager"
file_name = "data.txt"

# Ensure the folder exists
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Full file path
file_path = os.path.join(folder_path, file_name)

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website)==0 or len(password)==0:
        messagebox.showerror(title="Oops!", message="Please make sure website or password is not empty!")
    else:
        is_ok = messagebox.askokcancel(title="Title", message=f"Details entered: \nEmail: {email}"
                            f"\npassword: {password} \nDo You want to save?")
        
        if is_ok:
            with open(file_path,"a") as data_file:
                data_file.write(f"{website} | {email} | {password}\n")
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file=r"D:\python code Udemy\python\password_manager\logo.png")
canvas.create_image(100, 100, image=logo_img)
# canvas.pack()
canvas.grid(row=0,column=1)


# Website labels
website_label = Label(text="Website:")
website_label.grid(row=1,column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2,column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)


# Entries

website_entry=Entry(width=35)
website_entry.grid(row=1,column=1, columnspan=2)
website_entry.focus()

email_entry=Entry(width=35)
email_entry.grid(row=2,column=1, columnspan=2)
email_entry.insert(0, "Sairaj@gmail.com")

password_entry=Entry(width=17)
password_entry.grid(row=3, column=1)

# Buttons
genrate_password_button = Button(text="Generate Password")
genrate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=30, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()