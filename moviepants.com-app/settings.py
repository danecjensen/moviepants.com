# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
MoviePants Application Settings

Variables with all-capitals will be added to the Flask app's configuration.
"""

# Flask configuration
DEBUG = False  # Set to True for development, False for production

# Session configuration
SESSION_COOKIE_SECURE = True  # Require HTTPS for cookies
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection

# TMDB API configuration
# These can be overridden by environment variables
# Get your API key from https://www.themoviedb.org/settings/api
TMDB_API_KEY = ''  # Set via environment variable TMDB_API_KEY
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'
