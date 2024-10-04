import psycopg2
from application.utils.constants import HOST, DB_NAME, DB_USERNAME, DB_PASSWORD

DB_ENUM_U_ROLE_STUDENT = 'STUDENT'
DB_ENUM_U_ROLE_COORDINATOR = 'COORDINATOR'
DB_ENUM_U_ROLE_REVIEWER = 'REVIEWER'

DB_ENUM_A_STATE_CREATED = 'CREATED'
DB_ENUM_A_STATE_ASSIGNED = 'ASSIGNED'
DB_ENUM_A_STATE_REJECTED = 'REJECTED'
DB_ENUM_A_STATE_APPROVED = 'APPROVED'

DB_ENUM_A_METRICS = [
    {'kind': 'Participação em Pesquisa de Iniciação Científica ou Extensão Reconhecida Institucionalmente pela UFCG.',
     'credits_limit': 18,
     'workload_unity': 'ano(s)',
     },
    {'kind': 'Participação em Projeto de Pesquisa e Desenvolvimento Reconhecido Institucionalmente pela UFCG, incluindo atividades de PD&I junto à CodeX.',
     'credits_limit': 16,
     'workload_unity': 'meses',
     },
    {'kind': 'Participação em Monitoria Reconhecida Institucionalmente pela UFCG.',
     'credits_limit': 16,
     'workload_unity': 'semestre(s)',
     },
    {'kind': 'Realização de Estágio Não Obrigatório.',
     'credits_limit': 18,
     'workload_unity': 'hora(s)',
     },
    {'kind': 'Atividades profissionais na área de Ciência da Computação (válido apenas para alunos que integralizaram pelo menos 80 créditos obrigatórios).',
     'credits_limit': 16,
     'workload_unity': 'hora(s)',
     },
    {'kind': 'Representação Estudantil. Participação na direção do Centro Acadêmico do curso de Ciência da Computação da UFCG, participação no colegiado do Curso de Ciência da Computação ou participação na Direção do Diretório Central de Estudantes da UFCG.',
     'credits_limit': 2,
     'workload_unity': 'ano(s)',
     },
    {'kind': 'Participação na autoria de trabalho em Evento.',
     'credits_limit': 16,
     'workload_unity': '-',
     'hours_per_credit': 30
     },
    {'kind': 'Participação em Evento (apresentador).',
     'credits_limit': 16,
     'workload_unity': '-',
     'hours_per_credit': 30
     },
    {'kind': 'Participação em Evento (ouvinte).',
     'credits_limit': 16,
     'workload_unity': '-',
     'hours_per_credit': 30
     },
    {'kind': 'Participação em Evento apoiado (organizador).',
     'credits_limit': 16,
     'workload_unity': '-',
     'hours_per_credit': 30
     },
    {'kind': 'Ministrante em atividade de extensão (oficinas, minicursos, cursos de extensão).',
     'credits_limit': 16,
     'workload_unity': '-',
     'hours_per_credit': 30
     },
    {'kind': 'Colaborador / organizador em atividade de extensão (oficinas, minicursos, cursos de extensão).',
     'credits_limit': 16,
     'workload_unity': '-',
     'hours_per_credit': 30
     },
    {'kind': 'Outras Atividades.',
     'credits_limit': 8,
     'workload_unity': '-',
     'hours_per_credit': 60
     }
]

def get_db_connection():
    conn = psycopg2.connect(
        host=HOST,
        database=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASSWORD)

    return conn


def init_database():
    conn = get_db_connection()

    # Open a cursor to perform database operations
    cur = conn.cursor()

    cur.execute(" DO $$ "
                " BEGIN "
                " IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'role_enum') THEN "
                f" CREATE TYPE role_enum AS ENUM ( '{DB_ENUM_U_ROLE_STUDENT}', '{DB_ENUM_U_ROLE_COORDINATOR}', '{DB_ENUM_U_ROLE_REVIEWER}'); "
                " END IF; "
                " END$$; "
                )

    cur.execute(" DO $$ "
                " BEGIN "
                " IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'state_enum') THEN "
                " CREATE TYPE state_enum AS ENUM "
                f" ( '{DB_ENUM_A_STATE_CREATED}', '{DB_ENUM_A_STATE_ASSIGNED}', '{DB_ENUM_A_STATE_REJECTED}', '{DB_ENUM_A_STATE_APPROVED}');"
                " END IF; "
                " END$$; "
                )

    cur.execute(" CREATE TABLE IF NOT EXISTS users (email varchar (100) PRIMARY KEY, "
                " name varchar (100) NOT NULL, "
                " role role_enum NOT NULL, "
                " enroll integer, "
                " picture varchar (255), "
                " creation_time timestamp default current_timestamp ); "
                )

    cur.execute(" CREATE TABLE IF NOT EXISTS activities_metrics (kind varchar (255) PRIMARY KEY, "
                " credits_limit integer NOT NULL, "
                " workload_unity varchar (20)); "
                )

    cur.execute(" CREATE TABLE IF NOT EXISTS activities_submitted (id serial PRIMARY KEY, "
                " owner_email varchar (100) NOT NULL, "
                " reviewer_email varchar (100), "
                " kind varchar (255) NOT NULL, "
                " workload integer, "
                " start_date date, "
                " end_date date, "
                " state state_enum NOT NULL, "
                " description varchar (255) NOT NULL, "
                " voucher_path varchar (150) NOT NULL, "
                " computed_credits integer, "
                " justify varchar (255), "
                " group integer NOT NULL, "
                " creation_time timestamp default current_timestamp, "
                " updated_time timestamp, "
                " CONSTRAINT fk_kind FOREIGN KEY (kind) REFERENCES activities_metrics (kind), "
                " CONSTRAINT fk_owner_email FOREIGN KEY (owner_email) REFERENCES users (email), "
                " CONSTRAINT fk_reviewer_email FOREIGN KEY (reviewer_email) REFERENCES users (email)); "
                )

    cur.execute(" CREATE TABLE IF NOT EXISTS process (owner_email varchar (100) PRIMARY KEY, "
                " checksum varchar (100) NOT NULL, "
                " path varchar (255) NOT NULL, "
                " creation_time timestamp default current_timestamp, "
                " CONSTRAINT fk_owner_email FOREIGN KEY (owner_email) REFERENCES users (email)); "
                )

    cur.execute(" CREATE OR REPLACE FUNCTION update_updated_time() "
                " RETURNS TRIGGER AS $$ "
                " BEGIN "
                " NEW.updated_time = now(); "
                " RETURN NEW; "
                " END; "
                " $$ LANGUAGE plpgsql; "
                )

    cur.execute(
        " DROP TRIGGER IF EXISTS update_activities_submitted_updated_time ON activities_submitted; ")

    cur.execute(" CREATE TRIGGER update_activities_submitted_updated_time "
                " BEFORE INSERT OR UPDATE ON activities_submitted "
                " FOR EACH ROW EXECUTE PROCEDURE update_updated_time(); "
                )

    conn.commit()

    cur.close()
    conn.close()


def fill_activities_metrics():
    conn = get_db_connection()

    cur = conn.cursor()

    for metric in DB_ENUM_A_METRICS:
        try:
            if 'hours_per_credit' in metric:
                cur.execute(" INSERT INTO activities_metrics (kind, credits_limit) "
                        " VALUES (%s, %s, %s) "
                        " ON CONFLICT DO NOTHING; ",
                        (metric['kind'], metric['credits_limit'], metric['hours_per_credit']))
            else:
                cur.execute(" INSERT INTO activities_metrics (kind, credits_limit, workload_unity) "
                            " VALUES (%s, %s, %s) "
                            " ON CONFLICT DO NOTHING; ",
                            (metric['kind'], metric['credits_limit'], metric['workload_unity']))
        except KeyError:
            pass

    conn.commit()

    cur.close()
    conn.close()
