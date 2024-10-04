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

# == ACTIVITY GROUPS CLASSIFICATION ==
GROUP_1_ACTIVITIES = [
    'Participação em Pesquisa de Iniciação Científica ou Extensão Reconhecida Institucionalmente pela UFCG.',
    'Participação em Projeto de Pesquisa e Desenvolvimento Reconhecido Institucionalmente pela UFCG, incluindo atividades de PD&I junto à CodeX.',
    'Participação em Monitoria Reconhecida Institucionalmente pela UFCG.',
    'Realização de Estágio Não Obrigatório.',
    'Atividades profissionais na área de Ciência da Computação (válido apenas para alunos que integralizaram pelo menos 80 créditos obrigatórios).',
    'Representação Estudantil. Participação na direção do Centro Acadêmico do curso de Ciência da Computação da UFCG, participação no colegiado do Curso de Ciência da Computação ou participação na Direção do Diretório Central de Estudantes da UFCG.'
]

GROUP_2_ACTIVITIES = [
    'Participação em Evento apoiado (organizador).',
    'Participação em Evento (ouvinte).',
    'Participação em Evento (apresentador).',
    'Participação na autoria de trabalho em Evento.',
]

GROUP_3_ACTIVITIES = [
    'Colaborador / organizador em atividade de extensão (oficinas, minicursos, cursos de extensão).',
    'Ministrante em atividade de extensão (oficinas, minicursos, cursos de extensão).',
]

GROUP_4_ACTIVITIES = [
    'Outras Atividades.',
]
