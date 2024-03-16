import psycopg2
import mysql.connector

from helpers.data import DATABASE_TYPES
from helpers.logger import logger
from services.mysql_query_strings import MySQL_CREATE_TABLE
from services.postgres_query_strings import POSTGRES_CREATE_TABLE, POSTGRES_CHECK_TABLE_EXISTS
from store.app_context import app_context

from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from psycopg2.extensions import connection as PostgreSQLConnection
from psycopg2.extensions import cursor as PostgreSQLCursor


def create_table_if_not_exists_postgres(
        conn: PostgreSQLConnection,
        cursor: PostgreSQLCursor
):
    try:
        # Check if the table exists
        cursor.execute(POSTGRES_CHECK_TABLE_EXISTS)
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            # Create the table if it doesn't exist
            cursor.execute(
                POSTGRES_CREATE_TABLE
            )
            conn.commit()
            logger(
                "table_creation",
                "success",
                "Table created successfully in Postgres",
            )
        else:
            logger(
                "table_creation",
                "success",
                "Table already exists in Postgres",
            )

    except Exception as error:
        logger(
            "table_creation",
            "error",
            f"Error creating table in Postgres: {error}",
        )
        conn.rollback()

    finally:
        # Closing database connection.
        if conn:
            logger(
                "table_creation",
                "info",
                "Postgres connection is closed",
            )


def create_table_if_not_exists_mysql(conn: MySQLConnection, cursor: MySQLCursor):
    try:
        # Check if the table exists
        cursor.execute("SHOW TABLES LIKE 'passwords'")
        table_exists = cursor.fetchone()

        if not table_exists:
            # Create the table if it doesn't exist
            cursor.execute(
                MySQL_CREATE_TABLE
            )
            conn.commit()
            logger(
                "table_creation",
                "success",
                "Table created successfully in MySQL",
            )
        else:
            logger(
                "table_creation",
                "info",
                "Table already exists in MySQL",
            )

    except mysql.connector.Error as error:
        logger(
            "table_creation",
            "error",
            f"Error creating table in MySQL: {error}",
        )
        conn.rollback()

    finally:
        # Closing database connection.
        if conn:
            logger(
                "table_creation",
                "info",
                "MySQL connection is closed",
            )


def create_db_table() -> bool:
    db_type = app_context.get_config("db_type")
    conn = app_context.get_config("db_connection")
    cursor = app_context.get_config("db_cursor")
    try:
        if db_type == DATABASE_TYPES.get("p"):
            create_table_if_not_exists_postgres(conn, cursor)
        elif db_type == DATABASE_TYPES.get("m"):
            create_table_if_not_exists_mysql(conn, cursor)

        logger(
            "table_creation",
            "success",
            "Table created successfully in Postgres",
        )
        return True
    except Exception as e:
        logger(
            "table_creation",
            "error",
            f"Error creating table in Postgres: {e}",
        )
        return False
