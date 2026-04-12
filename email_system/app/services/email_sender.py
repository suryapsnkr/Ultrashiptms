# email_sender.py
import smtplib
from email.mime.text import MIMEText
from app.services.rotation import get_smtp

def send_email(to_email, subject, content):
    smtp = get_smtp()

    msg = MIMEText(content, "html")
    msg["Subject"] = subject
    msg["From"] = smtp["user"]
    msg["To"] = to_email

    server = smtplib.SMTP(smtp["host"], 587)
    server.starttls()
    server.login(smtp["user"], smtp["pass"])
    server.send_message(msg)
    server.quit()

    return True