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
        query = ("insert into users_data "
                 "(user_id, user_lang, accept_tou) "
                 "values (%s, %s, %s) "
                 "on conflict (user_id) do nothing")

        self.execute_query(query, user_id, None, False, )
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
        query = "update subscriptions set is_active = %s where user_id = %s"

        self.execute_query(query, new_status, user_id)

    def get_user_status(self, user_id):
        with psycopg2.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute('select is_active from subscriptions where user_id = %s',
                               [user_id, ])
                result = cursor.fetchone()

                return result[0] if result else 0

    def get_end_sub(self, user_id):
        with psycopg2.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute('select end_date from subscriptions where user_id = %s',
                               [user_id, ])
                result = cursor.fetchone()

                return result[0] if result else 0

    def create_payment(self, user_id, plan, status):
        query = ("insert into payments "
                 "(user_id, plan, status, message_id, paid_at) "
                 "values (%s, %s, %s, %s, %s)")

        self.execute_query(query, user_id, plan, status, None, None)
        with psycopg2.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute("select id from payments where user_id = %s and status = 'pending'",
                               [user_id, ])
                return cursor.fetchone()[0]

    def set_message_id(self, payment_id, message_id):
        query = "update payment set message_id = %s where id = %s"

        self.execute_query(query, message_id, payment_id)

    def get_payment_by_id(self, id):
        with psycopg2.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute('select * from payments where id = %s',
                               [id, ])
                return cursor.fetchone()

    def update_payment_data(self, id, status, pay_time=None):
        query = "update payment set status = %s, paid_at = %s where id = %s"

        self.execute_query(query, status, pay_time, id)
        return True

    def create_new_subscription(self, user_id, plan, is_trial):
        durations = {
            '1month': '1 month',
            '3month': '3 months',
            '1year': '1 year'
        }

        interval_str = durations.get(plan, '1 month')
        query = ("insert into subscriptions "
                 "(user_id, plan, start_date, end_date, is_active, is_trial) "
                 "values (%s, %s, now(), now() + %s::interval, %s, %s) "
                 "on conflict (user_id) do nothing")

        self.execute_query(query, user_id, plan, interval_str, True, is_trial)
        return True

    def update_current_subscription(self, user_id, plan, is_trial):
        durations = {
            '1month': '1 month',
            '3month': '3 months',
            '1year': '1 year'
        }

        interval_str = durations.get(plan, '1 month')
        query = ("update subscriptions set "
                 "plan = %s, start_date = now(), end_date = now() + %s::interval, is_active = %s, is_trial = %s) "
                 "where user_id = %s")

        self.execute_query(query, plan, interval_str, True, is_trial, user_id)
        return True

    def get_user_subscription(self, user_id):
        with psycopg2.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute('select * from subscriptions where user_id = %s',
                               [user_id, ])
                return cursor.fetchone()