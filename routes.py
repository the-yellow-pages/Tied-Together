from flask import render_template, request, jsonify, APIRouter
import random
from app import app

# Simple list of random words for demonstration
RANDOM_WORDS = [
    "Sedan", "SUV", "Truck", "Coupe", "Convertible", 
    "Minivan", "Hatchback", "Sports Car", "Electric", "Hybrid"
]

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
    """
    data = request.get_json()
    # Process the positive swipe data
    # For demonstration, just return a success message
    return jsonify({
        "status": "success", 
        "message": "Positive swipe recorded",
        "data": data
        })

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
    API endpoint that returns a random word as the next candidate
    """
    # For demonstration, simply return a random word from the list
    random_word = random.choice(RANDOM_WORDS)
    return jsonify({
        "status": "success",
        "candidate": random_word,
        "id": random.randint(1, 1000)  # Adding a random ID for demo purposes
    })

@app.route('/api/all_cars', methods=['GET'])
def all_cars():
    """
    API endpoint that returns all available car types for debugging
    """
    return jsonify({
        "status": "success",
        "cars": RANDOM_WORDS
    })
