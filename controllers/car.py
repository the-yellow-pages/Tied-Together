from database.Vehicles import VehiclesDB
import random

class CarController:
    def __init__(self):
        self.db = VehiclesDB()
        
    def get_random_car(self, user_id=None):
        """
        Fetch a random car from the database
        """
        cars = self.db.get_hundred_vehicle(user_id)
        if not cars:
            return None
        
        return random.choice(cars)
    
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
