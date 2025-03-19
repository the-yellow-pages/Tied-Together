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

# Import routes
from routes import *

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run the app, allowing connections from ALLOWED_HOSTS
    app.run(host='0.0.0.0', port=port, debug=True)
