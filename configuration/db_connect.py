import os
from typing import Tuple

import MySQLdb
import psycopg2

from helpers.logger import logger

from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from psycopg2.extensions import connection as PostgreSQLConnection
from psycopg2.extensions import cursor as PostgreSQLCursor

from typings.configuration_types import DBConnectionType


def connect_to_mysql_db(
    db_host: str,
    db_user: str,
    db_password: str,
    db_name: str
):
    # Connect to MySQL
    try:
        mysql_conn: MySQLConnection = MySQLdb.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
        )

        mysql_cursor: MySQLCursor = mysql_conn.cursor()

        return True, mysql_cursor, mysql_conn
    except Exception as e:
        logger(
            "db_connect",
            "error",
            f"Error connecting to MySQL: {e}",
        )

        return False, None, None


def connect_to_postgresql_db(
    db_host: str,
    db_user: str,
    db_password: str,
    db_name: str
):
    # Connect to PostgresSQL
    try:
        postgresql_conn: PostgreSQLConnection = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
        )

        postgresql_cursor: PostgreSQLCursor = postgresql_conn.cursor()

        return True, postgresql_cursor, postgresql_conn
    except Exception as e:
        logger(
            "db_connect",
            "error",
            f"Error connecting to PostgresSQL: {e}",
        )

        return False, None, None


def connect_to_database() -> DBConnectionType:
    # Environment variables
    db_host: str = os.getenv("DATABASE_HOST")
    db_user: str = os.getenv("DATABASE_USER")
    db_password: str = os.getenv("DATABASE_PASSWORD")
    db_name: str = os.getenv("DATABASE_NAME")
    db_type: str = os.getenv("DATABASE_TYPE")

    if db_type == "mysql":
        status, cursor, conn = connect_to_mysql_db(
            db_host,
            db_user,
            db_password,
            db_name,
        )
    else:
        status, cursor, conn = connect_to_postgresql_db(
            db_host,
            db_user,
            db_password,
            db_name,
        )

    return status, conn, cursor
