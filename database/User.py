
from database.DBBase import DBBase


class UsersDB(DBBase):  # Inherit from DBBase
    def __init__(self):
        super().__init__()  # Call the parent class constructor
        self.tables = ['vehicles', 'attributes',
                       'contact', 'price', 'images', 'price_history']
        
    def select(self, q):
        return super().select(q)  # Use the parent class's select method
    
    def create_user_table(self):
        """
        Create user table with the following columns:
        id int,
        first_name text,
        last_name text,
        username text,
        """
        q = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            username TEXT
        );
        """
        self.cursor.execute(q)
        self.connection.commit()
        
    def create_liked_vehicles_table(self):
        """
        Create liked_vehicles table with the following columns:
        id int,
        user_id int,
        vehicle_id int,
        """
        q = """
        CREATE TABLE IF NOT EXISTS liked_vehicles (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(id),
            vehicle_id INT
        );
        """
        self.cursor.execute(q)
        self.connection.commit()
        
    def check_created_tables(self):
        """
        Check if the tables are created
        """
        self.cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = self.cursor.fetchall()
        return [table[0] for table in tables]