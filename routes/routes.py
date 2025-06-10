from quart import render_template, request, jsonify, current_app
import random
from app import app
import hmac
import hashlib
import time
import os
from functools import wraps



# Initialize the car controller

def require_auth(f):
    """
    Decorator for routes that require Telegram authentication
    Validates the integrity of the data using the hash parameter
    """
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        data = await request.get_json()
        
        if not data or 'auth_object' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing required parameters"
            }), 400
        
        auth_object = data.pop('auth_object')
        received_hash = auth_object.pop('hash')
        data_check_list = [f"{key}={value}" for key, value in auth_object.items()]
        data_check_list.sort()
        data_check_string = '\n'.join(data_check_list)
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
        
        calculated_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode(), # Use the alphabetically sorted string
            digestmod=hashlib.sha256
        ).hexdigest() # Use hexdigest() to get a hex string
        
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
        return await f(data, *args, **kwargs)
    
    return decorated_function

@app.route('/')
async def index():
    """
    Serves the index.html template
    """
    app.logger.info("Rendering index.html")
    return await render_template('index.html')

@app.route('/api/goodswipe', methods=['POST'])
@require_auth
async def goodswipe(data):
    """
    API endpoint for handling a positive swipe
    """
    user = data.get('user')
    vehicle_id = data.get('candidateId')
    if user and vehicle_id:
        # Add the liked vehicle to the database
        res = await current_app.user_controller.add_liked_vehicle(user, vehicle_id)
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
async def badswipe(data):
    """
    API endpoint for handling a negative swipe
    """
    # Process the negative swipe data
    user = data.get('user')
    vehicle_id = data.get('candidateId')
    if user and vehicle_id:
        # Add the disliked vehicle to the database
        res = await current_app.user_controller.add_disliked_vehicle(user, vehicle_id)
        if res:
            return jsonify({
                "status": "success", 
                "message": "Negative swipe recorded",
                "data": data
            })
    return jsonify({
        "status": "error",
        "message": "Invalid data"
    }, 400)

@app.route('/api/getnextcandidate', methods=['POST'])
async def getnextcandidate():
    """
    API endpoint that returns a batch of filtered cars from the database
    """
    data = await request.get_json() or {}
    user = data.get('user', {'id': None})
    start_price = data.get('start_price', 0)
    end_price = data.get('end_price', 0)
    start_year = data.get('start_year', 0)
    end_year = data.get('end_year', 0)
    not_fuel_type = data.get('not_fuel_type', None)
    fuel_type = data.get('fuel_type', None)
    limit = data.get('limit', 10)
    
    id = None
    if user:
        id = user.get('id', None)
    
    # Process not_fuel_type if it's a comma-separated string
    if isinstance(not_fuel_type, str) and ',' in not_fuel_type:
        not_fuel_type = not_fuel_type.split(',')
    
    cars = await current_app.car_controller.get_filtered_cars(
        user_id=id,
        start_price=start_price,
        end_price=end_price,
        start_year=start_year,
        end_year=end_year,
        limit=limit,
        not_fuel_type=not_fuel_type,
        fuel_type=fuel_type
    )
    
    if not cars:
        return jsonify({
            "status": "error",
            "message": "No cars available"
        }), 404
    
    return jsonify({
        "status": "success",
        "candidates": cars
    })

@app.route('/api/all_cars', methods=['GET'])
async def all_cars():
    """
    API endpoint that returns all available car types for debugging
    """
    cars = await current_app.car_controller.db.get_hundred_vehicle()
    car_count = len(cars) if cars else 0
    
    return jsonify({
        "status": "success",
        "count": car_count,
        "sample": cars[:5] if cars else []
    })
    
@app.route('/api/remove_like', methods=['POST'])
@require_auth
async def remove_like(data):
    """
    API endpoint for removing a liked vehicle
    """
    user = data.get('user')
    vehicle_id = data.get('candidateId')
    if user and vehicle_id:
        # Add the liked vehicle to the database
        res = await current_app.user_controller.remove_liked_vehicle(user['id'], vehicle_id, app.logger)
        app.logger.info("________Received remove like data______")
        app.logger.info(res)
        app.logger.info("__________________________________________")
        if res:
            return jsonify({
                "status": "success", 
                "message": "Like removed",
                "data": data
            })
    return jsonify({
        "status": "error",
        "message": "Invalid data"
    }), 400
    
@app.route('/api/get_liked_vehicles', methods=['POST'])
@require_auth
async def get_liked_vehicles(data):
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
    
    liked_vehicles, count = current_app.user_controller.get_liked_vehicles(user_id, page, limit)
    
    if not liked_vehicles or count == 0:
        return jsonify({
            "status": "success",
            "message": "No liked vehicles found",
            "data": []
        })
    
    # Pagination logic
    # start = (page - 1) * limit
    # end = start + limit
    # paginated_vehicles = [current_app.car_controller.format_car_for_frontend(car) for car in liked_vehicles[start:end]]
    paginated_vehicles = [current_app.car_controller.format_car_for_frontend(car) for car in liked_vehicles]
    
    return jsonify({
        "status": "success",
        "liked_vehicles": paginated_vehicles,
        "total_count": count,
    })

@app.route('/api/authorize', methods=['POST'])
async def authorize():
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
    data = await request.get_json()
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

