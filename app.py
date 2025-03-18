import os
import random
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Configuration
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]

origins = []
for host in ALLOWED_HOSTS:
    if host.startswith('.'):  # It's a wildcard domain
        domain = host[1:]  # Remove the leading dot
        origins.append(f"http://*.{domain}")
        origins.append(f"https://*.{domain}")
    else:  # It's a specific host
        origins.append(f"http://{host}")
        origins.append(f"https://{host}")

# Initialize CORS with the allowed origins
CORS(app, origins=origins)

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

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run the app, allowing connections from ALLOWED_HOSTS
    app.run(host='0.0.0.0', port=port, debug=True)
