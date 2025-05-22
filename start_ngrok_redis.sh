#!/bin/bash

# Initialize variables to store process IDs
GUNICORN_PID=""
NGROK_PID=""
CELERY_PID=""

# Kill only our processes
cleanup() {
    echo "Stopping all processes..."
    
    # Only kill processes we started
    if [ -n "$GUNICORN_PID" ]; then
        echo "Stopping Gunicorn (PID: $GUNICORN_PID)..."
        kill -TERM $GUNICORN_PID 2>/dev/null || echo "Could not stop Gunicorn"
    fi
    
    if [ -n "$NGROK_PID" ]; then
        echo "Stopping ngrok (PID: $NGROK_PID)..."
        kill -TERM $NGROK_PID 2>/dev/null || echo "Could not stop ngrok"
    fi
    
    if [ -n "$CELERY_PID" ]; then
        echo "Stopping Celery (PID: $CELERY_PID)..."
        kill -TERM $CELERY_PID 2>/dev/null || echo "Could not stop Celery"
    fi
    
    exit 0
}

# Set up trap to catch Ctrl+C and other termination signals
trap cleanup SIGINT SIGTERM

# Check if Redis is running, if not start it
redis_running=$(pgrep -x redis-server)
if [ -z "$redis_running" ]; then
    echo "Starting Redis server..."
    redis-server --daemonize yes
    sleep 1
fi

# Start Gunicorn in the background
echo "Starting Gunicorn server..."
gunicorn --config gunicorn_config.py wsgi:app &
GUNICORN_PID=$!
echo "Gunicorn started with PID: $GUNICORN_PID"

# Give Gunicorn time to start
sleep 2

# Get the port from gunicorn config
PORT=$(grep -oP 'bind\s*=\s*"[^:]+:\K\d+' gunicorn_config.py)
if [ -z "$PORT" ]; then
    PORT=5000  # Default if not found
fi

# Start ngrok with custom domain and log to stdout
echo "Starting ngrok with custom domain up-kiwi-informally.ngrok-free.app on port 8002..."
ngrok http --url=up-kiwi-informally.ngrok-free.app $PORT --log stdout &
NGROK_PID=$!
echo "ngrok started with PID: $NGROK_PID"

# Optionally start Celery worker
echo "Starting Celery worker..."
celery -A app.celery worker --loglevel=info &
CELERY_PID=$!
echo "Celery started with PID: $CELERY_PID"

echo "All services started. Press Ctrl+C to stop."
echo "ngrok URL is available at: http://localhost:4040"

# Wait for termination
wait $GUNICORN_PID $NGROK_PID $CELERY_PID
cleanup