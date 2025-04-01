from flask import render_template, request, jsonify
import random
from app import app
from controllers.car import CarController
from controllers.UserController import UserController

# Initialize the car controller
car_controller = CarController()
user_controller = UserController()

@app.route('/')
def index():
    """
    Serves the index.html template
    """
    return render_template('index.html')

@app.route('/api/goodswipe', methods=['POST'])
def goodswipe():
    """
    API endpoint for handling a positive swipe
    load
    """
    data = request.get_json()
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
def badswipe():
    """
    API endpoint for handling a negative swipe
    """
    data = request.get_json()
    # Process the negative swipe data
    # For demonstration, just return a success message
    return jsonify({
        "status": "success", 
        "message": "Negative swipe recorded",
        "data": data
        })

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
