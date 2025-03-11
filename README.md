# Tied-Together
This is an app for making friends via matchmaking.
A Django + DRF application that serves index.html from the root API endpoint.

## Features

- Django 4.2.7
- Django Rest Framework 3.14.0
- Serves static HTML from root endpoint
- Example API endpoint at /api/hello/

## Setup

1. Install dependencies:
   ```
   poetry install
   ```

2. Activate the virtual environment:
   ```
   poetry shell
   ```

3. Run migrations:
   ```
   python manage.py migrate
   ```

4. Start the development server:
   ```
   python manage.py runserver
   ```

5. Visit http://127.0.0.1:8000/ in your browser

## API Endpoints

- `GET /`: Serves the main index.html page
- `GET /api/hello/`: Returns a JSON message

## Running with ngrok

To expose your local development server to the internet, you can use ngrok:

1. Install ngrok:
   - Download from [ngrok.com](https://ngrok.com/download)
   - Or install using package managers:
     ```
     # Using npm
     npm install -g ngrok
     
     # Using Homebrew (macOS)
     brew install ngrok
     ```

2. Run your Django server:
   ```
   python manage.py runserver
   ```

3. In a separate terminal, start ngrok:
   ```
   ngrok http 8000
   ```

4. ngrok will provide a public URL (like `https://abc123.ngrok.io`) that forwards to your local server.

5. Update Django's `ALLOWED_HOSTS` in settings.py to include ngrok URLs:
   ```python
   ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.ngrok.io']
   ```

6. Access your application using the ngrok URL.

Note: Free ngrok accounts have certain limitations, including session expiration and URL changes between sessions.
