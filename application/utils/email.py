import smtplib
from email.message import EmailMessage
from application.utils.constants import EMAIL, EMAIL_PASSWORD, SMTP_PORT, SMTP_SERVER, SUBJECT, MESSAGE

def send_confirmation_email(user_email:str, link_to_confirm_email:str):
    email_content = MESSAGE.replace("%link%", link_to_confirm_email)

    msg = EmailMessage()
    msg.set_content(email_content)
    msg['Subject'] = SUBJECT
    msg['From'] = EMAIL
    msg['To'] = user_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)
