import os, smtplib, jwt, datetime
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET", "")
EMAIL = os.getenv("EMAIL", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_CONFIRMATION_TIMEOUT = 86300

SMTP_PORT = 587
SMTP_SERVER = "smtp.gmail.com"

SUBJECT = "YourComp: confirme seu cadastro"
MESSAGE = """\
Bem vindo ao YourComp!
Para confirmar seu email, clique no link a seguir:
%link%
Se você não criou uma conta no YourComp, ignore este email."""

def create_email_confirmation_jwt(email):
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=EMAIL_CONFIRMATION_TIMEOUT),
        "iat": datetime.datetime.utcnow(),
        "sub": email
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm="HS256"
    )


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
