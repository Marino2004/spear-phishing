import smtplib

sender = "Private Person <hello@demomailtrap.com>"
receiver = "A Test User <marinomiha7@gmail.com>"

message = f"""\
Subject: Hi Mailtrap
To: {receiver}
From: {sender}

This is a test e-mail message."""

with smtplib.SMTP("live.smtp.mailtrap.io", 587) as server:
    server.starttls()
    server.login("api", "<YOUR_API_TOKEN>")
    server.sendmail(sender, receiver, message)