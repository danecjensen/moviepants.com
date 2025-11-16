# 🎬 MoviePants - Pick a Movie Together

A Flask web application that helps groups of friends choose a movie to watch together. Each friend can add movies to a pool, then everyone votes on them using a Tinder-style swipe interface!

## Quick Start

### Prerequisites
- Python 3.7+
- pip

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. (Optional) Set TMDB API key:
```bash
export TMDB_API_KEY='your_api_key_here'
```
Get your free API key from https://www.themoviedb.org/settings/api

### Run Locally

**Option 1: Quick start script**
```bash
./run.sh
```

**Option 2: Run directly**
```bash
python main.py
```

**Option 3: Production-like with gunicorn**
```bash
gunicorn -b :8080 main:app
```

Open http://localhost:5000 (or :8080 for gunicorn) in your browser.

## Deploy to Google App Engine

1. Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

2. Initialize and configure:
```bash
gcloud init
gcloud config set project YOUR-PROJECT-ID
```

3. Update `app.yaml`:
   - Change `SECRET_KEY` to a secure random value
   - Add your `TMDB_API_KEY` (optional)

4. Deploy:
```bash
gcloud app deploy
```

5. View your app:
```bash
gcloud app browse
```

## How It Works

1. **Create a Session** - One friend creates a session
2. **Friends Join** - Others join with the session ID
3. **Add Movies** - Each friend adds 2 movies from TMDB search
4. **Swipe to Vote** - Everyone swipes on all movies (Tinder-style)
5. **See Winner** - Movie with most likes wins!

## Features

- Session-based movie selection
- TMDB API integration with movie posters
- Each friend can add 2 movies max
- Tinder-style swipe voting interface
- Real-time session updates
- Results page with winner announcement

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: Vanilla JavaScript, HTML/CSS
- **Deployment**: Google App Engine ready
- **API**: The Movie Database (TMDB)

## Documentation

For detailed documentation, see [MOVIEPANTS_README.md](../MOVIEPANTS_README.md) in the root directory.

## License

Open source - MIT License
