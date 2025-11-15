#!/bin/bash

# MoviePants - Quick start script

echo "🎬 Starting MoviePants..."
echo ""

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Flask is not installed. Installing dependencies..."
    pip3 install -r requirements.txt
    echo ""
fi

# Check if TMDB_API_KEY is set
if [ -z "$TMDB_API_KEY" ]; then
    echo "⚠️  TMDB_API_KEY is not set."
    echo "   The app will work with mock data, but you won't be able to search real movies."
    echo "   Get an API key from https://www.themoviedb.org/settings/api"
    echo "   Then run: export TMDB_API_KEY='your_key_here'"
    echo ""
fi

# Run the Flask app
echo "Starting Flask server..."
echo "Open http://localhost:5000 in your browser"
echo ""
python3 app.py
