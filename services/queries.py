# CREATE operation
from typing import Dict, Any, List, Tuple

import psycopg2

from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from psycopg2.extensions import connection as pq_connection
from psycopg2.extensions import cursor as pq_cursor

from store.app_context import app_context

db_type = app_context.get_config("db_type")
is_new_table = db_type == "postgresql"


def create_data(
        cursor: pq_cursor | MySQLCursor,
        conn: pq_connection | MySQLConnection,
        table_name: str,
        data: Dict[str, Any],
        response: str = ""
) -> None:
    columns: List[str] = list(data.keys())
    values: List[str] = [data[col] for col in columns]
    returning_values: str = f"RETURNING {response}" if response else ""
    query: str = 'INSERT INTO "{}" ({}) VALUES ({}) {}'.format(
        table_name, ", ".join(columns), ", ".join(["%s"] * len(columns)), returning_values
    )
    cursor.execute(query, values)
    conn.commit()


def create_data_with_response(
        cursor: pq_cursor | MySQLCursor,
        conn: pq_connection | MySQLConnection,
        table_name: str,
        data: Dict[str, Any],
        response: str = ""
) -> int:
    columns: List[str] = list(data.keys())
    values: List[str] = [data[col] for col in columns]
    returning_values: str = f"RETURNING {response}" if response else ""
    query: str = 'INSERT INTO "{}" ({}) VALUES ({}) {}'.format(
        table_name, ", ".join(columns), ", ".join(["%s"] * len(columns)), returning_values
    )
    try:
        cursor.execute(query, values)
        conn.commit()
        return cursor.fetchone()[0]
    except psycopg2.IntegrityError:
        conn.rollback()


# READ operation
def read_data(
    cursor: pq_cursor | MySQLCursor,
    table_name: str,
    data_id: int,
    response: str = "*",
    query_filter: str = "id=%s",
) -> Tuple | None:
    _: str = '"' if is_new_table else ""
    try:
        cursor.execute(
            f"SELECT {response} FROM {_}{table_name}{_} WHERE {query_filter}", (data_id,)
        )
        result: Tuple | None = cursor.fetchone()
        return result
    except psycopg2.IntegrityError:
        pass


# READ ALL operation
def read_all_data(
        cursor: pq_cursor | MySQLCursor,
        table_name: str,
        response: str = "*",
        order_by: str = ""
) -> List[Tuple]:
    _: str = '"' if is_new_table else ""
    order_statement: str = order_by if order_by else ""
    query: str = f"SELECT {response} FROM {_}{table_name}{_} {order_statement}"
    cursor.execute(query)
    result = cursor.fetchall()
    return result


# READ ALL operation with filter
def read_all_data_with_filter(
    cursor: pq_cursor | MySQLCursor,
    table_name: str,
    data_id: Tuple,
    response: str = "*",
    filter_statement: str = "id_mit=%s",
    multiple_filters: bool = False,
    order_by: str = "",
) -> List[Tuple]:
    _: str = '"' if is_new_table else ""
    data_tuple: Tuple = (*data_id,) if multiple_filters else (data_id,)
    order_statement: str = order_by if order_by else ""
    query: str = f"SELECT {response} FROM {_}{table_name}{_} WHERE {filter_statement} {order_statement}"
    cursor.execute(query, data_tuple)
    result = cursor.fetchall()
    return result


# UPDATE operation
def update_data(
        cursor: pq_cursor | MySQLCursor,
        conn: pq_connection | MySQLConnection,
        table_name: str,
        data_id: str | int,
        new_data: Dict[str, Any],
        filter_statement: str = "id = %s"
):
    columns = ", ".join([f"{col} = %s" for col in new_data.keys()])
    values = tuple(new_data.values()) + (data_id,)

    query = f'UPDATE "{table_name}" SET {columns} WHERE {filter_statement}'

    try:
        cursor.execute(query, values)
        conn.commit()
    except Exception:
        conn.rollback()


# DELETE operation
def delete_data(
        cursor: pq_cursor | MySQLCursor,
        conn: pq_connection | MySQLConnection,
        table_name: str,
        data_id: str | int,
        filter_statement: str = "id = %s"
) -> None:
    cursor.execute(f"DELETE FROM {table_name} WHERE {filter_statement}", (data_id,))
    conn.commit()


# GET NEXT ID operation
def get_next_id(
        cursor: pq_cursor | MySQLCursor,
        table_name: str,
) -> int:
    _: str = '"' if is_new_table else ""
    cursor.execute(f"SELECT MAX(id) FROM {_}{table_name}{_}")
    result: Tuple = cursor.fetchone()
    return result[0] + 1 if result[0] else 1
