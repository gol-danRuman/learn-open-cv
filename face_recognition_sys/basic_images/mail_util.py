import mailtrap as mt
MAILTRAP_API_TOKEN = 'c174272794d49530a715f99b35e0557a'
# create mail object
import smtplib

sender = "Private Person <ruman@fusemachines.com>"
receiver = "A Test User <rumancha12@gmail.com>"

message = f"""\
Subject: Hi Mailtrap
To: {receiver}
From: {sender}

This is a test e-mail message."""

with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
    server.login("7bd3ba2afda7bb", "89b6b89f6093ef")
    server.sendmail(sender, receiver, message)