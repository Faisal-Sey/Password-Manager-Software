MySQL_CREATE_TABLE = """
                CREATE TABLE passwords (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    title VARCHAR(255),
                    username VARCHAR(255) DEFAULT '',
                    website VARCHAR(255) DEFAULT '',
                    password BLOB NOT NULL,
                    description TEXT,
                    is_active BOOLEAN DEFAULT TRUE,
                    is_favorite BOOLEAN DEFAULT FALSE
                );
                """
