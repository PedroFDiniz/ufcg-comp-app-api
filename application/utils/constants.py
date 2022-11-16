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
EMAIL = os.getenv("EMAIL", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")

SMTP_PORT = 587
SMTP_SERVER = "smtp.gmail.com"
SUBJECT = "YourComp: confirme seu cadastro"
MESSAGE = """\
Bem vindo ao YourComp!
Para confirmar seu email, clique no link a seguir:
%link%
Se você não criou uma conta no YourComp, ignore este email."""

# == ACTIVITY ==
ACTIVITY_STATUS_CREATED = 'CREATED'
ACTIVITY_STATUS_VALIDATED = 'VALIDATED'
ACTIVITY_STATUS_FINISHED = 'FINISHED'