import os
from dotenv import load_dotenv

load_dotenv()
# == DATABASE ==
PORT = os.getenv("PORT", "")
HOST = os.getenv("HOST", "")
DB_NAME = os.getenv("DB_NAME", "")
MONGO_SERVER_URI = os.getenv("MONGO_SERVER_URI", "")

# == JWT ==
JWT_SECRET = os.getenv("JWT_SECRET", "")
JWT_TIMEOUT = 86400 # 1 dia
JWT_EMAIL_TIMEOUT = 86300

# == EMAIL ==
NOREPLY_EMAIL = os.getenv("NOREPLY_EMAIL", "")
NOREPLY_EMAIL_PASSWD = os.getenv("NOREPLY_EMAIL_PASSWD", "")


SMTP_PORT = 587
SMTP_SERVER = "smtp.gmail.com"
SUBJECT = "[Computação@UFCG] Atividade complementar atribuida"
MESSAGE = """\ Uma nova atividade complementar esta disponivel para revisão."""

# == ACTIVITY ==
ACTIVITY_STATUS_CREATED = 'CREATED'
ACTIVITY_STATUS_VALIDATED = 'VALIDATED'
ACTIVITY_STATUS_FINISHED = 'FINISHED'