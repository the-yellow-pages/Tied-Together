
from os import getenv
from dotenv import load_dotenv
import psycopg2

load_dotenv()

POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
POSTGRES_DB = getenv("POSTGRES_DB")
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"


class DBBase:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                database=POSTGRES_DB,
                host=POSTGRES_HOST,
                port=POSTGRES_PORT
            )
            print("Connection to PostgreSQL DB successful")
        except Exception as error:
            print(f"Error: {error}")
            return None
        self.cursor = self.connection.cursor()
        
    def select(self, q):
        print(q)
        self.cursor.execute(q)
        output_rows = self.cursor.fetchall()

        # Extract column names
        column_names = [description[0]
                        for description in self.cursor.description]

        # Convert each row to a dictionary
        output_rows_dict = [dict(zip(column_names, row))
                            for row in output_rows]
        return output_rows_dict if output_rows_dict else None 