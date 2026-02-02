import smtplib

my_email = "jadhavsairaj25@gmail.com"
password = "dkxcdaebzmevvhqm"


# connection = smtplib.SMTP("smtp.gmail.com", 587)

# connection.starttls()
# connection.login(user=my_email, password=password)
# connection.sendmail(
#     from_addr=my_email,   
#     to_addrs="sairaj_25@yahoo.com",
#     msg="Subject: Project 32\n\nHello, it's me"
# ) 
# connection.close()

with smtplib.SMTP("smtp.gmail.com", 587) as connection:
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(
        from_addr=my_email,
        to_addrs="sairaj_25@yahoo.com",
        msg="Subject:smtplib.SMTP using with\n\nsending a message"
    )