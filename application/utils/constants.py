import os
from dotenv import load_dotenv

load_dotenv()
# == DATABASE ==
PORT = os.getenv("PORT", "")
HOST = os.getenv("HOST", "")
DB_NAME = os.getenv("DB_NAME", "")
DB_USERNAME = os.getenv("DB_USERNAME", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# == EMAIL ==
NOREPLY_EMAIL = os.getenv("NOREPLY_EMAIL", "")
NOREPLY_EMAIL_PASSWD = os.getenv("NOREPLY_EMAIL_PASSWD", "")

SMTP_PORT = 587
SMTP_SERVER = "smtp.gmail.com"
SUBJECT = "[Computação@UFCG] Atividade complementar atribuida"
MESSAGE = """\ Uma nova atividade complementar esta disponivel para revisão."""

# == VOUCHERS ==
VOUCHERS_GENERAL_DIR = f'vouchers'