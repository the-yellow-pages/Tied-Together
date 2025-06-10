#!/bin/bash

echo "Starting Quart server in production mode with Hypercorn config..."
# Start Quart application with Hypercorn using config file
poetry run hypercorn --config file:hypercorn_config.py app:app &
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
