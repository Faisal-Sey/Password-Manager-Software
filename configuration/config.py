import os

from configuration.db_connect import connect_to_database
from configuration.initialize_db import create_db_table
from configuration.load_env_variables import load_env_variables
from store.app_context import app_context

loading_state: str = "⌛⌛⌛"
completed_state: str = "✔✔✔"
error_state: str = "❌❌❌"


def load_configurations() -> None:
    # Load environment variables
    print(f"{loading_state} Loading environment variables...")
    load_variables = load_env_variables()
    if load_variables:
        print(f"{completed_state} Environment variables loaded...")
    else:
        print(f"{error_state} Error loading environment variables...")

    # Connect to Database
    print(f"{loading_state} Connecting to database...")
    status, conn, cursor = connect_to_database()
    app_context.set_config("db_type", os.getenv("DATABASE_TYPE"))

    if status:
        app_context.set_config("db_connection", conn)
        app_context.set_config("db_cursor", cursor)
        print(f"{completed_state} Connected to database...")

        # Create table if it doesn't exist
        print(f"{loading_state} Creating table in database...")
        create_db_table()
        print(f"{completed_state} Table created in database...")
    else:
        app_context.set_config("db_connection", None)
        app_context.set_config("db_cursor", None)
        print(f"{error_state} Error connecting to database...")



