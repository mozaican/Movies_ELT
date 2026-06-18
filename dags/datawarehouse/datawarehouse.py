import logging
from airflow.decorators import task
from psycopg2 import sql

from datawarehouse.data_transformation import clean_movie_data, add_features
from datawarehouse.data_utils import get_conn_cursor, close_conn_cursor, create_schema, create_table
from datawarehouse.data_modifications import insert_rows, update_rows
from datawarehouse.data_loading import load_data


logger = logging.getLogger(__name__)


@task
def transform_and_load_data(schema="movies_schema", table="movies_stats"):
    conn, cursor = get_conn_cursor()
    
    try:
        create_schema(schema)
        create_table(schema, table)

        data = load_data()

        df = clean_movie_data(data)
        df = add_features(df)
        records = df.to_dict('records')

        for row in records:
            if record_exists(cursor, schema, table, row['id']):
                update_rows(cursor, conn, schema, table, row)
            else:
                insert_rows(cursor, conn, schema, table, row)

        conn.commit()
        logger.info("Individual row updates completed successfully.")

    except Exception as e:
        conn.rollback()
        logger.error(f"Error during data transformation and loading: {e}")
        raise
    finally:
        close_conn_cursor(conn, cursor)


def record_exists(cursor, schema, table, row_id):
    query = sql.SQL("SELECT 1 FROM {}.{} WHERE id = %s").format(
        sql.Identifier(schema), sql.Identifier(table)
    )
    cursor.execute(query, (row_id,))
    return cursor.fetchone() is not None