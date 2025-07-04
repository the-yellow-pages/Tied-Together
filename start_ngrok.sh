#!/bin/bash

echo "Starting Quart server on port 5000 with Hypercorn..."
# Start Quart application with Hypercorn ASGI server
poetry run hypercorn app:app --bind 0.0.0.0:5000 --reload &
QUART_PID=$!

# Give a moment to start
sleep 3

# Start ngrok tunnel to port 5000
echo "Starting ngrok tunnel to port 5000..."
ngrok http --url=up-kiwi-informally.ngrok-free.app 5000 --log stdout

# When ngrok is killed, also kill the server
echo "Stopping Quart server..."
kill $QUART_PID
echo "Server stopped."