from typing import Union, Tuple

from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from psycopg2.extensions import connection as PostgreSQLConnection
from psycopg2.extensions import cursor as PostgreSQLCursor

DBConnectionType = Union[
    Tuple[None, None] |
    Tuple[MySQLConnection, MySQLCursor] |
    Tuple[PostgreSQLConnection, PostgreSQLCursor]
]

CursorType = Union[MySQLCursor | PostgreSQLCursor]
ConnectionType = Union[MySQLConnection | PostgreSQLConnection]
