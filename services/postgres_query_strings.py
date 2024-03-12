
POSTGRES_CHECK_TABLE_EXISTS = """
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_name = 'passwords'
            );
            """

POSTGRES_CREATE_TABLE = """
                CREATE TABLE passwords (
                    id SERIAL PRIMARY KEY,
                    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    title VARCHAR(255),
                    username VARCHAR(255) DEFAULT '',
                    website VARCHAR(255) DEFAULT '',
                    password BYTEA NOT NULL,
                    description TEXT DEFAULT '',
                    is_active BOOLEAN DEFAULT TRUE,
                    is_favorite BOOLEAN DEFAULT FALSE
                );
                """