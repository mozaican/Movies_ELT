import logging
from psycopg2 import sql


logger = logging.getLogger(__name__)


def insert_rows(cursor, conn, schema, table, row):
    try:
        query = sql.SQL("INSERT INTO {}.{} (id, title, popularity, vote_average, release_date) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;").format(
            sql.Identifier(schema),
            sql.Identifier(table)
        )
        
        cursor.execute(query, (
            row['id'], row['title'], row['popularity'], row['vote_average'], row['release_date']
        ))
        conn.commit()
    except Exception as e:
        logger.error(f"Failed to insert row: {e}")
        conn.rollback()
        raise


def update_rows(cursor, conn, schema, table, row):
    try:
        query = sql.SQL("UPDATE {}.{} SET title = %s, popularity = %s, vote_average = %s, release_date = %s WHERE id = %s;").format(
            sql.Identifier(schema),
            sql.Identifier(table)
        )
        cursor.execute(query, (
            row['title'], row['popularity'], row['vote_average'], row['release_date'], row['id']
        ))
        conn.commit()
    except Exception as e:
        logger.error(f"Failed to update row: {e}")
        conn.rollback()
        raise


def delete_rows(cursor, conn, schema, table, row_id):
    try:
        query = sql.SQL("DELETE FROM {}.{} WHERE id = %s;").format(
            sql.Identifier(schema),
            sql.Identifier(table)
        )
        cursor.execute(query, (row_id,))
        conn.commit()
    except Exception as e:
        logger.error(f"Failed to delete row: {e}")
        conn.rollback()
        raise
