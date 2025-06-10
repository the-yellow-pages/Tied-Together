from database.Vehicles import VehiclesDB
import random


class CarController:
    def __init__(self):
        self.db = VehiclesDB()

    async def get_random_car(self, user_id=None):
        """
        Fetch a random car from the database
        """
        cars = await self.db.get_hundred_vehicle(user_id)
        if not cars:
            return None

        return random.choice(cars)

    async def get_filtered_cars(self,
                          user_id,
                          start_price=0,
                          end_price=0,
                          start_year=0,
                          end_year=0,
                          limit=10,
                          not_fuel_type=None,
                          fuel_type=None
                          ):
        """
        Fetch cars from the database based on specific filters
        """
        cars = await self.db.new_get_filtered_cars(
            user_id, start_price, end_price, start_year, end_year, limit, not_fuel_type, fuel_type)
        if not cars:
            return None
        return [self.format_car_for_frontend(car) for car in cars]

    def format_car_for_frontend(self, car):
        """
        Format car data for frontend display
        """
        if not car:
            return None

        # Extract the first image URL from the comma-separated list
        image_urls = []
        if car.get('image_urls'):
            # Ensure all image URLs have https:// prefix
            image_urls = [
                (f"https://{image}" if not image.startswith('http') else image)
                for image in car.get('image_urls', '').split(',')
                if image.strip()  # Skip empty strings
            ]

        first_image = image_urls[0] if image_urls else None

        return {
            "id": car.get('vehicle_id'),
            "title": car.get('title'),
            "price": car.get('price_last'),
            "currency": car.get('currency', 'EUR'),
            "location": car.get('location'),
            "mileage": car.get('mileage'),
            "fuel_type": car.get('fuel_type'),
            "transmission": car.get('transmission'),
            "body_type": car.get('body_type'),
            "first_registration": car.get('first_registration'),
            "image_url": first_image,
            "all_images": image_urls,
            "source_link": car.get('url', ''),
        }
