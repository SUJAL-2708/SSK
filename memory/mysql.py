import mysql.connector

from config.settings import (
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_DATABASE
)


class MySQLMemory:

    def __init__(self):

        self.connection = None

        self._create_database()

        self.connection = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )

        self._create_table()

    # =====================================
    # GET CONNECTION
    # =====================================

    def _get_connection(self):

        if self.connection is None:
            raise RuntimeError(
                "MySQL connection is not initialized."
            )

        return self.connection

    # =====================================
    # CREATE DATABASE
    # =====================================

    def _create_database(self):

        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )

        cursor = connection.cursor()

        try:

            cursor.execute(
                f"""
                CREATE DATABASE IF NOT EXISTS
                `{MYSQL_DATABASE}`
                """
            )

            connection.commit()

        finally:

            cursor.close()
            connection.close()

    # =====================================
    # CREATE TABLE
    # =====================================

    def _create_table(self):

        connection = self._get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (

                    memory_id VARCHAR(36) PRIMARY KEY,

                    block VARCHAR(50) NOT NULL,

                    content TEXT NOT NULL,

                    importance INT NOT NULL,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        ON UPDATE CURRENT_TIMESTAMP,

                    status VARCHAR(20) DEFAULT 'active'

                )
                """
            )

            connection.commit()

        finally:

            cursor.close()

    # =====================================
    # SAVE MEMORY
    # =====================================

    def save_memory(
        self,
        memory_id: str,
        block: str,
        content: str,
        importance: int
    ):

        connection = self._get_connection()

        cursor = connection.cursor()

        try:

            query = """
            INSERT INTO memories
            (
                memory_id,
                block,
                content,
                importance
            )
            VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (
                    memory_id,
                    block,
                    content,
                    importance
                )
            )

            connection.commit()

        finally:

            cursor.close()

    # =====================================
    # GET MEMORY
    # =====================================

    def get_memory(
        self,
        memory_id: str
    ):

        connection = self._get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        try:

            cursor.execute(
                """
                SELECT *
                FROM memories
                WHERE memory_id = %s
                """,
                (memory_id,)
            )

            result = cursor.fetchone()

            return result

        finally:

            cursor.close()

    # =====================================
    # CLOSE
    # =====================================

    def close(self):

        if self.connection is not None:

            self.connection.close()

            self.connection = None