#!/bin/bash

echo "Starting server on port 8001..."
poetry run flask run --host=0.0.0.0 --port=8001 &
FLASK_PID=$!

# Give a moment to start
sleep 2

# Start ngrok tunnel to port 8001
echo "Starting ngrok tunnel to port 8001..."
ngrok http --url=up-kiwi-informally.ngrok-free.app 8001 --log stdout

# When ngrok is killed, also kill the server
kill $FLASK_PID
0