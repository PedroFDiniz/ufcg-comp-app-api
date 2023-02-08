import os
import random
import datetime

from application.utils.constants import VOUCHERS_GENERAL_DIR
from application.database.psql_database import get_db_connection
from werkzeug.datastructures import FileStorage


class Activity:

    @staticmethod
    def register(owner_email: str, voucher: FileStorage, workload: int, kind: str, description: str, state: str, start_date: datetime.datetime, end_date: datetime.datetime):
        try:
            user_dir = owner_email.split("@")[0]

            if not os.path.exists(f'{VOUCHERS_GENERAL_DIR}/{user_dir}'):
                os.makedirs(f'{VOUCHERS_GENERAL_DIR}/{user_dir}')

            if not os.path.exists(f'{VOUCHERS_GENERAL_DIR}/{user_dir}/{voucher.filename}'):
                voucher_path = f'{VOUCHERS_GENERAL_DIR}/{user_dir}/{voucher.filename}'
            else:
                voucher_path = f'{VOUCHERS_GENERAL_DIR}/{user_dir}/{random.randint(0, 1000)}-{voucher.filename}'

            voucher.save(voucher_path)

            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('INSERT INTO activities_submitted (owner_email, kind, workload, state, description, voucher_path, start_date, end_date)'
                        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (owner_email, kind, workload, state, description, voucher_path, start_date, end_date))

            conn.commit()
            cur.close()
            conn.close()

        except ValueError as e:
            raise (e)

    @staticmethod
    def assign(activity_id: str, reviewer_email: str, state: str):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('UPDATE activities_submitted SET reviewer_email = %s, state = %s WHERE id = %s', (reviewer_email, state, activity_id))
        conn.commit()

        cur.execute('SELECT * FROM activities_submitted WHERE id = %s', (activity_id))
        activity = cur.fetchone()

        cur.close()
        conn.close()

        return activity

    def validate(activity_id: int, state: str, computed_credits: int, justify: str):
        query = ""
        if (computed_credits != None):
            query = f" SET state = '{state}', computed_credits = {computed_credits} WHERE id = {activity_id} "
        else:
            query = f" SET state = '{state}', justify = '{justify}' WHERE id = {activity_id} "

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('UPDATE activities_submitted %s ;' % (query))
        conn.commit()

        cur.execute('SELECT * FROM activities_submitted WHERE id = %s ;', (activity_id))
        activity = cur.fetchone()

        cur.close()
        conn.close()

        return activity

    @staticmethod
    def find_all_subm_activities(page: int, size: int, sort: str, order: str):
        query = ""
        if (sort and order):
            query += f" ORDER BY {sort} {order} "

        if (page != None and size != None):
            query += f" OFFSET {int(page) * int(size)} ROWS FETCH NEXT {size} ROWS ONLY "

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM activities_submitted %s;' % (query))
        activities = cur.fetchall()
        conn.close()

        return activities

    @staticmethod
    def find_by_owner_or_state(owner_email: str, states: list, page: int, size: int, sort: str, order: str):
        query = ""
        if owner_email:
            query = f" owner_email = '{owner_email}' "
        
        if owner_email and states:
            query += " AND "

        if states:
            for i, s in enumerate(states):
                if i == 0:
                    query += f" state = '{s}' "
                else:
                    query += f" OR  state = '{s}' "

        if (sort and order):
            query += f" ORDER BY {sort} {order} "
        
        if (page != None and size != None):
            query += f" OFFSET {int(page) * int(size)} ROWS FETCH NEXT {size} ROWS ONLY "

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM activities_submitted WHERE %s ;' % (query))
        activities = cur.fetchall()
        conn.close()

        return activities

    @staticmethod
    def find_by_id(activity_id: int):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM activities_submitted WHERE id = %s;', (activity_id))
        activity = cur.fetchone()
        conn.close()

        return activity

    @staticmethod
    def count_by_owner_or_state(owner_email: str, states: list):
        query = ""
        if owner_email:
            query = f" owner_email = '{owner_email}' "
        
        if owner_email and states:
            query += " AND "

        if states:
            for i, s in enumerate(states):
                if i == 0:
                    query += f" state = '{s}' "
                else:
                    query += f" OR  state = '{s}' "

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM activities_submitted WHERE %s ;' % (query))
        activities = cur.fetchone()
        conn.close()

        return activities[0]

