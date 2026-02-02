import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# It's better to use environment variables to store sensitive information
# to store the environment variable in windows search bar type"edit the system environment variables"
my_email = os.getenv("MY_EMAIL")
password = os.getenv("Birthday_Bot_pass")

print(my_email, password)
# Create the email content
to_email = "sairaj_25@yahoo.com"
subject = "Test Email"
body = "Hello"

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = my_email
message["To"] = to_email
message["Subject"] = subject

# Add body to email
message.attach(MIMEText(body, "plain"))

try:
    # Connect to the SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()  # Secure the connection
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=to_email, msg=message.as_string())
    print("Email sent successfully")
except Exception as e:
    print(f"Error: {e}")
