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
        
        
    def make_dict(self, row: tuple):
        if not row or not len(row):
            return None
        column_names = [description[0]
                        for description in self.cursor.description]
        return {column_names[i]: row[i] for i in range(len(row))}
    
    def make_dicts(self, rows: list):
        if not rows or not len(rows):
            return None
        column_names = [description[0]
                        for description in self.cursor.description]
        return [{column_names[i]: row[i] for i in range(len(row))} for row in rows]
    
        
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
    
    def safely_execute_one_with_parameters(self, query, params):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.fetchone()
        except Exception as e:
            self.connection.rollback()
            raise e
