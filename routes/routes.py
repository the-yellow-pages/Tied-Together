from flask import render_template, request, jsonify
import random
from app import app
from controllers.car import CarController
from controllers.UserController import UserController
import hmac
import hashlib
import time
import os
from functools import wraps



# Initialize the car controller
car_controller = CarController()
user_controller = UserController()

def require_auth(f):
    """
    Decorator for routes that require Telegram authentication
    Validates the integrity of the data using the hash parameter
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.get_json()
        
        if not data or 'auth_object' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing required parameters"
            }), 400
        
        auth_object = data.pop('auth_object')
        received_hash = auth_object.pop('hash')
        
        app.logger.info("________Received goodswipe data______")
        app.logger.info(auth_object)
        app.logger.info("__________________________________________")
        
        
        # Create data check string by sorting alphabetically and joining with \n
        data_check_string = '\n'.join([f"{key}={value}" for key, value in sorted(auth_object.items())])
        app.logger.info(f"Data check string: {data_check_string}")
        
        # Get bot token from environment variable
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        if not bot_token:
            return jsonify({
                "status": "error",
                "message": "Bot token not configured"
            }), 500
        
        # Create secret key
        secret_key = hmac.new(
            key=b"WebAppData",
            msg=bot_token.encode(),
            digestmod=hashlib.sha256
        ).digest()
        
        # Calculate hash
        calculated_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()
        
        # Validate hash
        if calculated_hash != received_hash:
            return jsonify({
                "status": "error",
                "message": "Data integrity check failed"
            }), 401
        
        # Validate auth_date (optional: check if not older than 24 hours)
        auth_date = int(auth_object.get('auth_date', 0))
        current_time = int(time.time())
        if current_time - auth_date > 86400:  # 24 hours
            return jsonify({
                "status": "error",
                "message": "Authorization data is outdated"
            }), 401
        
        # Pass the authenticated data to the decorated function
        return f(data, *args, **kwargs)
    
    return decorated_function

@app.route('/')
def index():
    """
    Serves the index.html template
    """
    app.logger.info("Rendering index.html")
    return render_template('index.html')

@app.route('/api/goodswipe', methods=['POST'])
@require_auth
def goodswipe(data):
    """
    API endpoint for handling a positive swipe
    """
    user = data.get('user')
    vehicle_id = data.get('candidateId')
    if user and vehicle_id:
        # Add the liked vehicle to the database
        res = user_controller.add_liked_vehicle(user, vehicle_id)
        if res:
            return jsonify({
                "status": "success", 
                "message": "Positive swipe recorded",
                "data": data
            })
    return jsonify({
        "status": "error",
        "message": "Invalid data"
    }), 400

@app.route('/api/badswipe', methods=['POST'])
@require_auth
def badswipe(data):
    """
    API endpoint for handling a negative swipe
    """
    # Process the negative swipe data
    user = data.get('user')
    vehicle_id = data.get('candidateId')
    if user and vehicle_id:
        # Add the disliked vehicle to the database
        res = user_controller.add_disliked_vehicle(user, vehicle_id)
        if res:
            return jsonify({
                "status": "success", 
                "message": "Negative swipe recorded",
                "data": data
            })
    return jsonify({
        "status": "error",
        "message": "Invalid data"
    }), 400

@app.route('/api/getnextcandidate', methods=['GET'])
def getnextcandidate():
    """
    API endpoint that returns a random car from the database
    """
    car = car_controller.get_random_car()
    formatted_car = car_controller.format_car_for_frontend(car)
    
    if not formatted_car:
        return jsonify({
            "status": "error",
            "message": "No cars available"
        }), 404
    
    return jsonify({
        "status": "success",
        "candidate": formatted_car
    })

@app.route('/api/all_cars', methods=['GET'])
def all_cars():
    """
    API endpoint that returns all available car types for debugging
    """
    cars = car_controller.db.get_hundred_vehicle()
    car_count = len(cars) if cars else 0
    
    return jsonify({
        "status": "success",
        "count": car_count,
        "sample": cars[:5] if cars else []
    })
    
@app.route('/api/get_liked_vehicles', methods=['POST'])
@require_auth
def get_liked_vehicles(data):
    """
    return liked vehicles with pagination
    body: {
        "user_id": 1,
        "page": 1,
        "limit": 10
    }
    """
    user_id = data.get('user_id')
    page = data.get('page', 1)
    limit = data.get('limit', 10)
    
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "User ID is required"
        }), 400
    
    liked_vehicles = user_controller.get_liked_vehicles(user_id)
    
    if not liked_vehicles:
        return jsonify({
            "status": "success",
            "message": "No liked vehicles found",
            "data": []
        })
    
    # Pagination logic
    start = (page - 1) * limit
    end = start + limit
    paginated_vehicles = [car_controller.format_car_for_frontend(car) for car in liked_vehicles[start:end]]
    
    return jsonify({
        "status": "success",
        "liked_vehicles": paginated_vehicles,
        "total_count": len(liked_vehicles)
    })

@app.route('/api/authorize', methods=['POST'])
def authorize():
    """
    API endpoint for authorizing Telegram Mini App data
    Validates the integrity of the data using the hash parameter
    
    Expected body:
    {
        "hash": "ab12cd34...",
        "auth_date": 123456789,
        "user": "...",
        ... (other Telegram WebApp initData fields)
    }
    """
    data = request.get_json()
    app.logger.info("________Received authorization data______")
    app.logger.info(data)
    app.logger.info("__________________________________________")
    
    if not data or 'hash' not in data:
        return jsonify({
            "status": "error",
            "message": "Missing required parameters"
        }), 400
    
    received_hash = data.pop('hash')
    
    # Create data check string by sorting alphabetically and joining with \n
    data_check_string = '\n'.join([f"{key}={value}" for key, value in sorted(data.items())])
    
    # Get bot token from environment variable
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        return jsonify({
            "status": "error",
            "message": "Bot token not configured"
        }), 500
    
    # Create secret key
    secret_key = hmac.new(
        key=b"WebAppData",
        msg=bot_token.encode(),
        digestmod=hashlib.sha256
    ).digest()
    
    # Calculate hash
    calculated_hash = hmac.new(
        key=secret_key,
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()
    
    # Validate hash
    if calculated_hash != received_hash:
        return jsonify({
            "status": "error",
            "message": "Data integrity check failed"
        }), 401
    
    # Validate auth_date (optional: check if not older than 24 hours)
    auth_date = int(data.get('auth_date', 0))
    current_time = int(time.time())
    if current_time - auth_date > 86400:  # 24 hours
        return jsonify({
            "status": "error",
            "message": "Authorization data is outdated"
        }), 401
    
    # Process user data if needed
    user_data = data.get('user')
    
    return jsonify({
        "status": "success",
        "message": "Authorization successful",
        "user": user_data
    })
