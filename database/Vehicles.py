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
    
    
    def get_hundred_vehicle(self):
        """
        Return list of 100 dicts in such fromat:
        [
            {
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
        ]
        """
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
            where t3.body_type != 'Van'
            and t4.pricerating != 'unk'
            and t1.post_time is not NULL
            and t2.is_sell='unk'
            limit 100;"""
        cars = self.select(q)
        return cars
    
        