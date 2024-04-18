import psycopg2
from urllib.parse import urlparse

class Database:
    def __init__(self, url: str):
        """
        Initializes the DatabaseConnector with connection details.
        :param url: postgreSQL db url
        """
        result = urlparse(url)
        self.user = result.username
        self.password = result.password
        self.db_name = result.path[1:]
        self.host = result.hostname
        self.port = result.port
        self.connection = None
        self.connect()

    def connect(self):
        """
        Establishes a connection to the PostgreSQL database.
        """
        try:
            self.connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print(f"Connected to the {self.db_name} database.")
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")

    def disconnect(self):
        """
        Closes the database connection.
        """
        if self.connection:
            self.connection.close()
            print(f"Disconnected from the {self.db_name} database.")

    def execute_query(self, query, params=None):
        """
        Executes an SQL query and returns the results.
        :param query: The SQL query to execute.
        :param params: Optional parameters for the query (as a tuple).
        :return: A list of query results (if any).
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            return None

    def get_tables(self, table_schema="public"):
        """
        Gets table from given table_schema
        :param table_schema: select the schema from which the query has to be genrated (default is 'public')
        """
        return self.execute_query("""
            SELECT table_name, STRING_AGG(column_name, ', ')
            FROM information_schema.columns
            WHERE table_schema = 'public'
            GROUP BY table_name;""")

