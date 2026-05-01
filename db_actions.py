import config
import psycopg2

class SqlQuery:
    def __init__(self, conn_str):
        self.conn_str = conn_str

    def execute_query(self, sql, *params):
        try:
            with psycopg2.connect(self.conn_str) as conn:
                with conn.cursor() as cursor:
                    if params:
                        cursor.execute(sql, params)
                    else:
                        cursor.execute(sql)
                    conn.commit()
        except psycopg2.DatabaseError as err:
            raise err

    def fetch_rows(self, sql, *params):
        try:
            with psycopg2.connect(self.conn_str) as conn:
                with conn.cursor() as cursor:
                    if params:
                        cursor.execute(sql, params)
                    else:
                        cursor.execute(sql)
                return cursor.fetchall()
        except psycopg2.DatabaseError as err:
            raise err

    def fetch_one_row(self, sql, *params):
        try:
            with psycopg2.connect(self.conn_str) as conn:
                with conn.cursor() as cursor:
                    if params:
                        cursor.execute(sql, params)
                    else:
                        cursor.execute(sql)
                return cursor.fetchone()
        except psycopg2.DatabaseError as err:
            raise err

    def get_user(self, user_id):
        with psycopg2.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute('select * from users_data where user_id = %s',
                             [user_id, ])

                return cursor.fetchone()

    def add_new_user(self, user_id):
        query = ("insert into users_data"
                 "(user_id, user_lang, user_status, is_trial, accept_tou, end_sub) "
                 "values (%s, %s, %s, %s, %s, %s)"
                 "on conflict (user_id) do nothing")

        self.execute_query(query, user_id, None, 0, False, False, None)
        return True

    def get_user_lang(self, user_id):
        with psycopg2.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute('select user_lang from users_data where user_id = %s',
                               [user_id, ])

                return cursor.fetchone()[0]

    def is_accept_tou(self, user_id):
        with psycopg2.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute('select accept_tou from users_data where user_id = %s',
                             [user_id, ])

                return cursor.fetchone()[0]
    def change_tou_status(self, tou_status=False, user_id=None):
        query = "update users_data set accept_tou = %s where user_id = %s"

        self.execute_query(query, tou_status, user_id)

    def change_user_lang(self, user_id, lang):
        query = "update users_data set user_lang = %s where user_id = %s"

        self.execute_query(query, lang, user_id)

    def change_user_status(self, user_id, new_status):
        query = "update users_data set user_status = %s where user_id = %s"

        self.execute_query(query, new_status, user_id)

    def get_user_status(self, user_id):
        with psycopg2.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute('select user_status from users_data where user_id = %s',
                               [user_id, ])

                return cursor.fetchone()[0]

    def get_end_sub(self, user_id):
        with psycopg2.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute('select end_sub from users_data where user_id = %s',
                               [user_id, ])

                return cursor.fetchone()[0]