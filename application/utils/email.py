import smtplib
from email.message import EmailMessage
from application.utils.constants import NOREPLY_EMAIL, NOREPLY_EMAIL_PASSWD, SMTP_PORT, SMTP_SERVER

def send_noreply_email_assign(user_email: str):
    SUBJECT = "[Computação@UFCG] Atividade complementar atribuida"
    MESSAGE = """\ Uma nova atividade complementar esta disponivel para revisão."""
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


def send_noreply_email_validate(user_email: str, description: str, reviewer: str):
    SUBJECT = "[Computação@UFCG] Atividade complementar validada"
    MESSAGE = f"""\ A atividade complementar '{description}' foi validada por {reviewer}."""

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
