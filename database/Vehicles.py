import json
from database.DBBase import DBBase


class VehiclesDB(DBBase):  # Inherit from DBBase
    def __init__(self):
        super().__init__()  # Call the parent class constructor
        self.tables = ['vehicles', 'attributes',
                       'contact', 'price', 'images', 'price_history']
        
    def select(self, q):
        return super().select(q)  # Use the parent class's select method
    
    def _user_filter(self, user_id):
        """
        Exclude vehicles that the user has already liked or disliked
        """
        return f"""
            and t1.vehicle_id NOT IN (
                SELECT vehicle_id FROM liked_vehicles WHERE user_id = {user_id}
                UNION
                SELECT vehicle_id FROM disliked_vehicles WHERE user_id = {user_id}
            )
        """
        
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
    
    def get_filtered_cars(self, user_id=None, start_price=0, end_price=0, start_year=0, end_year=0, limit=0, not_fuel_type=None, fuel_type=None):
        """
        Retrieves cars with specific price and year conditions from the database.
        Args:
            mobile_db: Database connection object (either Mobile or MobilePostgres)
            start_price: Minimum price of the car
            end_price: Maximum price of the car
            start_year: Minimum year of manufacture
            end_year: Maximum year of manufacture
            not_fuel_type: Fuel type to exclude from the results
            fuel_type: Fuel type to include in the results
        """
        q = f"""select * from 
            (select id as price_id, price as price_last, * from price_history ) t1
            left join (select id as vehicle_id, * from vehicles) t2
            on t1.vehicle_id=t2.vehicle_id
            left join 
            (select vehicle_id, location, first_registration, power, fuel_type, mileage, transmission, cubic_capacity, body_type from attributes) t3
            on t1.vehicle_id=t3.vehicle_id
            left join
            (select vehicle_id, gross_amount, currency, net_amount,pricerating from price
            ) t4
            on t1.vehicle_id=t4.vehicle_id
            left join (
                SELECT vehicle_id, STRING_AGG(uri, ',') AS image_urls
                FROM images
                GROUP BY vehicle_id
            ) t5
            on t1.vehicle_id=t5.vehicle_id
            where t1.post_time='new'
            and t3.body_type != 'Van'
            and t3.body_type != 'OtherCar'
            and t2.is_sell='unk'
            and t3.first_registration != ''
        """
        if not_fuel_type is not None:
            q += f" and t3.fuel_type != '{not_fuel_type}'"
        if fuel_type is not None:
            q += f" and t3.fuel_type = '{fuel_type}'"
        if user_id is not None:
            q += self._user_filter(user_id)
        if start_year > 0:
            q += f" and CAST(SUBSTRING(t3.first_registration, position('/' in t3.first_registration)+1, 4) AS INTEGER) >= {start_year}"
        if end_year > 0:
            q += f" and CAST(SUBSTRING(t3.first_registration, position('/' in t3.first_registration)+1, 4) AS INTEGER) <= {end_year}"
        if end_price > 0:
            q += f" and t4.gross_amount <= {end_price}"
        if start_price > 0:
            q += f" and t4.gross_amount >= {start_price}"
        if limit > 0:
            q  += f" limit {limit}"
        else:
            q  += " limit 100"
        
        
        q += ";"
        cars = self.select(q)
        return cars
    
    
    def get_hundred_vehicle(self, user_id=None):
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
        # Base query without user filtering
        base_query = """select * from 
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
            and t3.body_type != 'OtherCar'
            and t4.pricerating != 'unk'
            and t1.post_time is not NULL
            and t2.is_sell='unk'"""
            
        # Add user-specific filtering if a user_id is not None
        if user_id is not None:
            q = base_query + self._user_filter(user_id) + " limit 100;"
        else:
            # Query without user filtering
            q = base_query + " limit 100;"
        cars = self.select(q)
            
        return cars

