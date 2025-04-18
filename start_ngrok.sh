#!/bin/bash

echo "Starting server on port 8002..."
poetry run flask run --host=0.0.0.0 --port=8002 &
FLASK_PID=$!

# Give a moment to start
sleep 2

# Start ngrok tunnel to port 8002
echo "Starting ngrok tunnel to port 8002..."
ngrok http --url=up-kiwi-informally.ngrok-free.app 8002 --log stdout

# When ngrok is killed, also kill the server
kill $FLASK_PID
0