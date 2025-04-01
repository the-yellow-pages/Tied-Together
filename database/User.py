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
        tested
        Create user table with the following columns:
        id int,
        first_name text,
        last_name text,
        username text,
        """
        q = """
        CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            username TEXT
        );
        """
        self.cursor.execute(q)
        self.connection.commit()
        
    def create_liked_vehicles_table(self):
        """
        tested
        Create liked_vehicles table with the following columns:
        id int,
        user_id int,
        vehicle_id int,
        """
        q = """
        CREATE TABLE IF NOT EXISTS liked_vehicles (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(id),
            vehicle_id INT REFERENCES vehicles(id),
            UNIQUE(user_id, vehicle_id)
        );
        """
        self.cursor.execute(q)
        self.connection.commit()
        
    def check_created_tables(self):
        """
        tested
        Check if the tables are created
        """
        self.cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = self.cursor.fetchall()
        return [table[0] for table in tables]
    
    def delete_user_table(self):
        """
        tested
        Delete user table
        """
        q = "DROP TABLE IF EXISTS users;"
        self.cursor.execute(q)
        self.connection.commit()
        
    def delete_liked_vehicles_table(self):
        """
        tested
        Delete liked_vehicles table
        """
        q = "DROP TABLE IF EXISTS liked_vehicles;"
        self.cursor.execute(q)
        self.connection.commit()

    def create_user(self, user_data):
        """
        tested
        Insert a new user into the users table.
        :param user_data: dict with keys 'id', 'first_name', 'last_name', 'username'
        """
        q = """
        INSERT INTO users (id, first_name, last_name, username)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """
        res = super().safely_execute_one_with_parameters(q, (user_data['id'], user_data['first_name'], user_data['last_name'], user_data['username']))
        return res[0]  # Return the ID of the newly created user

    def read_user(self, user_id):
        """
        tested
        Retrieve a user by ID.
        :param user_id: int
        """
        q = "SELECT * FROM users WHERE id = %s;"
        self.cursor.execute(q, (user_id,))
        return self.cursor.fetchone()

    def update_user(self, user_id, updated_data):
        """
        TODO: test
        Update user details.
        :param user_id: int
        :param updated_data: dict with keys to update (e.g., 'first_name', 'last_name', 'username')
        """
        set_clause = ", ".join([f"{key} = %s" for key in updated_data.keys()])
        q = f"UPDATE users SET {set_clause} WHERE id = %s;"
        self.cursor.execute(q, (*updated_data.values(), user_id))
        self.connection.commit()

    def delete_user(self, user_id):
        """
        TODO: test
        Delete a user by ID.
        :param user_id: int
        """
        q = "DELETE FROM users WHERE id = %s;"
        self.cursor.execute(q, (user_id,))
        self.connection.commit()

    def create_liked_vehicle(self, liked_vehicle_data):
        """
        TESTED
        Insert a new liked vehicle into the liked_vehicles table.
        :param liked_vehicle_data: dict with keys 'user_id', 'vehicle_id'
        """
        q = """
        INSERT INTO liked_vehicles (user_id, vehicle_id)
        VALUES (%s, %s)
        RETURNING id;
        """
        res = super().safely_execute_one_with_parameters(q, (liked_vehicle_data['user_id'], liked_vehicle_data['vehicle_id']))
        return res[0]  # Return the ID of the newly created liked vehicle

    def read_liked_vehicles(self, user_id):
        """
        tested
        Retrieve all liked vehicles for a user.
        :param user_id: int
        """
        q = "SELECT * FROM liked_vehicles WHERE user_id = %s;"
        self.cursor.execute(q, (user_id,))
        return self.cursor.fetchall()

    def delete_liked_vehicle(self, user_id, vehicle_id):
        """
        tested
        Delete a liked vehicle by user_id and vehicle_id.
        :param user_id: int
        :param vehicle_id: int
        """
        q = "DELETE FROM liked_vehicles WHERE user_id = %s AND vehicle_id = %s;"
        self.cursor.execute(q, (user_id, vehicle_id))
        self.connection.commit()