import os
from dotenv import load_dotenv

load_dotenv()

# == AUTH ==
AUTH_COORDINATOR_EMAIL = os.getenv("AUTH_COORDINATOR_EMAIL", "")
AUTH_REVIEWER_DOMAIN = os.getenv("AUTH_REVIEWER_DOMAIN", "")
AUTH_STUDENT_DOMAIN = os.getenv("AUTH_STUDENT_DOMAIN", "")

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

# == VOUCHERS ==
VOUCHERS_GENERAL_DIR = f'vouchers'

# == POOLED ACTIVITY CLASSIFICATION ==
TYPE_1_ACTIVITIES = [
    'Participação em Evento apoiado (organizador).',
    'Participação em Evento (ouvinte).',
    'Participação em Evento (apresentador).',
    'Participação na autoria de trabalho em Evento.',
]

TYPE_2_ACTIVITIES = [
    'Colaborador / organizador em atividade de extensão (oficinas, minicursos, cursos de extensão).',
    'Ministrante em atividade de extensão (oficinas, minicursos, cursos de extensão).',
]

TYPE_3_ACTIVITIES = [
    'Outras Atividades.',
]

CREDIT_POOL_ACTIVITIES: list[str] = TYPE_1_ACTIVITIES + TYPE_2_ACTIVITIES + TYPE_3_ACTIVITIES
TYPE_1_MAX = 16
TYPE_2_MAX = 16
TYPE_3_MAX = 8