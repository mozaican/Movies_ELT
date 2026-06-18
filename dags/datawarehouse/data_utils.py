from airflow.providers.postgres.hooks.postgres import PostgresHook
from psycopg2.extras import RealDictCursor
from psycopg2 import sql


table = "movies_stats"


def get_conn_cursor():
    hook = PostgresHook(postgres_conn_id='postgres_db_yt_elt', database='elt_db')
    conn = hook.get_conn()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cursor

def close_conn_cursor(conn, cursor):
    cursor.close()
    conn.close()
 
def create_schema(schema):
    conn, cursor = get_conn_cursor()
    schema_sql = f"CREATE SCHEMA IF NOT EXISTS {schema};"
    cursor.execute(schema_sql)
    conn.commit()
    close_conn_cursor(conn, cursor)

def create_table(schema, table):
    conn, cursor = get_conn_cursor()
    try:
        query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {}.{} (
                id INT PRIMARY KEY,
                title VARCHAR(255),
                popularity FLOAT,
                vote_average FLOAT,
                release_date DATE
            );
        """).format(
            sql.Identifier(schema),
            sql.Identifier(table)
        )
        
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        print(f"Failed to create table: {e}")
        conn.rollback()
    finally:
        close_conn_cursor(conn, cursor)