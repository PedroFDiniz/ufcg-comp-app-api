from application.database.psql_database import get_db_connection


class User:
    @staticmethod
    def create(name: str, email: str, role: str):

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('INSERT INTO users (name, email, role) VALUES (%s, %s, %s) ;', (name, email, role))
        conn.commit()

        cur.execute('SELECT * FROM users WHERE email = %s ;', (email, ))
        user = cur.fetchall()

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
        result = cur.fetchall()

        cur.close()
        conn.close()

        users = []
        for row in result:
            users.append({
                "email": row[0],
                "name": row[1],
                "role": row[2],
                "enroll": row[3],
                "creation_time": row[4]
            })

        return users
