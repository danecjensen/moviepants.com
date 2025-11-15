# Getting Started with Flask GAE Starter Template

This guide will help you set up your new project using this template repository.

## Quick Start

### Option 1: Use This Template (Recommended)

1. **Click "Use this template"** button at the top of the GitHub repository
2. **Name your repository** and choose visibility (public/private)
3. **Clone your new repository**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
   cd YOUR-REPO-NAME
   ```

### Option 2: Use Cookiecutter

If you prefer to generate a basic project structure:

```bash
pip install cookiecutter
cookiecutter gh:YOUR-ORG/flask-gae-starter
```

This will create a new project with the structure from the `{{ cookiecutter.project }}` directory.

## Initial Setup

### 1. Set Up Python Environment

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -e .
pip install -r dev-requirements.txt
```

### 2. Choose Your Starting Point

This template provides multiple approaches:

#### A. Use the Library (securescaffold)
Keep the `src/securescaffold/` library and build your app using it:

```python
from securescaffold import create_app

app = create_app(__name__)

@app.route('/')
def index():
    return 'Hello World!'
```

#### B. Start from an Example
Copy one of the examples as your starting point:

```bash
# For a static site:
cp -r examples/static-site/* .

# For a full Flask app:
cp -r examples/python-app/* .

# For language-based redirects:
cp -r examples/language-redirect/* .
```

#### C. Start Fresh
Remove the library and examples, keep only what you need:

```bash
# Remove the library
rm -rf src/securescaffold

# Remove examples
rm -rf examples

# Update setup.py to remove the library references
```

### 3. Configure for Google App Engine

#### Update `app.yaml`

```yaml
runtime: python311  # Use latest Python runtime
entrypoint: gunicorn -b :$PORT main:app

# Add environment variables
env_variables:
  SECRET_KEY: "your-secret-key-here"  # Change this!

# Configure instance settings
instance_class: F1
automatic_scaling:
  min_instances: 0
  max_instances: 5
```

#### Set Up Google Cloud Project

```bash
# Install gcloud CLI if not already installed
# https://cloud.google.com/sdk/docs/install

# Initialize your project
gcloud init

# Create a new project (or use existing)
gcloud projects create YOUR-PROJECT-ID
gcloud config set project YOUR-PROJECT-ID

# Enable required APIs
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 4. Customize Security Settings

Edit your main application file to configure CSP and CSRF settings:

```python
from securescaffold import create_app
from securescaffold.settings import TALISMAN_CONFIG

# Customize Content Security Policy
custom_csp = TALISMAN_CONFIG.copy()
custom_csp['content_security_policy']['default-src'] = ["'self'", "your-cdn.com"]

app = create_app(
    __name__,
    talisman_config=custom_csp
)
```

### 5. Run Tests

```bash
# Run tests with current Python version
pytest

# Run tests across all Python/Flask versions
nox
```

### 6. Local Development

```bash
# Run the development server
python main.py

# Or use gunicorn (more similar to production)
gunicorn -b :8080 main:app
```

Visit http://localhost:8080 to see your app.

## Deployment

### Deploy to Google App Engine

```bash
# Deploy to App Engine
gcloud app deploy

# View your deployed app
gcloud app browse

# Stream logs
gcloud app logs tail -s default
```

### Deploy with Cloud Build (CI/CD)

Create `.github/workflows/deploy.yml` for automatic deployment:

```yaml
name: Deploy to GAE

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - uses: google-github-actions/auth@v2
      with:
        credentials_json: ${{ secrets.GCP_SA_KEY }}

    - uses: google-github-actions/deploy-appengine@v2
```

## Project Structure Cleanup

After setting up, consider cleaning up:

1. **Remove this file**: `rm TEMPLATE_SETUP.md`
2. **Update README.md**: Replace with your project description
3. **Remove unused examples**: `rm -rf examples/`
4. **Update cookiecutter**: Remove if not needed: `rm -rf {{ cookiecutter.project }} cookiecutter.json hooks/`
5. **Update package info**: Edit `setup.py` with your project details

## Next Steps

1. **Set up monitoring**: Enable Google Cloud Monitoring and Error Reporting
2. **Configure Identity-Aware Proxy (IAP)**: For authentication
3. **Add database**: Integrate Cloud Datastore/Firestore
4. **Set up secrets**: Use Google Secret Manager instead of environment variables
5. **Configure custom domain**: Add your domain in App Engine settings

## Getting Help

- **Documentation**: See [README.md](README.md) for API documentation
- **Examples**: Check the `examples/` directory for reference implementations
- **Issues**: Report bugs or request features on GitHub
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines

## Security Checklist

Before deploying to production:

- [ ] Update `SECRET_KEY` in app.yaml
- [ ] Review and customize CSP headers
- [ ] Enable HTTPS enforcement (Talisman does this by default)
- [ ] Configure IAP for authentication if needed
- [ ] Review CSRF protection settings
- [ ] Scan dependencies for vulnerabilities: `pip install safety && safety check`
- [ ] Enable Google Cloud Security Command Center
- [ ] Set up proper IAM roles and permissions
- [ ] Configure Cloud Armor for DDoS protection (if needed)

## Common Issues

### ImportError: No module named 'securescaffold'

Make sure you've installed the package:
```bash
pip install -e .
```

### Tests failing with Flask version errors

Install the correct Flask version:
```bash
pip install 'flask>=2.0'
```

### Deployment fails with runtime error

Ensure `app.yaml` specifies a supported runtime:
```yaml
runtime: python311
```

## Resources

- [Google App Engine Documentation](https://cloud.google.com/appengine/docs/standard/python3)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-Talisman (Security Headers)](https://github.com/GoogleCloudPlatform/flask-talisman)
- [Flask-SeaSurf (CSRF Protection)](https://github.com/maxcountryman/flask-seasurf)
