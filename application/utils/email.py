import smtplib
from email.message import EmailMessage
from application.utils.constants import NOREPLY_EMAIL, NOREPLY_EMAIL_PASSWD, SMTP_PORT, SMTP_SERVER, SUBJECT, MESSAGE

def send_noreply_email(user_email):
    email_content = MESSAGE

    msg = EmailMessage()
    msg.set_content(email_content)
    msg['Subject'] = SUBJECT
    msg['From'] = NOREPLY_EMAIL
    msg['To'] = user_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(NOREPLY_EMAIL, NOREPLY_EMAIL_PASSWD)
        server.send_message(msg)
