from datetime import datetime as dt
import pandas as pd
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from collections import defaultdict

# Use environment variables for security
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("Birthday_Bot_pass")


# Get today's date
today = dt.now()
today_tuple = (today.month, today.day)

# Read CSV file into DataFrame
data = pd.read_csv("birthdays.csv")

# Create a dictionary to store multiple people with the same birthday
birthdays_dict = defaultdict(list)
for _, data_row in data.iterrows():
    birthdays_dict[(data_row["month"], data_row["day"])].append(data_row)

# Get the list of people whose birthday is today
birthday_people_today = birthdays_dict.get(today_tuple, [])

# Debugging: Print names of birthday persons
print("Today's birthdays:", [data["name"] for data in birthday_people_today])

# If there are birthdays today, send wishes
if birthday_people_today:
    for birthday_person in birthday_people_today:
        try:
            # Read quotes from file
            with open("quotes.txt", "r", encoding="utf-8") as file:
                quotes = [quote.strip() for quote in file.readlines() if quote.strip()]

            # Select a random quote and personalize it
            random_quote = random.choice(quotes)
            wish_text = random_quote.replace("[Name]", birthday_person["name"])

            print(f"Sending email to {birthday_person['name']} ({birthday_person['email']}): {wish_text}")

            # Create email message
            message = MIMEMultipart()
            message["From"] = MY_EMAIL
            message["To"] = birthday_person["email"]
            message["Subject"] = "Happy Birthday!"
            
            # Attach body text (properly encoded)
            message.attach(MIMEText(wish_text, "plain", "utf-8"))

            # Send email
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(MY_EMAIL, MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=birthday_person["email"],
                    msg=message.as_string()  # Properly formatted email
                )

            print(f"Email sent successfully to {birthday_person['name']} ({birthday_person['email']})!")

        except Exception as e:
            print(f"Failed to send email to {birthday_person['name']} ({birthday_person['email']}): {e}")

else:
    print("No birthdays today.")
