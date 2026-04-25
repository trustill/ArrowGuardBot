import config
import psycopg2

schema_sql = open("schemas.sql", encoding="utf-8").read()

def create_schema(conn_str, sql):
    try:
        with psycopg2.connect(conn_str) as conn:
            print("Connection createed")
            with conn.cursor() as cursor:
                cursor.execute(sql)
                print("Database created")
    except psycopg2.DatabaseError as err:
        raise err

if __name__ == "__main__":
    create_schema(config.conn_str, schema_sql)