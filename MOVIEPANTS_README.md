# 🎬 MoviePants - Pick a Movie Together

A Flask web application that helps groups of friends choose a movie to watch together. Each friend can add movies to a pool, then everyone votes on them using a Tinder-style swipe interface!

## Features

- **Session-based**: Create a unique session for each movie night
- **Collaborative Movie Selection**: Each friend can add up to 2 movies
- **Movie Search**: Search for movies with poster images using The Movie Database (TMDB) API
- **Tinder-style Voting**: Swipe right to like, swipe left to pass
- **Results Page**: See which movie wins based on the most likes

## How It Works

1. **Create a Session**: One friend creates a movie picking session
2. **Friends Join**: Other friends join using the session ID and their names
3. **Add Movies**: Each friend searches for and adds up to 2 movies to the pool
4. **Start Voting**: Once all movies are added, start the voting phase
5. **Swipe to Vote**: Each friend swipes on all movies (like or pass)
6. **See Results**: The movie with the most likes wins!

## Setup Instructions

### Prerequisites

- Python 3.7+
- pip

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. (Optional) Get a TMDB API key for movie search:
   - Sign up at https://www.themoviedb.org/
   - Go to Settings > API
   - Copy your API key
   - Set it as an environment variable:
   ```bash
   export TMDB_API_KEY='your_api_key_here'
   ```

   **Note**: The app will work without an API key using mock data, but you won't be able to search for real movies.

### Running the Application Locally

**Option 1: Using the quick start script**
```bash
./run.sh
```

**Option 2: Run directly**
```bash
python main.py
```

**Option 3: Using gunicorn (production-like)**
```bash
gunicorn -b :8080 main:app
```

Open your browser and navigate to:
```
http://localhost:5000  (or http://localhost:8080 for gunicorn)
```

Create a session and share the session ID with your friends!

### Deploying to Google App Engine

This application is configured for Google App Engine deployment:

1. Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

2. Initialize your project:
```bash
gcloud init
gcloud config set project YOUR-PROJECT-ID
```

3. Update `app.yaml` with your configuration:
   - Change `SECRET_KEY` to a secure random value
   - Add your `TMDB_API_KEY` if you have one

4. Deploy:
```bash
gcloud app deploy
```

5. View your app:
```bash
gcloud app browse
```

## Usage Guide

### For the Session Creator

1. Click "Create Session" on the home page
2. Enter your name to join the session
3. Share the session ID with your friends
4. Search for and add your 2 movies
5. Wait for friends to add their movies
6. Click "Start Voting" when everyone is ready
7. Swipe on all movies
8. View the results to see which movie won!

### For Friends Joining

1. Get the session ID from the session creator
2. Enter the session ID on the home page
3. Enter your name
4. Add your 2 movies by searching and clicking on posters
5. Wait for the session creator to start voting
6. Swipe on all movies (❤️ Like or ✕ Pass)
7. View the results!

## Technical Details

### Architecture

- **Backend**: Flask (Python web framework)
- **Frontend**: Vanilla JavaScript with HTML/CSS
- **Session Storage**: In-memory (resets when server restarts)
- **Movie Data**: The Movie Database (TMDB) API
- **UI Components**: Custom Tinder-style swipe cards

### File Structure

This project follows the Flask GAE Starter template structure:

```
moviepants.com/
├── main.py                 # Main Flask application
├── settings.py             # Application configuration
├── requirements.txt        # Python dependencies
├── app.yaml               # Google App Engine configuration
├── .gcloudignore          # Files to exclude from GAE deployment
├── run.sh                 # Quick start script for local development
├── templates/
│   ├── base.html          # Base template with common styles
│   ├── index.html         # Home page (create/join session)
│   ├── session.html       # Session page (add movies)
│   ├── vote.html          # Voting page (swipe interface)
│   └── results.html       # Results page (winner announcement)
└── static/                # Static files (CSS, JS, images)
```

### API Endpoints

- `GET /` - Home page
- `POST /create-session` - Create a new movie session
- `GET /session/<session_id>` - Session page
- `POST /join-session` - Join a session with a name
- `GET /search-movies` - Search for movies via TMDB
- `POST /add-movie` - Add a movie to the session pool
- `POST /start-voting` - Start the voting phase
- `GET /vote/<session_id>` - Voting page with swipe interface
- `POST /submit-vote` - Submit a vote for a movie
- `GET /results/<session_id>` - Results page
- `GET /session-data/<session_id>` - Get current session data (for updates)

### Session Data Structure

```python
{
    'session_id': 'unique_id',
    'created_at': 'ISO timestamp',
    'friends': {
        'friend_name': {
            'movies_added': 0,  # Max 2
            'votes': {}         # {movie_id: 'like' or 'nope'}
        }
    },
    'movie_pool': [
        {
            'id': movie_id,
            'title': 'Movie Title',
            'poster_path': '/path.jpg',
            'overview': 'Description',
            'release_date': '2024-01-01',
            'added_by': 'friend_name',
            'votes': {}  # {friend_name: 'like' or 'nope'}
        }
    ],
    'status': 'adding_movies' or 'voting' or 'completed'
}
```

## Production Considerations

This is a development version. For production use, consider:

1. **Database**: Replace in-memory storage with a database (PostgreSQL, MongoDB, etc.)
2. **Session Management**: Use Redis or database-backed sessions
3. **Authentication**: Add user authentication if needed
4. **HTTPS**: Enable SSL/TLS for secure connections
5. **Environment Variables**: Use proper environment variable management
6. **Deployment**: Deploy to a production server (Heroku, AWS, Google Cloud, etc.)
7. **Error Handling**: Add comprehensive error handling and logging
8. **Rate Limiting**: Add rate limiting for API calls
9. **Caching**: Cache TMDB API responses to reduce API calls

## Troubleshooting

### Movie search isn't working
- Make sure you've set the `TMDB_API_KEY` environment variable
- Check your internet connection
- Verify your API key is valid at https://www.themoviedb.org/settings/api

### Session not found
- Sessions are stored in memory and will be lost when the server restarts
- Make sure you're using the correct session ID

### Can't add more movies
- Each friend is limited to 2 movies
- Check that you've joined the session with your name

## Credits

- Movie data provided by [The Movie Database (TMDB)](https://www.themoviedb.org/)
- Tinder-style swipe interface inspired by the tinder-swipe-cards.html template

## License

This project is open source and available under the MIT License.
