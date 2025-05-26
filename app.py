import os
import random
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from controllers.car import CarController
from controllers.UserController import UserController
from celery_config import make_celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)

# Configure logging
if not os.path.exists('logs'):
    os.makedirs('logs')

file_handler = RotatingFileHandler('logs/car_tinder.log', maxBytes=10240000, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Car Tinder startup')

celery = make_celery(app)

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


with app.app_context():
    app.car_controller = CarController()
    app.user_controller = UserController()
    
# Import routes
from routes.routes import *

# Example of a background task
@celery.task()
def process_data_task(data):
    # Long-running operation here
    return result

# In your Flask routes, use background task for heavy operations:
@app.route('/process')
def process():
    # Start the task asynchronously
    task = process_data_task.delay(some_data)
    return {'task_id': task.id}

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run the app, allowing connections from ALLOWED_HOSTS
    app.run(host='0.0.0.0', port=port, debug=True)
