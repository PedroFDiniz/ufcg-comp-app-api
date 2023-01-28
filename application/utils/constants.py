import os
from dotenv import load_dotenv

load_dotenv()
# == DATABASE ==
PORT = os.getenv("PORT", "")
HOST = os.getenv("HOST", "")
DB_NAME = os.getenv("DB_NAME", "")
MONGO_SERVER_URI = os.getenv("MONGO_SERVER_URI", "")

# == EMAIL ==
NOREPLY_EMAIL = os.getenv("NOREPLY_EMAIL", "")
NOREPLY_EMAIL_PASSWD = os.getenv("NOREPLY_EMAIL_PASSWD", "")

SMTP_PORT = 587
SMTP_SERVER = "smtp.gmail.com"
SUBJECT = "[Computação@UFCG] Atividade complementar atribuida"
MESSAGE = """\ Uma nova atividade complementar esta disponivel para revisão."""

# == ACTIVITY ==
ACTIVITY_STATUS_CREATED = 'CREATED'
ACTIVITY_STATUS_ASSIGNED = 'ASSIGNED'
ACTIVITY_STATUS_REJECTED = 'REJECTED'
ACTIVITY_STATUS_APPROVED = 'APPROVED'

# == PROCESS ==
VOUCHERS_GENERAL_DIR = f'vouchers'