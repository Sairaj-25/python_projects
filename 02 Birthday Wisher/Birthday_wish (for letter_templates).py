import os
from datetime import datetime as dt
import pandas
import random
import smtplib

MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("Birthday_Bot_pass")
# create a tuple using datetime for saving todays's month and date

# today_month = dt.now().month
# today_date = dt.now().day

today = dt.now()

today_tuple = (today.month, today.day)

# Use pandas library to read csv files

data = pandas.read_csv("birthdays.csv")

# Dictionary Comprehension to create a dictionary from birthday.csv that is formated
# birthdays_dict = {
# (birthday_month, birthday_day): data_row
# }

"""
Dictionary comprehension template for pandas DataFrame looks like this:

new_dict = {new_key: new_value for (index, data_row} in data.iterrows()}

"""

# birthdays_dict = {(data_row['month'], data_row['day']): data_row for (index, data_row) in data.iterrows()}

# birthdays_dict = {
#     (data_row['month'], data_row['day']): data_row
#     for _, data_row in data.iterrows()
# }

# Create a dictionary where keys are (month, day) tuples and values are lists of rows
birthdays_dict = {}
for _, data_row in data.iterrows():
    birthday_tuple = (data_row['month'], data_row['day'])
    if birthday_tuple not in birthdays_dict:
        birthdays_dict[birthday_tuple] = []
    birthdays_dict[birthday_tuple].append(data_row)

if today_tuple in birthdays_dict:
    for person in birthdays_dict[today_tuple]:
        file_path = f"letter_templates/letter_{random.randint(1,3)}.txt"
        with open(file_path) as letter_file:
            contents = letter_file.read()
            contents = contents.replace("[NAME]", person["name"])
            print(person["name"])

            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(MY_EMAIL, MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=person['email'],
                    msg=f"Subject:Happy Birthday!\n\n{contents}"
                )
