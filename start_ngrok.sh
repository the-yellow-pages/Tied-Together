#!/bin/bash

# Start Django server in the background
echo "Starting Django server on port 8001..."
poetry run python manage.py runserver 8001 &
DJANGO_PID=$!

# Give Django a moment to start
sleep 2

# Start ngrok tunnel to port 8001
echo "Starting ngrok tunnel to port 8001..."
ngrok http 8001

# When ngrok is killed, also kill the Django server
kill $DJANGO_PID
