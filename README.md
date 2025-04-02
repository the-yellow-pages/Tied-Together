A Flask application that serves index.html from the root API endpoint.

## Features

- Flask 2.3.3
- REST API endpoints for car matchmaking
- Serves static HTML from root endpoint
- Interactive swipe interface for car selection
- Favorites system to save liked vehicles

## Setup

1. Install dependencies:
   ```
   poetry install
   ```

2. Activate the virtual environment:
   ```
   poetry shell
   ```

3. Start the development server:
   ```
   python -m flask run
   ```

   or

   ```
   flask run
   ```

4. Visit http://127.0.0.1:5000/ in your browser

## API Endpoints

- `GET /`: Serves the main index.html page
- `GET /api/getnextcandidate`: Returns a random car for swiping
- `POST /api/goodswipe`: Records a positive swipe
- `POST /api/badswipe`: Records a negative swipe
- `GET /api/all_cars`: Returns a list of all cars (for debugging)
- `POST /api/get_liked_vehicles`: Returns a user's liked vehicles with pagination

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

2. Run your Flask server:
   ```
   flask run --port=8001
   ```

3. In a separate terminal, start ngrok:
   ```
   ngrok http 8001
   ```

   Or use the provided script:
   ```
   ./start_ngrok.sh
   ```

4. ngrok will provide a public URL that forwards to your local server.

5. Access your application using the ngrok URL.

Note: Free ngrok accounts have certain limitations, including session expiration and URL changes between sessions.
