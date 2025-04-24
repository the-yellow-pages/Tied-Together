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
            id BIGINT PRIMARY KEY,
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
            user_id BIGINT REFERENCES users(id),
            vehicle_id INT REFERENCES vehicles(id),
            UNIQUE(user_id, vehicle_id)
        );
        """
        self.cursor.execute(q)
        self.connection.commit()
    
    def create_disliked_vehicles_table(self):
        """
        tested
        Create disliked_vehicles table with the following columns:
        id int,
        user_id int,
        vehicle_id int,
        """
        q = """
        CREATE TABLE IF NOT EXISTS disliked_vehicles (
            id SERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(id),
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
        res = super().safely_execute_one_with_parameters(q, (user_data['id'], user_data.get('first_name', ''), user_data.get('last_name', ''), user_data.get('username', '')))
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
    
    def get_liked_vehicles(self, user_id, offset=None, limit=None):
        """
        Retrieve a liked vehicle by user_id and vehicle_id.
        :param user_id: int
        :param vehicle_id: int
        """
        q = f"SELECT vehicle_id FROM liked_vehicles WHERE user_id = {user_id} ORDER BY vehicle_id DESC"
        if offset is not None and limit is not None:
            q += f" LIMIT {limit} OFFSET {offset}"
        q += ';'
        self.cursor.execute(q)
        return self.cursor.fetchall()

    def read_liked_vehicles(self, all_ids: list):
        """
        tested
        Retrieve all liked vehicles for a user by joinig tables
        :param user_id: int
        :param all_ids: list of vehicle_ids [id1, id2, ...]
        return: list of liked vehicles in this format:
                   [{
                "price_id": 40830,
                "price_last": 33550.0,
                "id": 407359999,
                "vehicle_id": 407359999,
                "price": "€33,750",
                "timestamp": "2025-01-07T12:34:56.507469",
                "post_time": "new",
                "is_eye_catcher": False,
                "is_new": True,
                "num_images": 23,
                "site_id": "GERMANY",
                "short_title": "Mercedes-Benz CLA 200",
                "sub_title": "d 8G-DCT AMG Line+LED+CARPLAY+WIDESCREEN",
                "has_damage": False,
                "is_video_enabled": True,
                "ready_to_drive": True,
                "highlights": "60 Mon. Garantie mögl., Finanzierung mögl., Lieferung mögl.",
                "title": "Mercedes-Benz CLA 200 d 8G-DCT AMG Line+LED+CARPLAY+WIDESCREEN",
                "url": "https://suchen.mobile.de/auto-inserat/mercedes-benz-cla-200-d-8g-dct-amg-line-led-carplay-widescreen-elmshorn/407359999.html",
                "category": "Saloon",
                "segment": "Car",
                "is_sell": "unk",
                "gross_amount": 33550.0,
                "currency": "EUR",
                "net_amount": 28193.28,
                "pricerating": '{"rating": "REASONABLE_PRICE", "ratingLabel": "Fair price", "thresholdLabels": ["\\u20ac24,500", "\\u20ac29,000", "\\u20ac31,000", "\\u20ac34,700", "\\u20ac39,800", "\\u20ac41,600"], "vehiclePriceOffset": 74}',
                "location": "Elmshorn",
                "first_registration": "10/2021",
                "power": "110\xa0kW\xa0(150\xa0hp)",
                "fuel_type": "Diesel",
                "mileage": "84,127\xa0km",
                "transmission": "Automatic",
                "cubic_capacity": "1,950\xa0ccm",
                "body_type": "Limousine",
                "image_urls": "img1.jpg,img2.jpg,img3.jpg"
            }
        """
        # Create the correct number of placeholders for the IN clause
        placeholders = ', '.join(['%s'] * len(all_ids))
        query = f"""
            SELECT * FROM 
            (SELECT id AS price_id, price AS price_last, * FROM price_history) t1
            LEFT JOIN (SELECT id AS vehicle_id, * FROM vehicles) t2
            ON t1.vehicle_id = t2.vehicle_id
            LEFT JOIN
            (SELECT vehicle_id, gross_amount, currency, net_amount, pricerating FROM price) t4
            ON t1.vehicle_id = t4.vehicle_id
            LEFT JOIN 
            (SELECT vehicle_id, location, first_registration, power, fuel_type, mileage, transmission, cubic_capacity, body_type FROM attributes) t3
            ON t1.vehicle_id = t3.vehicle_id
            LEFT JOIN (
                SELECT vehicle_id, STRING_AGG(uri::text, ',') AS image_urls
                FROM images GROUP BY vehicle_id
            ) t5 ON t1.vehicle_id = t5.vehicle_id
            WHERE t1.vehicle_id IN ({placeholders});
        """
        self.cursor.execute(query, all_ids)
        return self.cursor.fetchall()

    def delete_liked_vehicle(self, user_id, vehicle_id):
        """
        tested
        Delete a liked vehicle by user_id and vehicle_id.
        :param user_id: int
        :param vehicle_id: int
        """
        q = "DELETE FROM liked_vehicles WHERE user_id = %s AND vehicle_id = %s;"
        return super().safely_execute_one_without_fetch(q, (user_id, vehicle_id))
        
    def create_disliked_vehicle(self, disliked_vehicle_data):
        """
        tested
        Insert a new liked vehicle into the liked_vehicles table.
        :param liked_vehicle_data: dict with keys 'user_id', 'vehicle_id'
        """
        q = """
        INSERT INTO disliked_vehicles (user_id, vehicle_id)
        VALUES (%s, %s)
        RETURNING id;
        """
        res = super().safely_execute_one_with_parameters(q, (disliked_vehicle_data['user_id'], disliked_vehicle_data['vehicle_id']))
        return res[0]  # Return the ID of the newly created liked vehicle