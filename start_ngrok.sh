#!/bin/bash

echo "Starting server on port 5000..."
# poetry run flask run --host=0.0.0.0 --port=5000 &
gunicorn --config gunicorn_config.py wsgi:app &
FLASK_PID=$!

# Give a moment to start
sleep 2

# Start ngrok tunnel to port 5000
echo "Starting ngrok tunnel to port 5000..."
ngrok http --url=up-kiwi-informally.ngrok-free.app 5000 --log stdout

# When ngrok is killed, also kill the server
kill $FLASK_PID
0