from os import getenv
from dotenv import load_dotenv
import psycopg2
from psycopg2 import pool

load_dotenv()

POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
POSTGRES_DB = getenv("POSTGRES_DB")
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"


class DBBase:
    # Create a connection pool during initialization
    connection_pool = None
    
    def __init__(self):
        if DBBase.connection_pool is None:
            try:
                DBBase.connection_pool = pool.SimpleConnectionPool(
                    1, 10,  # min connections, max connections
                    user=POSTGRES_USER,
                    password=POSTGRES_PASSWORD,
                    database=POSTGRES_DB,
                    host=POSTGRES_HOST,
                    port=POSTGRES_PORT
                )
                print("Connection pool created successfully")
            except Exception as error:
                print(f"Error creating connection pool: {error}")
                raise Exception("Failed to connect to the database")
        
        # Get a connection from the pool
        self.connection = DBBase.connection_pool.getconn()
        self.cursor = self.connection.cursor()
        
    def __del__(self):
        """Clean up resources when object is destroyed"""
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection and DBBase.connection_pool:
            DBBase.connection_pool.putconn(self.connection)
        
        
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
        self.cursor.execute(q)
        output_rows = self.cursor.fetchall()

        # Extract column names
        column_names = [description[0]
                        for description in self.cursor.description]

        # Convert each row to a dictionary
        output_rows_dict = [dict(zip(column_names, row))
                            for row in output_rows]
        return output_rows_dict if output_rows_dict else None 
    
    def select_with_parameters(self, q, params):
        self.cursor.execute(q, params)
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
        
    def safely_execute_one_without_fetch(self, query, params):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            raise e
