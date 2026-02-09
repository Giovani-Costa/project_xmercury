from contextlib import contextmanager
from typing import Generator

import psycopg2
from psycopg2 import OperationalError, pool
from psycopg2.extras import RealDictCursor


class PostgresDB:
    def __init__(
        self, db_name, db_user, db_password, db_host, db_port, min_conn=1, max_conn=10
    ):
        self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=min_conn,
            maxconn=max_conn,
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )

    @contextmanager
    def get_cursor(self) -> Generator[RealDictCursor, None, None]:
        connection = None
        cursor = None
        try:
            connection = self.connection_pool.getconn()
            cursor = connection.cursor(cursor_factory=RealDictCursor)

            yield cursor

            connection.commit()

        except Exception:
            if connection:
                connection.rollback()
            raise

        finally:
            if cursor:
                cursor.close()
            if connection:
                self.connection_pool.putconn(connection)

    def close_all(self):
        if self.connection_pool:
            self.connection_pool.closeall()


if __name__ == "main":
    HOST = "localhost"
    PORT = "5432"
    DB_NAME = "postgres"
    USER = "postgres"
    PASSWORD = "your_password"
