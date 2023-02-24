from application.database.psql_database import get_db_connection


class User:
    @staticmethod
    def create(name: str, email: str, role: str, picture: str = None):

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('INSERT INTO users (name, email, role, picture) VALUES (%s, %s, %s, %s) ;', (name, email, role, picture))
        conn.commit()

        cur.execute('SELECT * FROM users WHERE email = %s ;', (email, ))
        user = cur.fetchone()

        cur.close()
        conn.close()
        return user

    @staticmethod
    def find_by_email(email: str):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM users WHERE email = %s ;', (email, ))
        user = cur.fetchone()

        cur.close()
        conn.close()
        return user

    @staticmethod
    def find_by_role(role: str):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM users WHERE role = %s ;', (role, ))
        users = cur.fetchall()

        cur.close()
        conn.close()

        return users

    @staticmethod
    def update_enroll(email: str, enroll: int):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('UPDATE users SET enroll = %s WHERE email = %s ;', (enroll, email))
        conn.commit()

        cur.execute('SELECT * FROM users WHERE email = %s ;', (email, ))
        user = cur.fetchone()

        cur.close()
        conn.close()
        return user