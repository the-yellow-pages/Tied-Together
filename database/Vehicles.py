from os import getenv
from dotenv import load_dotenv
import psycopg2

load_dotenv()

POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
POSTGRES_DB = getenv("POSTGRES_DB")
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"


class VehiclesDB:
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
        self.tables = ['vehicles', 'attributes',
                'contact', 'price', 'images', 'price_history']
        
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
        
    def get_big_capacity(self, capacity=5000):
        q = f"""select * from 
            (select id as price_id, price as price_last, * from price_history ) t1
            left join (select id as vehicle_id, * from vehicles) t2
            on t1.vehicle_id=t2.vehicle_id
            left join
            (select vehicle_id, gross_amount, currency, net_amount,pricerating from price
            ) t4
            on t1.vehicle_id=t4.vehicle_id
            left join 
            (select vehicle_id, location, first_registration, power, fuel_type, mileage, transmission, cubic_capacity, body_type from attributes) t3
            on t1.vehicle_id=t3.vehicle_id
            left join (
                SELECT vehicle_id, STRING_AGG(uri::text, ',') AS image_urls
                FROM images
                GROUP BY vehicle_id
            ) t5
            on t1.vehicle_id=t5.vehicle_id
            where t4.pricerating != 'unk' and t1.post_time is not NULL
            and t1.post_time='new'
            and t2.is_sell='unk'
            and CAST(CASE WHEN REGEXP_REPLACE(t3.cubic_capacity, '[^0-9]', '', 'g') = '' THEN '0' ELSE REGEXP_REPLACE(t3.cubic_capacity, '[^0-9]', '', 'g') END AS INTEGER)>{capacity};"""
        cars = self.select(q)
        return cars
    
        