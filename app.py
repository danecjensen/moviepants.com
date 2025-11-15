from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import secrets
import requests
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# In-memory storage for sessions (use a database in production)
movie_sessions = {}

# TMDB API configuration
TMDB_API_KEY = os.environ.get('TMDB_API_KEY', '')  # Get your API key from https://www.themoviedb.org/settings/api
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'


@app.route('/')
def index():
    """Home page with options to create or join a session"""
    return render_template('index.html')


@app.route('/create-session', methods=['POST'])
def create_session():
    """Create a new movie picking session"""
    session_id = secrets.token_urlsafe(8)
    movie_sessions[session_id] = {
        'created_at': datetime.now().isoformat(),
        'friends': {},  # {friend_name: {'movies_added': 0, 'votes': {}}}
        'movie_pool': [],  # List of movie objects
        'status': 'adding_movies'  # adding_movies, voting, completed
    }
    return jsonify({'session_id': session_id})


@app.route('/session/<session_id>')
def session_page(session_id):
    """Main session page"""
    if session_id not in movie_sessions:
        return "Session not found", 404

    # Store session_id in Flask session
    session['session_id'] = session_id

    sess_data = movie_sessions[session_id]
    return render_template('session.html',
                         session_id=session_id,
                         session_data=sess_data)


@app.route('/join-session', methods=['POST'])
def join_session():
    """Join an existing session with a friend name"""
    data = request.json
    session_id = data.get('session_id')
    friend_name = data.get('friend_name')

    if session_id not in movie_sessions:
        return jsonify({'error': 'Session not found'}), 404

    if not friend_name:
        return jsonify({'error': 'Friend name is required'}), 400

    sess_data = movie_sessions[session_id]

    # Add friend if not already in session
    if friend_name not in sess_data['friends']:
        sess_data['friends'][friend_name] = {
            'movies_added': 0,
            'votes': {}
        }

    # Store friend name in Flask session
    session['friend_name'] = friend_name
    session['session_id'] = session_id

    return jsonify({'success': True, 'friend_name': friend_name})


@app.route('/search-movies')
def search_movies():
    """Search for movies using TMDB API"""
    query = request.args.get('q', '')

    if not query:
        return jsonify({'results': []})

    if not TMDB_API_KEY:
        # Return mock data if no API key is set
        return jsonify({
            'results': [
                {
                    'id': 1,
                    'title': 'The Shawshank Redemption',
                    'poster_path': '/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
                    'overview': 'Two imprisoned men bond over a number of years...',
                    'release_date': '1994-09-23'
                }
            ]
        })

    try:
        response = requests.get(
            f'{TMDB_BASE_URL}/search/movie',
            params={
                'api_key': TMDB_API_KEY,
                'query': query,
                'language': 'en-US',
                'page': 1
            },
            timeout=5
        )
        response.raise_for_status()
        data = response.json()

        # Format results
        results = []
        for movie in data.get('results', [])[:10]:  # Limit to 10 results
            results.append({
                'id': movie['id'],
                'title': movie['title'],
                'poster_path': movie.get('poster_path'),
                'overview': movie.get('overview', ''),
                'release_date': movie.get('release_date', '')
            })

        return jsonify({'results': results})
    except Exception as e:
        print(f"Error searching movies: {e}")
        return jsonify({'error': 'Failed to search movies'}), 500


@app.route('/add-movie', methods=['POST'])
def add_movie():
    """Add a movie to the session pool"""
    data = request.json
    session_id = session.get('session_id')
    friend_name = session.get('friend_name')

    if not session_id or session_id not in movie_sessions:
        return jsonify({'error': 'Invalid session'}), 400

    if not friend_name:
        return jsonify({'error': 'You must join the session first'}), 400

    sess_data = movie_sessions[session_id]
    friend_data = sess_data['friends'].get(friend_name)

    if not friend_data:
        return jsonify({'error': 'Friend not found in session'}), 400

    # Check if friend has already added 2 movies
    if friend_data['movies_added'] >= 2:
        return jsonify({'error': 'You have already added 2 movies'}), 400

    # Add movie to pool
    movie = {
        'id': data['id'],
        'title': data['title'],
        'poster_path': data['poster_path'],
        'overview': data['overview'],
        'release_date': data.get('release_date', ''),
        'added_by': friend_name,
        'votes': {}  # {friend_name: 'like' or 'nope'}
    }

    sess_data['movie_pool'].append(movie)
    friend_data['movies_added'] += 1

    return jsonify({
        'success': True,
        'movies_added': friend_data['movies_added']
    })


@app.route('/start-voting', methods=['POST'])
def start_voting():
    """Start the voting phase"""
    session_id = session.get('session_id')

    if not session_id or session_id not in movie_sessions:
        return jsonify({'error': 'Invalid session'}), 400

    sess_data = movie_sessions[session_id]
    sess_data['status'] = 'voting'

    return jsonify({'success': True})


@app.route('/vote/<session_id>')
def vote_page(session_id):
    """Voting page with tinder-style interface"""
    if session_id not in movie_sessions:
        return "Session not found", 404

    friend_name = session.get('friend_name')
    if not friend_name:
        return redirect(url_for('session_page', session_id=session_id))

    sess_data = movie_sessions[session_id]

    # Get movies that this friend hasn't voted on yet
    movies_to_vote = []
    for movie in sess_data['movie_pool']:
        if friend_name not in movie['votes']:
            movies_to_vote.append(movie)

    return render_template('vote.html',
                         session_id=session_id,
                         friend_name=friend_name,
                         movies=movies_to_vote,
                         tmdb_image_base_url=TMDB_IMAGE_BASE_URL)


@app.route('/submit-vote', methods=['POST'])
def submit_vote():
    """Submit a vote for a movie"""
    data = request.json
    session_id = session.get('session_id')
    friend_name = session.get('friend_name')

    if not session_id or session_id not in movie_sessions:
        return jsonify({'error': 'Invalid session'}), 400

    if not friend_name:
        return jsonify({'error': 'You must join the session first'}), 400

    movie_id = data.get('movie_id')
    vote = data.get('vote')  # 'like' or 'nope'

    sess_data = movie_sessions[session_id]

    # Find the movie in the pool
    for movie in sess_data['movie_pool']:
        if movie['id'] == movie_id:
            movie['votes'][friend_name] = vote
            break

    return jsonify({'success': True})


@app.route('/results/<session_id>')
def results_page(session_id):
    """Show voting results and pick the winner"""
    if session_id not in movie_sessions:
        return "Session not found", 404

    sess_data = movie_sessions[session_id]

    # Calculate scores for each movie (number of likes)
    movie_scores = []
    for movie in sess_data['movie_pool']:
        likes = sum(1 for vote in movie['votes'].values() if vote == 'like')
        total_votes = len(movie['votes'])
        movie_scores.append({
            'movie': movie,
            'likes': likes,
            'total_votes': total_votes,
            'nopes': total_votes - likes
        })

    # Sort by likes (descending)
    movie_scores.sort(key=lambda x: x['likes'], reverse=True)

    return render_template('results.html',
                         session_id=session_id,
                         movie_scores=movie_scores,
                         tmdb_image_base_url=TMDB_IMAGE_BASE_URL,
                         total_friends=len(sess_data['friends']))


@app.route('/session-data/<session_id>')
def get_session_data(session_id):
    """Get current session data (for polling/updates)"""
    if session_id not in movie_sessions:
        return jsonify({'error': 'Session not found'}), 404

    sess_data = movie_sessions[session_id]
    return jsonify({
        'status': sess_data['status'],
        'friends': list(sess_data['friends'].keys()),
        'movie_count': len(sess_data['movie_pool']),
        'movie_pool': sess_data['movie_pool']
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
